# Backend Structure Document

## 1. Backend Architecture

We’ve organized the backend as a simple, modular web service that can scale out as demand grows and can be maintained easily over time.

- **Framework & Design Pattern**
  - Built on **Flask**, a lightweight Python web framework.
  - Uses Flask **Blueprints** to split functionality into logical modules (e.g., routing, data refresh, utilities).
  - A small **CLI tool** (using Click) sits alongside the Flask app for command-line access.
  - Routing logic lives in a separate service layer, which wraps the **scgraph** library and provides a clean interface to the web and CLI layers.

- **Scalability & Performance**
  - Stateless Flask containers behind a load balancer let us add more servers as traffic grows.
  - Caching of recent routes in an in-memory store (Redis) cuts down repeated path calculations.
  - Database connections are pooled to handle many simultaneous geospatial queries.

- **Maintainability**
  - Well-defined boundaries: API layer, service layer, data layer.
  - Dockerized setup ensures everyone runs the same environment locally and in production.
  - Automated database migrations (via Alembic) and data update scripts keep schemas and data in sync.

## 2. Database Management

- **Technology & Type**
  - PostgreSQL (relational SQL database).
  - PostGIS extension for geospatial data (points, lines, polygons).

- **Data Structure & Storage**
  - Geospatial tables for ports, channels, waterway polygons, bathymetry grids.
  - A lightweight **routes** table for caching recently computed routes.
  - A **data_update_log** table to record when the automated fetch ran last and whether it succeeded.

- **Data Access & Practices**
  - Use **psycopg2** for database connections.
  - All queries use prepared statements to guard against SQL injection.
  - Spatial queries leverage PostGIS functions (`ST_Intersects`, `ST_DWithin`, `ST_MakeLine`).
  - Automated scripts (run every 6 hours) pull fresh data from external sources and upsert it into PostGIS tables.

## 3. Database Schema

Below is a simplified overview of the main tables. Geometry columns use PostGIS types (POINT, LINESTRING, POLYGON).

1. **ports**
   - id (integer primary key)
   - unlocode (text, unique)
   - name (text)
   - location (geometry POINT)
   - last_updated (timestamp)

2. **channels**
   - id (integer primary key)
   - name (text)
   - geometry (geometry LINESTRING)

3. **waterway_polygons**
   - id (integer primary key)
   - type (text)  // e.g., “river”, “canal”, “coastal”
   - geometry (geometry POLYGON)

4. **bathymetry**
   - id (integer primary key)
   - depth (numeric)
   - geometry (geometry POLYGON)

5. **routes** (cache table)
   - id (serial primary key)
   - parameters (jsonb)  // e.g., {start: "MIAUS", end: "BZCBZE", waypoints: [...]}
   - path (geometry LINESTRING)
   - computed_at (timestamp)

6. **data_update_log**
   - id (serial primary key)
   - service_name (text)  // e.g., "bathymetry_fetch"
   - run_time (timestamp)
   - status (text)  // "success" or "failure"
   - message (text)

### SQL Schema Example (PostgreSQL)

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE ports (
  id           SERIAL PRIMARY KEY,
  unlocode     TEXT UNIQUE NOT NULL,
  name         TEXT NOT NULL,
  location     GEOMETRY(POINT, 4326) NOT NULL,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE channels (
  id       SERIAL PRIMARY KEY,
  name     TEXT,
  geometry GEOMETRY(LINESTRING, 4326)
);

CREATE TABLE waterway_polygons (
  id       SERIAL PRIMARY KEY,
  type     TEXT,
  geometry GEOMETRY(POLYGON, 4326)
);

CREATE TABLE bathymetry (
  id       SERIAL PRIMARY KEY,
  depth    NUMERIC,
  geometry GEOMETRY(POLYGON, 4326)
);

CREATE TABLE routes (
  id          SERIAL PRIMARY KEY,
  parameters  JSONB NOT NULL,
  path        GEOMETRY(LINESTRING, 4326) NOT NULL,
  computed_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE data_update_log (
  id           SERIAL PRIMARY KEY,
  service_name TEXT NOT NULL,
  run_time     TIMESTAMP WITH TIME ZONE DEFAULT now(),
  status       TEXT,
  message      TEXT
);
```  

## 4. API Design and Endpoints

We expose a small set of REST endpoints for both the browser UI and CLI tool.

- **GET /api/ports**
  - Returns a list of available ports (UN/LOCODE + name + coordinates).

- **POST /api/route**
  - Request body: `{ "start": "MIAUS", "end": "BZCBZE", "waypoints": ["MNZMX"], "options": {...} }`
  - Response: GeoJSON feature containing the route polyline and waypoints.
  - Caches the result in the `routes` table for quick repeat lookups.

- **GET /api/route?start=...&end=...**
  - Shortcut for clients that just need URL params.

- **POST /api/refresh-data**
  - Triggers manual refresh of geospatial datasets.
  - Returns status of the last update attempt.

- **GET /api/status**
  - Returns service health (database connection, last data update timestamp).

All endpoints return JSON and set `Access-Control-Allow-Origin: *` so the UI can call them directly.

## 5. Hosting Solutions

We chose **Amazon Web Services (AWS)** for reliability, scaling, and cost control.

- **Compute**: Docker containers running on **ECS Fargate** (serverless containers). No instances to manage.
- **Database**: **Amazon RDS for PostgreSQL** with PostGIS enabled. Backups and failover automated.
- **Storage**: **Amazon S3** for storing any generated files (e.g., GeoJSON downloads).
- **Domain & SSL**: **Route 53** + **AWS Certificate Manager** for TLS certificates.

Benefits:
- Managed services reduce operational burden.
- Autoscaling for spikes in use.
- Pay-as-you-go keeps costs low for a POC environment.

## 6. Infrastructure Components

- **Load Balancer**
  - AWS Application Load Balancer (ALB) in front of ECS tasks distributes traffic.

- **Caching**
  - **Amazon ElastiCache Redis** used by Flask-Caching to store frequently requested routes.

- **Scheduled Tasks**
  - **AWS EventBridge** (CloudWatch Events) triggers ECS tasks every 6 hours to refresh bathymetry, ports, and polygon data.

- **CDN**
  - **CloudFront** serves static assets (JS, CSS) and any GeoJSON files for faster downloads worldwide.

- **Secrets Management**
  - **AWS Secrets Manager** stores database credentials and API keys for data sources.

## 7. Security Measures

- **Encryption in transit** using HTTPS (TLS managed by ACM).
- **No user authentication** is required (open access), but we protect endpoints with **rate limiting** (Flask-Limiter) to prevent abuse.
- **Encrypted at rest**: RDS and ElastiCache are encrypted by default.
- **Principle of least privilege**: ECS tasks assume an IAM role that only allows the permissions they need (e.g., read secrets, write logs).
- **Input validation** on all endpoints to avoid injection attacks.

## 8. Monitoring and Maintenance

- **Logging & Metrics**
  - Flask logs (stdout) go to **CloudWatch Logs**.
  - Custom metrics (route times, data-refresh success rates) pushed to **CloudWatch Metrics**.
  - Optional Sentry integration for error tracking.

- **Alarms & Alerts**
  - CloudWatch alarms notify the team if API latency exceeds thresholds or if data updates fail.

- **Backups & Recovery**
  - RDS automated daily snapshots and point-in-time recovery.
  - Regular export of PostGIS tables to S3 for offsite archival.

- **Maintenance**
  - Weekly dependency updates via CI pipeline.
  - Database schema changes managed through Alembic migrations.

## 9. Conclusion and Overall Backend Summary

In summary, the backend for the Ship Routing Enhancement Project v2 uses a straightforward Flask service layered over PostgreSQL/PostGIS. It integrates the scgraph library for routing, automates data refreshes every six hours, and provides a small set of well-defined REST endpoints. The entire stack runs in Docker containers on AWS ECS Fargate, backed by managed RDS, Redis caching, and CloudFront. Security, monitoring, and automated maintenance practices are in place to ensure reliability and performance. This design delivers the accuracy, speed, and scalability needed to compute and visualize ship routes across North American coastal and inland waterways.
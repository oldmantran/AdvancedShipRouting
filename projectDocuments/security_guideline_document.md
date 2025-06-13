# Implementation Plan for Ship Routing Enhancement Project v2

## 1. Architecture Overview

**Components**
- Backend Service (Python / Flask)
- Geospatial Database (PostgreSQL + PostGIS)
- Front-end (HTML/CSS, JavaScript, Leaflet)
- Data Ingestion & Update Pipeline
- Dockerized Deployment

**Data Flow**
1. User issues route request (port codes or map clicks) via UI or CLI/URI.  
2. Flask API validates input → queries PostGIS for waterway graph, bathymetry, ports.  
3. Enhanced `scgraph` executes A* or Dijkstra with land-avoidance constraints.  
4. API returns GeoJSON route.  
5. Front-end renders polylines over OSM/OpenSeaMap; offers download.

## 2. Backend Service

### 2.1 Tech Stack & Frameworks
- Python 3.9+  
- Flask (REST API, CLI entrypoint)  
- scgraph (routing core, extended)  
- psycopg2 (PostGIS connectivity)  
- requests (AIS data via VesselFinder API)  
- Gunicorn or uWSGI (production WSGI server)

### 2.2 API Design

**Endpoints**
- `GET /route`  
  • Query params: `start_unlocode`, `end_unlocode`, optional `waypoints` (lat,lon list)  
  • Responses: 200 → GeoJSON LineString + metadata; 400/422 → validation errors; 500 → generic error.

- `POST /refresh-data`  
  • Triggers manual refresh of all geospatial datasets.  
  • Protected by a simple token in header (rotate via env var).

- `GET /health`  
  • Liveness & readiness checks (DB connectivity, last refresh timestamp).

### 2.3 Routing Engine Enhancement
- Wrap `scgraph` to load graph edges from PostGIS: waterways, channels, rivers.  
- Precompute weighted graph: edge weights = distance / navigability factor (depth, traffic).  
- Implement land-avoidance: spatial filter `ST_Intersects(waterways, path_segment)`.  
- Support inland‐only legs by restricting to river/canal layers.  
- Caching: LRU cache for frequent port‐to‐port queries.

### 2.4 Security & Hardening
- **Input Validation**: Use Marshmallow or Pydantic to validate/unmarshal JSON and query params.  
- **Output Encoding**: Sanitize all string outputs; return only required fields.  
- **Error Handling**: Catch exceptions; return generic messages; log stack traces securely.  
- **Secrets Management**: Load API keys, DB URLs via environment variables; do not commit secrets.  
- **HTTPS Enforcement**: In production, terminate TLS at load balancer or use Flask-TLS.  
- **Rate Limiting**: Flask-Limiter to throttle `/route` calls (e.g., 30 requests/minute/IP).  
- **CORS**: Restrictive policy (`Access-Control-Allow-Origin` to deployed UI domain).  
- **HTTP Headers**: Attach HSTS, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin`.

## 3. Data Integration & Storage

### 3.1 Database Schema
- **Tables**
  - `waterways` (POLYGON/MULTILINESTRING): geometry, type, navigability_index
  - `bathymetry` (POLYGON): depth, reliability_score
  - `ports` (POINT): UN/LOCODE, name, attributes
  - `graph_edges` (LINESTRING): source_id, target_id, weight, metadata
- **Indexes**: GIST on geometry columns; B-tree on UN/LOCODE.

### 3.2 ETL & Refresh Pipeline
- Python script (`data_sync.py`) to:
  1. Download OpenSeaMap, NOAA bathymetry, Global Maritime Traffic.
  2. Sanitize inputs (validate CRS, drop invalid geometries).
  3. Load into staging tables (use `COPY` or `ogr2ogr`).
  4. Transform & upsert into production tables in a transaction.

- **Automation**
  - Cronjob or systemd timer inside Docker container: run every 6 hours.  
  - Expose manual trigger via `/refresh-data`.

### 3.3 Security for Data Layer
- **Least Privilege DB User**: grant only `SELECT`, `INSERT`, `UPDATE` on specific tables.  
- **Encrypted Connections**: require SSL/TLS for Postgres client connections.  
- **Backup & Retention**: nightly dumps; rotate older than 7 days.

## 4. Front-End Implementation

### 4.1 UI Features
- Input form for port codes + dynamic map clicks for custom waypoints.  
- "Calculate Route" button → calls `/route`.  
- "Refresh Data" button → calls `/refresh-data` with auth token.

### 4.2 Map Integration
- Leaflet with OSM base layer + OpenSeaMap nautical charts.  
- Add GeoJSON Layer for returned route (LineString).  
- Waypoint markers: custom icons for ports vs user‐placed markers.  
- Download: generate Blob from GeoJSON; link with `download` attribute.

### 4.3 Front-end Security
- **Content Security Policy**: restrict script/style sources to self and approved CDNs (with SRI).  
- **Sanitize Inputs**: reject invalid port codes client-side; server enforces.  
- **Avoid Local Storage**: ephemeral state only; no sensitive data stored.

## 5. Testing & QA

### 5.1 Unit & Integration Tests
- Use PyTest for backend: validate routing logic, API responses, error cases.  
- JS unit tests (Jest) for front-end input validation, map rendering.

### 5.2 Performance Benchmarking
- Automated tests to measure 1–3s for regional; 3–5s for trans-Atlantic.  
- Use Locust or JMeter for concurrency tests.

### 5.3 Geospatial Validation
- Compare sample routes against NOAA charts / known AIS tracks.  
- Visual QA: overlay computed routes on official nautical chart PDFs.

## 6. Deployment & DevOps

### 6.1 Containerization
- Docker images for backend and DB.  
- `docker-compose.yml` to orchestrate services.  
- Non‐root container users; minimal base images (alpine-slim).

### 6.2 CI/CD Pipeline
- GitHub Actions: lint (flake8, ESLint), run tests, build Docker, push to registry.  
- Manual or gated deploy to staging/production.

### 6.3 Configuration Management
- All configs via environment variables (12-factor).  
- Example `.env.sample` with placeholders; exclude `.env` from Git.

### 6.4 Monitoring & Logging
- Centralized logs (ELK or CloudWatch).  
- Health check alerts; data‐refresh failures trigger notifications.

### 6.5 Production Hardening
- Disable Flask debug; use secure cookie flags.  
- Rotate API keys quarterly; revoke unused Vault secrets.  
- Regularly scan images with SCA (Trivy, Snyk).

## 7. Timeline & Milestones

| Phase           | Duration | Deliverables                                   |
|-----------------|----------|------------------------------------------------|
| Kickoff & Setup | 1 week   | Repo structure, Docker configs, DB schema      |
| Data Pipeline   | 2 weeks  | ETL scripts, automated refresh, seed data      |
| Backend Core    | 3 weeks  | Enhanced routing, API endpoints, unit tests    |
| Front-end       | 2 weeks  | Leaflet UI, form inputs, download feature      |
| Integration     | 1 week   | End-to-end tests, performance tuning            |
| Deployment      | 1 week   | CI/CD, staging deploy, security hardening      |
| QA & Sign-off   | 1 week   | Final validation, documentation, demo          |

**Total**: ~11 weeks (POC scope)

---
*All components adhere to security-by-design, least privilege, defense in depth, secure defaults, and fail-securely principles.*
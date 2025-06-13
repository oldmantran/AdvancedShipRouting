# Implementation plan

This implementation plan translates the Ship Routing Enhancement Project v2 requirements into an exact, step-by-step plan for AI-driven execution.

## Phase 1: Environment Setup

1. **Pre-validation**: Detect if current directory is already a Git repository. If not, proceed; otherwise skip Git initialization. (Reference: Project Overview)
2. **Initialize Git**: Run `git init` at project root and create `.gitignore` with entries for `venv/`, `__pycache__/`, `node_modules/`, and `*.pyc`. (Reference: Development & Deployment)
3. **Check Python**: Verify Python 3.11.4 is installed by running `python3.11 --version`; if missing, instruct user to install Python 3.11.4. (Reference: Technology Stack: Back-end)
4. **Check Docker**: Run `docker --version`; if Docker is not installed, instruct user to install Docker Desktop. (Reference: Technology Stack: Development & Deployment)
5. **Validate Docker**: Run `docker info` to ensure Docker daemon is running. (Reference: Technology Stack: Development & Deployment)
6. **Create Virtualenv**: Run `python3.11 -m venv venv` at project root; then activate with `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows). (Reference: Technology Stack: Back-end)
7. **Install Python Dependencies**: Create `/backend/requirements.txt` listing `Flask==2.3.2`, `psycopg2-binary==2.9.6`, `requests==2.31.0`, `flask-cors==3.0.10`, and `scgraph-enhanced==1.0.0`. Run `pip install -r backend/requirements.txt`. (Reference: Technology Stack: Back-end)
8. **Project Structure**: Create directories: `/backend`, `/frontend`, `/data`, `/cron`. (Reference: Project Overview)
9. **README.md**: Create `README.md` at project root with project name, overview, and basic setup commands. (Reference: Project Overview)

## Phase 2: Frontend Development

10. **HTML Boilerplate**: Create `/frontend/index.html` with `<head>` linking to Leaflet CSS & JS (v1.9.4) and OpenSeaMap layers. (Reference: Technology Stack: Front-end)
11. **CSS**: Create `/frontend/css/style.css` defining colors from UI Design & Branding (Primary: `#E1A141`, Secondary: `#00FFB2`, etc.). (Reference: UI Design & Branding)
12. **Map Initialization**: Create `/frontend/js/map.js` that initializes a Leaflet map centered on Miami coordinates `[25.7617, -80.1918]` with both OpenStreetMap and OpenSeaMap tile layers. (Reference: Geographic Scope)
13. **UI Controls**: Create `/frontend/js/ui.js` that builds a dropdown for UN/LOCODE port codes and sets up click listener on map to capture waypoints. (Reference: Functional Requirements)
14. **GeoJSON Download**: In `/frontend/js/map.js`, add a control button to export current route as GeoJSON and trigger download. (Reference: Functional Requirements)
15. **Front-end Tests**: Create `/frontend/tests/map.test.js` using Jest to check that `L.map` is called and tile layers are added. Run `npm init -y` and `npm install jest leaflet`. (Reference: Quality Assurance)
16. **Validation**: Open `index.html` in a local server (e.g., `npx serve frontend`) and confirm map loads with both layers and UI controls render. (Reference: Functional Requirements)

## Phase 3: Backend Development

17. **Flask App**: Create `/backend/app.py` with Flask app instance and register CORS for endpoint `/route` allowing `*`. (Reference: Technology Stack: Back-end)
18. **CLI Entry Point**: In `/backend/app.py`, add `if __name__ == "__main__"` block to support `python app.py --start <lat1,long1> --end <lat2,long2>`. (Reference: Functional Requirements)
19. **Docker Postgres**: Create `docker-compose.yml` in project root defining service `db` using `postgres:15.3` with environment `POSTGRES_PASSWORD=postgres` and port mapping `5432:5432`. (Reference: Data Storage and Serving)
20. **PostGIS Extension**: After `docker-compose up -d`, run `docker exec -it <container_id> psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS postgis;"`. (Reference: Data Storage and Serving)
21. **Database Schema**: Create `/data/schema.sql` with tables:
    - `waterways(id SERIAL PRIMARY KEY, geom GEOMETRY(POLYGON,4326), weight FLOAT)`
    - `bathymetry(id SERIAL PRIMARY KEY, geom GEOMETRY(POLYGON,4326), depth FLOAT)`
    - `ports(id SERIAL PRIMARY KEY, locode VARCHAR(5) UNIQUE, geom GEOMETRY(POINT,4326))`
   (Reference: Data Storage and Serving)
22. **Load Data Script**: Create `/data/load_data.py` that uses `psycopg2` to connect to `postgresql://postgres:postgres@localhost:5432/postgres` and execute `schema.sql`, then ingest OpenSeaMap, NOAA bathymetry, and port CSV. (Reference: Data Storage and Serving)
23. **Validate DB Load**: Run `python data/load_data.py` and then run `docker exec -it <container_id> psql -U postgres -c "SELECT COUNT(*) FROM waterways;"`. (Reference: Data Storage and Serving)
24. **Routing Module**: Create `/backend/routing.py` that:
    1. Connects to Postgres via `psycopg2`.  
    2. Builds a graph using enhanced `scgraph` with edges weighted by distance and inland-waterway bias.  
    3. Implements A* using PostGIS `ST_Contains` to ensure path segments lie within waterways.  (Reference: Key Implementation Details)
25. **VesselFinder Integration**: Create `/backend/vesselfinder.py` using `requests` to fetch AIS data from `https://api.vesselfinder.com/*` with API key stored in environment variable `VESSELFINDER_KEY`. (Reference: Functional Requirements)
26. **Route Endpoint**: In `/backend/app.py`, add `@app.route('/route', methods=['GET'])` that accepts `start`, `end`, optional `waypoints` (array of `lat,long`), looks up port codes if provided, calls `routing.calculate_route()`, and returns GeoJSON. (Reference: Functional Requirements)
27. **Data Refresh Script**: Create `/cron/refresh_data.py` that runs every 6 hours:
    - Clears and reloads waterway, bathymetry, and port tables.  
    - Use Python `schedule` or cron.  
   (Reference: Functional Requirements)
28. **Cron Job**: Add entry to user’s crontab (`crontab -e`): `0 */6 * * * /usr/bin/python3.11 /path/to/project/cron/refresh_data.py`. (Reference: Functional Requirements)
29. **Validation – CLI**: Run `python backend/app.py --start 25.7617,-80.1918 --end 17.5046,-88.1962` and verify printed GeoJSON route within 1–5 seconds. (Reference: Performance)
30. **Validation – HTTP**: Use `curl 'http://localhost:5000/route?start=25.7617,-80.1918&end=17.5046,-88.1962'` and check for 200 response with valid GeoJSON. (Reference: Performance)

## Phase 4: Integration

31. **Front-end API Module**: Create `/frontend/js/api.js` with `async function fetchRoute(start, end, waypoints)` that calls `/route` endpoint and returns parsed GeoJSON. (Reference: App Flow)
32. **Map Rendering**: In `/frontend/js/map.js`, tie `fetchRoute` to UI controls—on form submit, call `fetchRoute`, then plot resulting GeoJSON polyline in color `#AA84FB`. (Reference: Functional Requirements)
33. **CORS Validation**: Confirm that Flask CORS allows front-end origin by loading `index.html` and performing a route request in browser console without errors. (Reference: Functional Requirements)
34. **End-to-End Test**: Create `/frontend/tests/e2e.spec.js` using Cypress to simulate selecting ports Miami → Belize City → Manzanillo and asserting polyline appears. Run `npx cypress run`. (Reference: Quality Assurance)

## Phase 5: Deployment

35. **Docker Compose for Full Stack**: Extend `docker-compose.yml`:
    - Service `web`:
        image: `python:3.11-slim`
        volumes: `./backend:/app`
        command: `sh -c "pip install -r requirements.txt && python app.py"`
        ports: `5000:5000`
        depends_on: `db`
   (Reference: Development & Deployment)
36. **Validate Full Stack Locally**: Run `docker-compose up --build` and `docker-compose ps` to ensure both `db` and `web` are `Up` (healthy). (Reference: Development & Deployment)
37. **README Update**: Add Docker Compose instructions and sample `curl` commands under a **Deployment** section in `README.md`. (Reference: Development & Deployment)
38. **Single-Instance Deployment**: Advise user to deploy on a VM (e.g., AWS EC2 `t3.medium` in `us-east-1`) by installing Docker and following Docker Compose steps. (Reference: Availability)
39. **Post-Deployment Check**: Run end-to-end test against VM public IP: `curl http://<EC2_IP>:5000/route?start=25.7617,-80.1918&end=17.5046,-88.1962`. (Reference: Availability)
40. **Performance Monitoring**: Suggest adding basic logging in `/backend/app.py` to log execution time of `calculate_route()` and output to `logs/app.log`. (Reference: Performance)

---
Total steps: 40. Each step includes a single action, file paths, and references to the source sections of the project summary.
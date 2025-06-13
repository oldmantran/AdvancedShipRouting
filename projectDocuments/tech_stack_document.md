# Tech Stack Document for Ship Routing Enhancement Project v2

This document explains the technologies chosen for the Ship Routing Enhancement Project v2 in everyday language. It clarifies each tool’s role and how they work together to deliver accurate, land-avoiding vessel routes.

## 1. Frontend Technologies
The user interface displays maps, allows waypoint input, and shows results clearly. We chose lightweight, well-supported tools to keep the UI fast and simple.

• HTML & CSS
  - Structure and style the web pages.
  - CSS applies our color palette (e.g., #E1A141 for buttons, #AA84FB for routes) and Roboto font for readability.

• JavaScript
  - Powers interactive features like form validation and map controls.

• Leaflet
  - A lightweight mapping library that displays OpenStreetMap tiles.
  - Renders GeoJSON polylines for routes and markers for waypoints.
  - Supports overlaying nautical charts from OpenSeaMap and depth contours.

• OpenStreetMap & OpenSeaMap
  - Base map layers for general geography and detailed maritime data (channels, depth lines).

• VS Code
  - Developer code editor with extensions for HTML, CSS, and JavaScript to speed up development.

## 2. Backend Technologies
The backend handles route calculations, data storage, and API calls. We use proven Python tools for geospatial processing and web serving.

• Python
  - Main programming language for routing logic, data processing, and scripting updates.

• Flask
  - A lightweight Python web framework that handles HTTP requests and serves JSON or GeoJSON responses.

• scgraph
  - Open-source Python library extended with bathymetry and waterway constraints to compute routes as [latitude, longitude] tuples.

• PostgreSQL + PostGIS
  - Stores geospatial data: waterway polygons, bathymetry contours, ports, and channels.
  - Provides spatial queries (e.g., ST_Contains, ST_Intersects) to enforce land-avoiding constraints and weight sea lanes.

• psycopg2
  - Python library to connect Flask and Python scripts with PostgreSQL/PostGIS.

• requests
  - Python library to fetch external data (e.g., AIS data from VesselFinder, maritime datasets).

• Docker
  - Containerizes the backend and database for consistent local or cloud deployment.

## 3. Infrastructure and Deployment
We chose tools to ensure reliable development, version control, and easy deployment—even in a proof-of-concept stage.

• Git & GitHub
  - Version control system to track code changes and collaborate.

• Docker & Docker Compose
  - Encapsulate the Flask app and PostGIS database in containers.
  - Simplifies setup on any machine or cloud VM.

• Hosting Platforms
  - Local development: Docker containers on a developer’s machine.
  - Cloud deployment: Single-instance VM (e.g., AWS EC2) running Docker containers.

• CI/CD Pipeline (optional)
  - GitHub Actions can automate linting, testing, and container builds on each push.

• Scheduled Tasks
  - Linux cron jobs inside the Docker container to run Python scripts every 6 hours for dataset updates.

## 4. Third-Party Integrations
We pull in external services and data to enrich routing accuracy and real-time information.

• VesselFinder AIS API
  - Provides current vessel positions for route validation and situational awareness.

• OpenSeaMap Data
  - Coastal and inland waterway polygons for navigability constraints.

• NOAA or IHO Bathymetry Data
  - Depth contours used to weight edges in the routing graph for safety.

• Global Maritime Traffic Data
  - Port and channel locations (e.g., UN/LOCODE entries) for waypoint lookups.

## 5. Security and Performance Considerations
Despite no user login, we implement basic measures to protect data and ensure speed.

Security Measures:
• HTTPS (TLS)
  - Encrypts all data between browser and server to prevent eavesdropping.

• Input Validation
  - Port codes and map coordinates validated against PostGIS tables using ST_Contains to reject invalid or off-water points.

• Dependency Management
  - Pin Python package versions in requirements.txt.
  - Regularly update Docker base images.

Performance Optimizations:
• Spatial Indexing
  - GiST indexes on PostGIS tables speed up ST_Contains and ST_Intersects queries.

• Graph Simplification
  - Reduce nodes with techniques like Douglas–Peucker where high precision isn’t needed.

• Caching
  - In-memory or Flask-caching of recently computed routes for identical origin-destination requests.

• Response-Time Targets
  - Regional routes (e.g., Miami→Belize City→Manzanillo): 1–3 seconds.
  - Longer routes (trans-Atlantic): under 5 seconds.

## 6. Conclusion and Overall Tech Stack Summary
Our chosen stack balances simplicity and power to deliver accurate, land-avoiding maritime routes in a proof-of-concept:

• Frontend: HTML/CSS, JavaScript, Leaflet, OpenStreetMap/OpenSeaMap, styled with a clear color palette and Roboto font.
• Backend: Python, Flask, scgraph, PostgreSQL/PostGIS, psycopg2, requests.
• Infrastructure: Docker, Git/GitHub, optional GitHub Actions, cron jobs for data updates, deployable locally or on a cloud VM.
• Integrations: VesselFinder AIS, OpenSeaMap, NOAA/IHO bathymetry, global port/channel datasets.
• Security & Performance: HTTPS, input validation, spatial indexing, caching, and targeted response times.

This combination ensures that the PoC meets its goals—accurate water-only vessel routing, inland waterway support, consistent results, and fast performance—while remaining easy to develop, deploy, and test.
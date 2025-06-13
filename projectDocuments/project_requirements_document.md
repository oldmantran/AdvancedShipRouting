# Project Requirements Document

## 1. Project Overview

The **Ship Routing Enhancement Project v2** aims to upgrade an existing maritime routing proof-of-concept that currently uses the open-source `scgraph` library. While `scgraph` can generate basic sea routes, it often produces paths that cross land, ignores inland waterways, and fails to adapt to real-world navigational channels. This project will integrate richer geospatial datasets (coastal outlines, river and canal polygons, bathymetry contours) and a more robust routing engine (either an enhanced `scgraph` implementation or a maritime-specific API) to generate accurate, land-avoiding, and optimized vessel routes.

We’re building this to demonstrate a reliable back-end service (invocable via command-line or HTTP URL) that:

*   Produces valid sea and inland-waterway routes (e.g., Miami → Belize City → Manzanillo)
*   Completes routing calculations in under 5 seconds
*   Offers interactive map rendering with OpenStreetMap/Leaflet and downloadable GeoJSON\
    Success means consistent, reproducible routes that respect navigable waters, integrate AIS data from VesselFinder, and allow a single user to plan and export voyages without manual workarounds.

## 2. In-Scope vs. Out-of-Scope

**In-Scope (Version 1 PoC)**

*   Command-line / HTTP-URL back-end service for route calculation

*   Integration with VesselFinder API for live AIS data

*   PostGIS database storing:

    *   Coastal and inland waterway polygons (OpenSeaMap)
    *   Bathymetry contours (NOAA/IHO)
    *   Port and channel locations (global traffic data)

*   Enhanced routing algorithm (A* or Dijkstra) with:

    *   Land-avoiding constraints (ST_Contains checks)
    *   Inland waterway prioritization (weighted edges)

*   Interactive web map (Leaflet + OpenStreetMap/OpenSeaMap) showing:

    *   Polylines in purple (#AA84FB)
    *   Waypoints in green (#00FFB2)

*   GeoJSON export of computed routes

*   Automatic 6-hour dataset updates + manual “Refresh Data” button

*   Open access (no user authentication) in a controlled environment

**Out-of-Scope (Later Phases)**

*   Full multi-user authentication or role-based access
*   Batch CSV/KML route uploads
*   Mobile app or offline-first features
*   PDF map exports or advanced printing
*   Global coverage beyond North America, Caribbean, Mexico, Great Lakes, and Mississippi River
*   Production-scale deployment, high-availability clustering, or full container orchestration

## 3. User Flow

A user navigates to the PoC URL (or runs the CLI) and immediately sees a clean Flask-powered page styled with Roboto fonts and the project’s Figma color palette (orange #E1A141 for buttons, white background, black text). A nautical map (OpenSeaMap tiles) occupies most of the screen. Above or beside it are input fields for origin, destination, and optional waypoints—either as UN/LOCODE port codes from a dropdown (e.g., USMIA, BZBZE, MXZLO) or clickable map points validated against navigable water polygons.

Once points are set, the user clicks **Calculate Route**. A spinner appears while the Flask back-end queries PostGIS, runs the enhanced `scgraph` (or alternative) with waterway/bathymetry constraints, and returns a GeoJSON LineString. In under 3 seconds for regional routes (under 5 seconds for long-haul), Leaflet draws a purple polyline, and waypoints become interactive markers showing port codes and segment distances. The user can pan/zoom freely.

If needed, the user hits **Download GeoJSON** to save the route or clicks **Refresh Data** to trigger an on-demand update of waterways, bathymetry, and port tables. Any errors (invalid port code, point outside waterways, API fetch failure) surface as red alerts (#FF7979) with clear messages and highlighted inputs for quick correction.

## 4. Core Features

*   **Command-Line / HTTP Routing Service**\
    ­– Invoke via CLI or URL with query parameters for ports/waypoints.
*   **AIS Data Integration**\
    ­– Fetch real-time vessel positions from VesselFinder API.
*   **Geospatial Storage (PostGIS)**\
    ­– Store waterway polygons, bathymetry, ports/channels with spatial indexing.
*   **Enhanced Pathfinding Algorithm**\
    ­– A* or Dijkstra’s with weighted edges (distance, depth, navigability).\
    ­– Enforce land-avoiding constraints using `ST_Contains`.\
    ­– Prioritize inland waterways by assigning lower weights.
*   **Interactive Map Visualization**\
    ­– Leaflet + OpenStreetMap/OpenSeaMap for nautical charts.\
    ­– Purple polylines for routes, green markers for waypoints.
*   **GeoJSON Export**\
    ­– Downloadable LineString feature for external use.
*   **Automated & Manual Data Refresh**\
    ­– Cron-driven 6-hour updates + Flask endpoint (`/refresh_data`).
*   **Error Handling & Alerts**\
    ­– Immediate UI feedback on invalid inputs or data fetch failures.

## 5. Tech Stack & Tools

*   **Backend**\
    ­– Python 3.x, Flask (HTTP API & CLI wrapper)\
    ­– scgraph (enhanced) or alternative routing API (OpenRouteService, SeaRoute)
*   **Database**\
    ­– PostgreSQL + PostGIS (geometry/geography types, GiST indexes)\
    ­– Data import via `psycopg2`, GDAL/OGR
*   **Frontend**\
    ­– HTML/CSS, JavaScript\
    ­– Leaflet for map rendering\
    ­– OpenStreetMap & OpenSeaMap tile layers
*   **Data Sources**\
    ­– OpenSeaMap polygons, NOAA/IHO bathymetry, global maritime traffic
*   **Development Tools**\
    ­– VS Code (with Python, Docker extensions)\
    ­– Docker for local dev (PostGIS container)
*   **Optional Future Integrations**\
    ­– OpenRouteService / SeaRoute APIs for advanced routing\
    ­– CI tools (GitHub Actions) for automated testing

## 6. Non-Functional Requirements

*   **Performance**\
    ­– Regional routes: ≤ 3 seconds\
    ­– Trans-Atlantic: ≤ 5 seconds\
    ­– Map render: ≤ 0.5 seconds
*   **Scalability**\
    ­– Single-user PoC; no horizontal scaling required initially
*   **Availability & Maintainability**\
    ­– Local or single-instance cloud (Docker/EC2)\
    ­– Automated dataset imports every 6 hours
*   **Security**\
    ­– Open access in controlled network; no public credentials\
    ­– Sanitized user inputs (port codes, coordinates)
*   **Usability**\
    ­– WCAG-compliant color contrasts (text #08070C on white)\
    ­– Intuitive buttons and map controls
*   **Compliance**\
    ­– Open-source licenses for `scgraph`, OpenStreetMap, GDAL

## 7. Constraints & Assumptions

*   **Constraints**\
    ­– Rely on `scgraph` enhancements or compatible routing API under permissive license\
    ­– PostGIS must handle 10 – 100 GB of geospatial data within a single instance\
    ­– VesselFinder API rate limits apply to AIS data fetches
*   **Assumptions**\
    ­– Single user (logistics manager) context; no concurrency stress\
    ­– Host environment supports Python 3.x, Docker or native PostGIS\
    ­– Geospatial sources (OpenSeaMap, NOAA) provide reliable updates\
    ­– Network latency low enough to meet performance targets

## 8. Known Issues & Potential Pitfalls

*   `scgraph`** Limitations**\
    ­– May require graph pre-processing to avoid land crossings; consider fallback to OpenRouteService.
*   **Geospatial Data Gaps**\
    ­– Incomplete inland waterway polygons can cause false routing errors; mitigate with manual data patches.
*   **API Rate Limits**\
    ­– VesselFinder throttling may delay AIS integration; implement local caching and retry logic.
*   **Performance Bottlenecks**\
    ­– Complex coastal graphs can slow A*/Dijkstra; mitigate with spatial indexing, graph simplification (Douglas-Peucker).
*   **Data Import Failures**\
    ­– Source format changes (GeoJSON → Shapefile) could break import scripts; include schema validation and alerting.
*   **Map Tile Availability**\
    ­– OpenSeaMap tiles may rate-limit requests; add tile caching or retry fallbacks.

*This document serves as the definitive reference for all subsequent technical artifacts—Tech Stack, Frontend Guidelines, Backend Structure, App Flow, and more—ensuring the AI-driven development pipeline has no ambiguities.*

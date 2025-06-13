# App Flow Document for Ship Routing Enhancement Proof of Concept

## Onboarding and Sign-In/Sign-Up
When a user opens their web browser and navigates to the application URL, the landing page appears instantly without any need for sign-in or account creation. The page loads a full-screen map view along with input fields and controls alongside the map. There are no login forms, password recovery options, or social sign-up methods, since this proof of concept is open access and meant for immediate use by anyone with the link. The user can simply begin planning a route without encountering any screens or dialogs for authentication.

## Main Dashboard or Home Page
After arriving at the application URL, the user sees the main dashboard. The map dominates most of the screen, displaying OpenStreetMap tiles overlaid by nautical charts from OpenSeaMap. Above or beside the map are labeled input fields for entering origin and destination port codes, optional intermediate port code entries, and a toggle to specify waypoints interactively on the map. Below these fields, action buttons labeled “Calculate Route,” “Download GeoJSON,” and “Refresh Data” are visible. A small status indicator shows when the geospatial database was last updated. In the corner of the map frame, basic zoom and layer toggle controls allow the user to switch between the standard nautical chart and a grayscale base map. From this home page, the user can move seamlessly into any core function of the app by clicking the appropriate button or interacting directly with the map.

## Detailed Feature Flows and Page Transitions

### Specifying a Route
To define a voyage, the user types a UN/LOCODE into the origin field and selects the matching port from the dropdown list. They repeat this for the destination and any intermediate stops. Alternatively, the user can click points directly on the map to place green waypoint markers. Each click is validated against navigable waterway boundaries in the back-end. Invalid clicks outside water bodies trigger an inline warning next to the map.

### Initiating Route Calculation
Once the user is satisfied with the waypoint sequence, they click the “Calculate Route” button. Immediately, a loading spinner appears over the map area. The front-end issues an HTTP request to the Flask back-end with the list of coordinates or port codes. The server then queries PostgreSQL/PostGIS for waterway polygons, bathymetry, and channel data. It may also fetch current AIS vessel positions via the VesselFinder API to overlay live traffic if requested. The enhanced scgraph algorithm runs A* or Dijkstra’s search on the weighted graph, applying land-avoiding constraints and prioritizing inland channels where appropriate. When the computation finishes, the server returns GeoJSON data representing the optimized route.

### Viewing Vessel AIS Data
If the user toggles the AIS overlay before or after route calculation, the application automatically calls the VesselFinder API with the bounding box of the current view. The returned vessel positions are displayed as small ship icons on the map. Clicking a ship icon opens a tooltip showing vessel name, MMSI, speed, and course. This AIS layer can be shown or hidden at any time via a control on the map.

### Visualizing the Computed Path
When route data arrives, Leaflet renders the GeoJSON LineString as a purple polyline over the nautical chart layer. The map view automatically zooms and centers to include the entire route. The user can hover or click on any segment of the polyline to see details such as segment distance, depth constraints, and recommended speed. Waypoint markers are updated with pop-ups that display port codes and coordinates.

### Exporting Route Data
After reviewing the path, the user can click “Download GeoJSON.” The browser initiates a file download containing the route LineString and waypoint features. This file matches exactly the GeoJSON object used for rendering on the map, allowing offline analysis or import into other GIS tools.

### Refreshing Geospatial Data
At any time, the user may click the “Refresh Data” button to pull fresh waterway polygons from OpenSeaMap, updated bathymetry from NOAA, and port/channel updates from global traffic feeds. A progress bar appears beneath the button. In the back-end, a Python script runs the update process and atomically replaces the PostGIS tables. When complete, the status indicator updates with the new timestamp and the user can immediately recalculate routes using the updated data without reloading the page.

## Settings and Account Management
Since this proof of concept does not require user accounts, there are no profile pages or password controls. Instead, the user can adjust application preferences by toggling map layers between the nautical chart and a muted grayscale base map, and by enabling or disabling the AIS vessel overlay. Those controls live persistently on the map, and changes apply instantly. After making adjustments, the user can continue planning, calculating, or exporting routes without ever leaving the main dashboard.

## Error States and Alternate Paths
If the user enters an invalid UN/LOCODE or the typed code does not match any port in the PostGIS table, a red alert bar appears at the top of the interface explaining that the port code is unrecognized. The invalid field is outlined in red, and the user can correct it before proceeding. If a clicked waypoint falls outside valid waterway polygons, a similar inline warning appears next to the map. In cases where the VesselFinder API fails or network connectivity is lost during AIS data fetch, a non-blocking alert notifies the user that the AIS layer is unavailable, while allowing route calculation to continue. If the geospatial data refresh fails, the “Refresh Data” button becomes disabled and a full-width error message prompts the user to retry. In every error scenario, the user is guided back to the normal flow without requiring a page reload.

## Conclusion and Overall App Journey
From the moment the user navigates to the application URL, they are presented with a single, unified interface that requires no sign-up. They specify voyages using port codes or map clicks, then calculate optimized, land-avoiding routes in just a few seconds. Live AIS overlays provide additional context when needed. The calculated path appears instantly as a purple polyline overlaid on a nautical chart, with interactive segment and waypoint details available on demand. Users can download the route data as GeoJSON for offline use and refresh the underlying maritime datasets with a single click. Throughout the experience, intuitive error messages and real-time controls keep the user on track. This flow ensures a seamless journey from route planning to analysis, demonstrating the enhanced routing algorithm’s accuracy, consistency, and performance in a minimal-complexity proof of concept.
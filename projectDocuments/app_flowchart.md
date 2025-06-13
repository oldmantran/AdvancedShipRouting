flowchart TD
    A[User opens application]
    A --> B[Select route input method]
    B --> C{Use port codes}
    C -->|Yes| D[Enter UN LOCODE port codes]
    C -->|No| E[Select waypoints on map]
    D --> F[Validate and fetch port coordinates]
    E --> F
    F --> G[Fetch AIS data from VesselFinder]
    G --> H[Assemble waypoint list]
    H --> I[Call routing engine]
    I --> J[Calculate optimal route avoiding land]
    J --> K[Display route on map with start end and waypoints]
    K --> L[Offer download in GeoJSON format]
    A --> M[Automatic data refresh every 6 hours]
    M --> N[Update geospatial datasets in PostGIS]
    K --> O[Manual data refresh button]
    O --> N
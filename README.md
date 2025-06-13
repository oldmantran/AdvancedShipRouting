# Advanced Ship Routing Enhancement Project v2

A proof-of-concept maritime routing tool that generates accurate, land-avoiding vessel routes using enhanced geospatial data and a robust routing engine.

## Features

- Calculates valid sea and inland waterway routes (e.g., Miami → Belize City → Manzanillo)
- Avoids land and restricted areas using coastal outlines, river/canal polygons, and bathymetry
- Interactive map with OpenStreetMap/Leaflet and nautical overlays
- Live AIS data integration for vessel context
- Downloadable GeoJSON routes
- Automatic and manual maritime dataset refresh

## Tech Stack

- **Backend:** Python 3.11, Flask, scgraph, PostgreSQL/PostGIS, Docker
- **Frontend:** HTML, CSS, JavaScript, Leaflet, OpenStreetMap/OpenSeaMap
- **Deployment:** Docker, AWS ECS Fargate, RDS, Redis, CloudFront

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/oldmantran/AdvancedShipRouting.git
   cd AdvancedShipRouting
   ```

2. **Install Python dependencies:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the backend and frontend**  
   See the project documents for detailed instructions.

## Usage

- Open the app in your browser.
- Enter port codes or select waypoints on the map.
- Calculate and view optimized, land-avoiding routes.
- Download route data as GeoJSON.

## Contributing

Pull requests are welcome! Please see the project documentation for guidelines.

## License

MIT (or specify your chosen license)
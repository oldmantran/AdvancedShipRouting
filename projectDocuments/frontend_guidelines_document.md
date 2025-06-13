# Frontend Guideline Document

This document outlines the frontend setup, architecture, design principles, and technologies used in the Ship Routing Enhancement Project v2. It’s written in everyday language so anyone—technical or not—can understand how the frontend works and why it’s built this way.

## 1. Frontend Architecture

### 1.1 Overview
- **Core Technologies**: Plain HTML/CSS/JavaScript and [Leaflet](https://leafletjs.com/) for interactive maps.
- **Data Flow**: The frontend calls the Flask backend API to request route data (GeoJSON). It then renders that data on a map.
- **Build Tools**: We use a simple bundler setup (e.g., Webpack or Rollup) to bundle, minify, and optimize JavaScript and CSS assets.

### 1.2 Scalability, Maintainability & Performance
- **Modular Code**: JavaScript and CSS are organized by feature (map, forms, UI controls), so adding new features or fixing bugs stays straightforward.
- **Code Splitting**: Heavy libraries like Leaflet and custom map layers are loaded only when the map view initializes, keeping initial page load fast.
- **Caching & CDN**: Static assets (JS, CSS, map tiles) are served via a CDN and cache headers to improve load times.
- **Responsive Design**: The UI scales from desktop to mobile, ensuring the app works everywhere without separate codebases.

## 2. Design Principles

### 2.1 Usability
- **Clear Controls**: Input fields and buttons are labeled and placed logically (e.g., port dropdown above the map). Users immediately know how to add waypoints or refresh data.
- **Feedback**: Actions like drawing a route or refreshing data show a spinner or progress bar.

### 2.2 Accessibility
- **Keyboard Navigable**: All inputs and buttons can be tabbed through. Map popups and controls are reachable via the keyboard.
- **Contrast & Legibility**: Text and interactive elements meet WCAG AA contrast ratios.
- **ARIA Labels**: Form fields and buttons include ARIA attributes where needed.

### 2.3 Responsiveness
- The layout adjusts fluidly from full-screen desktop maps to portrait mobile views.
- Breakpoints: 320px (mobile), 768px (tablet), 1024px (desktop).

## 3. Styling and Theming

### 3.1 Styling Approach
- **Methodology**: We follow BEM (Block, Element, Modifier) naming conventions in our CSS, organized in SCSS files.
- **Preprocessor**: SCSS (SASS) enables variables, nesting, and mixins for consistency.
- **CSS Variables**: Key colors and font sizes are exposed as `:root` variables for easy theming.

### 3.2 Theming & Look-and-Feel
- **Style**: Modern flat design with subtle shadows on controls and a slight glassmorphism effect on popups (semi-transparent backgrounds).
- **Map Layer**: Default OpenStreetMap tiles, with an optional nautical chart overlay from OpenSeaMap. A toggle switch lets users switch to a grayscale base map.

### 3.3 Color Palette
- Primary (Buttons, Highlights): `#E1A141` (Orange-500)
- Secondary (Accents, Icons): `#00FFB2` (Green-Green)
- Background: `#FFFFFF` (White)
- Text Primary: `#08070C` (Black)
- Route Polyline: `#AA84FB` (Purple-500)
- Alert/Warning: `#FF7979` (Red-500)
- Neutral/Borders: `#78777B` (Gray-500)

### 3.4 Typography
- **Primary Font**: Roboto (Google Font)
- **Fallback**: Arial, sans-serif
- **Sizes**: Base 16px, headings scale from 24px to 32px.

## 4. Component Structure

- **MapComponent**: Handles Leaflet initialization, tile layers, route polyline, and waypoint markers.
- **RouteFormComponent**: Port dropdowns (UN/LOCODE), coordinate inputs, and “Add Waypoint” functionality.
- **ControlPanelComponent**: Buttons for Refresh, Toggle Layers, Download GeoJSON.
- **AlertComponent**: Shows warnings or errors (e.g., invalid coordinate).

Each component lives in its own folder with:
```
MapComponent/
  map.js         // logic
  map.scss       // styles
  map.html       // template (or DOM markup via JS)
```
Components communicate via a simple event bus (Pub/Sub) so they remain decoupled.

## 5. State Management

- We use a lightweight **Pub/Sub** pattern in vanilla JavaScript:
  - A central `Store` object holds current route data, waypoint list, and UI flags.
  - Components subscribe to store events (e.g., `routeUpdated`, `waypointAdded`).
  - Actions (like `fetchRoute`) dispatch events to update the store and notify subscribers.
- This keeps state predictable and shared without pulling in a full framework.

## 6. Routing and Navigation

- This is a **single-page app** (SPA) with no frontend URL routing.
- All interaction occurs on one page. Components show/hide themselves or update content dynamically.
- A future version could add hash-based navigation (e.g., `#/settings`) if we split the UI into distinct views.

## 7. Performance Optimization

- **Lazy Loading**: Leaflet and heavy map plugins load only when the map is first displayed.
- **Code Splitting**: Bundler splits vendor code (Leaflet, polyfills) from app code.
- **Minification**: JS and CSS are minified in production builds.
- **Image & SVG Sprites**: Icons are combined into SVG sprites to reduce HTTP requests.
- **Caching**: Service Worker caches static assets for instant repeat loads.
- **Spatial Indexing**: Though on the backend, fast PostGIS queries help the frontend receive data under 2 seconds.

## 8. Testing and Quality Assurance

### 8.1 Automated Testing
- **Unit Tests**: Jest + jsdom for testing core JS modules (Store, Map logic, Form validation).
- **Integration Tests**: Test interactions between components using Jest or Mocha.
- **E2E Tests**: Cypress runs browser-based tests: drawing a route, adding waypoints, and downloading GeoJSON.

### 8.2 Linting & Formatting
- **ESLint**: Enforces consistent JS style and catches errors.
- **Stylelint**: Checks SCSS for consistency and prevents common mistakes.
- **Prettier**: Auto-formats code on save.

### 8.3 CI/CD
- On each commit, GitHub Actions runs linting, unit tests, and build checks.
- Docker container is built to ensure the frontend bundles without errors.

## 9. Conclusion and Overall Frontend Summary

This frontend setup uses familiar web technologies—HTML, CSS (SCSS), and JavaScript—enhanced by Leaflet for interactive mapping. We follow clear design principles (usability, accessibility, responsiveness) and a modular, component-based architecture for easy maintenance and scaling. Performance is tuned with lazy loading, caching, and code splitting. Quality is safeguarded through testing, linting, and CI/CD.

By following these guidelines, any developer or stakeholder can understand how to extend, maintain, and deploy the Ship Routing Enhancement Project frontend with confidence.
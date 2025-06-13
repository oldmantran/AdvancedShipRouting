from flask import Blueprint, jsonify, request
from .models import db, Port, Route
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

main = Blueprint('main', __name__)

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@main.route('/ports', methods=['GET'])
def get_ports():
    ports = Port.query.all()
    result = []
    for port in ports:
        geom = to_shape(port.location)
        result.append({
            'id': port.id,
            'name': port.name,
            'locode': port.locode,
            'location': mapping(geom)
        })
    return jsonify(result)

@main.route('/ports', methods=['POST'])
def add_port():
    data = request.get_json()
    name = data.get('name')
    locode = data.get('locode')
    lon = data.get('lon')
    lat = data.get('lat')
    if not all([name, locode, lon, lat]):
        return jsonify({'error': 'Missing data'}), 400
    wkt = f'POINT({lon} {lat})'
    port = Port(name=name, locode=locode, location=wkt)
    db.session.add(port)
    db.session.commit()
    return jsonify({'message': 'Port added', 'id': port.id}), 201

@main.route('/routes', methods=['GET'])
def get_routes():
    routes = Route.query.all()
    result = []
    for route in routes:
        geom = to_shape(route.path)
        result.append({
            'id': route.id,
            'name': route.name,
            'path': mapping(geom)
        })
    return jsonify(result)

@main.route('/routes', methods=['POST'])
def add_route():
    data = request.get_json()
    name = data.get('name')
    coordinates = data.get('coordinates')  # Expecting a list of [lon, lat] pairs
    if not name or not coordinates or not isinstance(coordinates, list):
        return jsonify({'error': 'Missing or invalid data'}), 400
    coord_str = ', '.join([f"{lon} {lat}" for lon, lat in coordinates])
    wkt = f'LINESTRING({coord_str})'
    route = Route(name=name, path=wkt)
    db.session.add(route)
    db.session.commit()
    return jsonify({'message': 'Route added', 'id': route.id}), 201
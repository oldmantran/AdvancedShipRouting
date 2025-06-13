from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

db = SQLAlchemy()

class Port(db.Model):
    __tablename__ = 'ports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    locode = db.Column(db.String(10), unique=True, nullable=False)
    location = db.Column(Geometry('POINT'), nullable=False)

class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    path = db.Column(Geometry('LINESTRING'), nullable=False)
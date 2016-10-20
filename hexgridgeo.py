# coding=utf-8
from abc import ABCMeta, abstractmethod
from collections import namedtuple
import math

import hexgrid

EARTH_CIRCUMFERENCE = 40075016.685578488
EARTH_METERS_PER_DEGREE = 111319.49079327358

PI = math.pi

Point = namedtuple('Point', ['lon', 'lat'])


class ProjectionNoOp(object):

    @staticmethod
    def to_point(geopoint):
        # type: (Point) -> hexgrid.Point
        return hexgrid.Point(geopoint.lon, geopoint.lat)

    @staticmethod
    def to_geopoint(point):
        # type: (hexgrid.Point) -> Point
        return Point(point.x, point.y)


class ProjectionSin(object):

    @staticmethod
    def to_point(geopoint):
        # type: (Point) -> hexgrid.Point
        lambd = (geopoint.lon + 180) * (PI / 180)
        phi = geopoint.lat * (PI / 180)
        x = (lambd * math.cos(phi)) * ((EARTH_CIRCUMFERENCE / 2) / PI)
        y = phi * ((EARTH_CIRCUMFERENCE / 2) / PI)
        return hexgrid.Point(x, y)

    @staticmethod
    def to_geopoint(point):
        # type: (hexgrid.Point) -> Point
        phi = point.y / ((EARTH_CIRCUMFERENCE / 2) / PI)
        lambd = point.x / (math.cos(phi) * ((EARTH_CIRCUMFERENCE / 2) / PI))
        lon = (lambd / (PI / 180)) - 180
        lat = phi / (PI / 180)
        return Point(lon, lat)


class ProjectionAEP(object):

    @staticmethod
    def to_point(geopoint):
        # type: (Point) -> hexgrid.Point
        theta = geopoint.lon * (PI / 180)
        rho = PI/2 - (geopoint.lat * (PI / 180))
        x = rho * math.sin(theta)
        y = -rho * math.cos(theta)
        return hexgrid.Point(x, y)

    @staticmethod
    def to_geopoint(point):
        # type: (hexgrid.Point) -> Point
        theta = math.atan2(point.x, -point.y)
        rho = point.x / math.sin(theta)
        lat = (PI/2 - rho) / (PI/180)
        lon = theta / (PI / 180)
        return Point(lon, lat)


class ProjectionSM(object):

    @staticmethod
    def to_point(geopoint):
        # type: (Point) -> hexgrid.Point
        latR = geopoint.lat * (PI / 180)
        x = geopoint.lon * EARTH_METERS_PER_DEGREE
        y = math.log(math.tan(latR) + (1 / math.cos(latR)))
        y = (y / PI) * (EARTH_CIRCUMFERENCE / 2)
        return hexgrid.Point(x, y)

    @staticmethod
    def to_geopoint(point):
        # type: (hexgrid.Point) -> Point
        lon = point.x / EARTH_METERS_PER_DEGREE
        lat = math.asin(math.tanh((point.y / (EARTH_CIRCUMFERENCE / 2)) * PI))
        lat = lat * (180 / PI)
        return Point(lon, lat)


class Grid(namedtuple('Grid', ['hexgrid', 'projection'])):

    def __new__(cls, orientation, size, projection=None):
        projection = projection or ProjectionSM
        grid = hexgrid.Grid(orientation, hexgrid.Point(0, 0), size)
        return super(Grid, cls).__new__(cls, grid, projection)

    def hex_to_code(self, hex):
        # type: (hexgrid.Hex) -> int
        return self.hexgrid.hex_to_code(hex)

    def hex_from_code(self, code):
        # type: (int) -> hexgrid.Hex
        return self.hexgrid.hex_from_code(code)

    def hex_at(self, geopoint):
        # type: (Point) -> hexgrid.Hex
        point = self.projection.to_point(geopoint)
        return self.hexgrid.hex_at(point)

    def hex_center(self, hex):
        # type: (hexgrid.Hex) -> Point
        point = self.hexgrid.hex_center(hex)
        return self.projection.to_geopoint(point)

    def hex_corners(self, hex):
        # type: (hexgrid.Hex) -> list
        corners = self.hexgrid.hex_corners(hex)
        return [self.projection.to_geopoint(p) for p in corners]

    def hex_neighbors(self, hex, layers):
        # type: (hexgrid.Hex, int) -> list
        return self.hexgrid.hex_neighbors(hex)

    def make_region(self, geometry):
        # type: (list) -> hexgrid.Region
        points = [self.projection.to_point(p) for p in geometry]
        return self.hexgrid.make_region(points)

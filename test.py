import unittest
import logging
import hexgrid

from hexgridgeo import (
    Point,
    ProjectionNoOp,
    ProjectionSin,
    ProjectionAEP,
    ProjectionSM,
    Grid
)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestHexgridGeo(unittest.TestCase):

    def assertPointEqual(self, e, r, precision):
        if(abs(e.x-r.x) > precision or abs(e.y - r.y) > precision):
            self.fail("{} != {}".format(e, r))

    def assertGeoPointEqual(self, e, r, precision):
        if(abs(e.lon-r.lon) > precision or abs(e.lat - r.lat) > precision):
            self.fail("{} != {}".format(e, r))

    def test_projection_NoOp(self):
        geopoint = Point(-73.0, 40.0)
        point = ProjectionNoOp.to_point(geopoint)
        self.assertPointEqual(
            hexgrid.Point(-73.0, 40.0), point, 0.00001)
        recoded_geopoint = ProjectionNoOp.to_geopoint(point)
        self.assertGeoPointEqual(geopoint, recoded_geopoint, 0.00001)

    def test_projection_Sin(self):
        geopoint = Point(-73.0, 40.0)
        point = ProjectionSin.to_point(geopoint)
        self.assertPointEqual(
            hexgrid.Point(9124497.47463, 4452779.63173), point, 0.00001)
        recoded_geopoint = ProjectionSin.to_geopoint(point)
        self.assertGeoPointEqual(geopoint, recoded_geopoint, 0.00001)

    def test_projection_AEP(self):
        geopoint = Point(-73.0, 40.0)
        point = ProjectionAEP.to_point(geopoint)
        self.assertPointEqual(
            hexgrid.Point(-0.83453, -0.25514), point, 0.00001)
        recoded_geopoint = ProjectionAEP.to_geopoint(point)
        self.assertGeoPointEqual(geopoint, recoded_geopoint, 0.00001)

    def test_projection_SM(self):
        geopoint = Point(-73.0, 40)
        point = ProjectionSM.to_point(geopoint)
        self.assertPointEqual(
            hexgrid.Point(-8126322.82791, 4865942.27950), point, 0.00001)
        recoded_geopoint = ProjectionSM.to_geopoint(point)
        self.assertGeoPointEqual(geopoint, recoded_geopoint, 0.00001)

    def test_simple(self):
        grid = Grid(
            hexgrid.OrientationFlat,
            hexgrid.Point(500, 500),
            ProjectionSM)
        corners = grid.hex_corners(grid.hex_at(Point(-73.0, 40.0)))
        expected_corners = [
            Point(-72.99485, 39.99877), Point(-72.99710, 40.00175),
            Point(-73.00159, 40.00175), Point(-73.00384, 39.99877),
            Point(-73.00159, 39.99579), Point(-72.99710, 39.99579)
        ]
        for expected_corner, corner in zip(expected_corners, corners):
            self.assertGeoPointEqual(expected_corner, corner, 0.00001)

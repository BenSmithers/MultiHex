import unittest

from MultiHex.core import Hex, Point

from math import sqrt
rthree = sqrt(3)

class TestPoints(unittest.TestCase):

    def test_constructor(self):

        with self.assertRaises(TypeError):
            new = Hex( 1. , 1.)

        with self.assertRaises(TypeError):
            new = Hex(Point(1.0,1.0), "failure")

    def test_access(self):
        center = Point(5.,7.)
        radius = 3.5

        ex = Hex(center, radius)

        self.assertTrue( ex.radius == radius)
        self.assertTrue( ex.center == ex.center)

    def test_vertices(self):
        center = Point(5.,7.)
        radius = 3.5

        ex = Hex(center, radius)

        verts = ex.vertices
        self.assertTrue( verts[0] == center+Point( -0.5, 0.5*rthree)*radius )
        self.assertTrue( verts[1] == center+Point(  0.5, 0.5*rthree)*radius )
        self.assertTrue( verts[2] == center+Point(  1.0, 0.0)*radius )
        self.assertTrue( verts[3] == center+Point(  0.5,-0.5*rthree)*radius )
        self.assertTrue( verts[4] == center+Point( -0.5,-0.5*rthree)*radius )
        self.assertTrue( verts[5] == center+Point( -1.0, 0.0)*radius )
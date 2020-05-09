import unittest

from MultiHex.core import Point, Hex
from MultiHex.core import Hexmap, construct_id, deconstruct_id 

from math import sqrt, pi
rthree = sqrt(3.)

class TestPoints(unittest.TestCase):
    def test_constructor(self):
        new = Hexmap()

    def test_con_decon(self):
        base_x = 10
        base_y = 15
        main = True

        other_x, other_y, other_main = deconstruct_id( construct_id( base_x, base_y, main))
        self.assertTrue( base_x == other_x )
        self.assertTrue( base_y == other_y )
        self.assertTrue( main == other_main )

    def test_get_id_get_point(self):
        main = Hexmap()
        radius = main.drawscale
        diag = radius*rthree/2.

        which = Point(5.*radius,10.*radius)

        with self.assertRaises(TypeError):
            main.get_id_from_point( 5 )

        # We want to make sure the get_id function works for a few cases
        which_id = main.get_id_from_point( Point( 3*radius, 0.) )
        constructed = construct_id(1, 0, True)
        self.assertTrue( constructed == which_id )

        # up a few hexes
        which_id = main.get_id_from_point( Point( 0., 4*diag) )
        constructed = construct_id(0,2, True)
        self.assertTrue( constructed == which_id )

        # up and right some
        which_id = main.get_id_from_point( Point( 3*radius, 4*diag) )
        constructed = construct_id(1,2, True)
        self.assertTrue( constructed == which_id )

        # up and right some
        where = Point( 1.5*radius, 3*diag) 
        which_id = main.get_id_from_point( where )
        constructed = construct_id(0,1, False)
        self.assertTrue( constructed == which_id )
        self.assertTrue( where == main.get_point_from_id( which_id ) )

    def test_register(self):
        main = Hexmap()
        radius = main.drawscale
        diag = radius*rthree/2.
        where = Point( 3*radius, 4*diag) 
        this_id = main.get_id_from_point(where)
        this_hex = Hex(where, radius)

        with self.assertRaises(TypeError):
            main.register_hex( 5, this_id)
        with self.assertRaises(TypeError):
            main.register_hex(this_hex, "")
        with self.assertRaises(AssertionError):
            bad_hex = Hex(where, radius/2.)
            main.register_hex(bad_hex, this_id)

        main.register_hex( this_hex, this_id )
        self.assertTrue( this_hex == main.catalogue[this_id] )



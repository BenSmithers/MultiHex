
import unittest


from MultiHex.core import Point, Point3d
from math import sqrt, pi
class TestPoints(unittest.TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            new = Point("test", 2)
        with self.assertRaises(TypeError):
            new = Point(2, "Test")

    def test_equals(self):
        self.assertTrue( Point(2.,2.) == Point(2, 2) )
        self.assertTrue( Point3d(2.,2.,2.) == Point3d(2, 2, 2.) )

        self.assertFalse( Point(2.,2.5) == Point(2, 2) )
        self.assertFalse( Point(2.5,2) == Point(2, 2) )
        self.assertFalse( Point(1.9,2.7) == Point(2, 2) )

        self.assertFalse( Point3d(2.,2.,2.5) == Point3d(2, 2, 2.) )
        self.assertFalse( Point3d(2.5,2.,2.) == Point3d(2, 2, 2.) )
        self.assertFalse( Point3d(2.,2.5,2.) == Point3d(2, 2, 2.) )

        self.assertFalse( Point3d(2.1,2.,2.7) == Point3d(2, 2, 2.) )
        self.assertFalse( Point3d(2.4,2.3,2.) == Point3d(2, 2, 2.) )
        self.assertFalse( Point3d(2.,2.1,2.9) == Point3d(2, 2, 2.) )

        self.assertFalse( Point3d(12,0.6,1.2) == Point3d(2, 2, 2.) )

    def test_add(self):
        new = Point( 1,1 ) + Point( 4,7)
        self.assertEqual( new, Point( 5, 8) )

        new = Point3d( 1, 1, 1) + Point3d( 4,7,6)
        self.assertEqual( new , Point3d( 5, 8, 7) )

    def test_subtract( self ):
        new = Point( 2., 2.) - Point( 0., 1.)
        self.assertAlmostEqual( new, Point( 2., 1.))

        new = Point3d( 1, 1, 1) - Point3d( 4,7,6)
        self.assertEqual( new , Point3d( -3, -6, -5) )

    def test_pow( self ):
        value =  Point( 2., 2.)**2.5
        self.assertAlmostEquals( value, 2*(2**2.5))

        value =  Point3d( 2., 2., 2.)**2.5
        self.assertAlmostEquals( value, 3*(2.**2.5))


    def test_magnitude(self):
        new = Point( sqrt(2), sqrt(2) )
        self.assertAlmostEqual(new.magnitude, 2.)

        new = Point3d( sqrt(2), sqrt(2) , sqrt(2))
        self.assertAlmostEqual(new.magnitude, sqrt(3*2))

    def test_normalize(self):
        new = Point( 5.0, 1)
        new.normalize()
        self.assertAlmostEqual( 1.0, new.magnitude)

    def test_dot(self):
        value = Point(1., 0.)*Point(0, 1)
        self.assertEqual( value, 0)
        value = Point3d(1., 0., 2)*Point3d(0, 1, 2.5)
        self.assertEqual( value, 5)

        new = Point( 3.5, 2.5)*2
        self.assertAlmostEquals( new, Point( 7., 5.) )
        new = Point3d( 3.5, 2.5,1.5)*2
        self.assertAlmostEquals(new, Point3d( 7., 5., 3.) )

if __name__ == '__main__':
    unittest.main(verbosity=2)
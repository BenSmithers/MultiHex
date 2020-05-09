import unittest

from MultiHex.core import Point, Path
from math import sqrt, pi

class TestPath(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(TypeError):
            new = Path( 5 )
    
    def test_trim(self):
        # build the path to test
        first = Point(0.0,0.0)
        second = Point(1.0,0.0)
        third = Point(2.0,0.0)
        fourth = Point(3.0,0.0)
        new = Path(first)
        new.add_to_end(second)
        new.add_to_end(third)
        new.add_to_end(fourth)

        # check args
        with self.assertRaises(TypeError):
            new.trim_at("")
        with self.assertRaises(TypeError):
            new.trim_at(0, 5)
        with self.assertRaises(ValueError):
            new.trim_at(Point(3.0,3.0))
        with self.assertRaises(ValueError):
            new.trim_at(17)

        new.trim_at(2, True) # keeping lower 
        print(len(new.vertices))
        self.assertTrue(len(new.vertices) == 2)
        self.assertTrue(new.end() == second)
        self.assertTrue(new.start() == first)

        # add them back on...
        new.add_to_end(third)
        new.add_to_end(fourth)

        new.trim_at(2, False) # keeping upper 
        print(len(new.vertices))
        self.assertTrue(len(new.vertices) == 2)
        self.assertTrue(new.end() == fourth)
        self.assertTrue(new.start() == third)


    def test_access(self):
        # build the Path
        first = Point(0.0,0.0)
        second = Point(1.0,0.0)
        third = Point(2.0,0.0)
        fourth = Point(3.0,0.0)
        new = Path(first)
        new.add_to_end(second)
        new.add_to_end(third)
        new.add_to_end(fourth)

        self.assertTrue( new.end() == fourth )
        self.assertTrue( new.start() == first )

        with self.assertRaises(TypeError):
            new.end("")
        with self.assertRaises(TypeError):
            new.start("")

        self.assertTrue( new.end(1) == third )
        self.assertTrue( new.start(1) == second )

    def test_add_to(self):
        first = Point(0.0,0.0)
        second = Point(1.0,0.0)
        third_bad = Point(2.0,1.0)
        third = Point(2.0,0.0)

        new = Path(first)
        with self.assertRaises(TypeError):
            new.add_to_end(5)

        new.add_to_end(second)
        with self.assertRaises(ValueError):
            new.add_to_end(third_bad) 
        
        new = None
        new = Path(first)
        with self.assertRaises(TypeError):
            new.add_to_start(5)

        new.add_to_start(second)
        with self.assertRaises(ValueError):
            new.add_to_start(third_bad) 

        
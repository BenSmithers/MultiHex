from hex import Hex
from point import Point

default_p = Point(0.0,0.0)

class Ocean(Hex):
    def __init__(self, center=default_p, radius=1.0 ):
        Hex.__init__(self, center, radius)
        self.fill = 'powderblue'
        self._temperature_base = 0.5
        self._humidity_base    = 1.0
        self._altitude_base    = 0.0
        self._is_land          = False
        

class Grassland(Hex):
    def __init__(self, center=default_p, radius=1.0 ):
        Hex.__init__(self, center, radius )
        self.fill = 'green3'
    

class Forest(Hex):
    def __init__(self, center=default_p, radius=1.0 ):
        Hex.__init__(self, center, radius )
        self.fill = 'forest green'
    

class Mountain(Hex):
    def __init__(self, center=default_p, radius=1.0 ):
        Hex.__init__(self, center, radius )
        self.fill = 'thistle4'
    

class Arctic(Hex):
    def __init__(self, center=default_p, radius=1.0 ):
        Hex.__init__(self, center, radius )
        self.fill = 'snow'
        self._temperature_base = 0.0
        self._humidity_base    = 0.0
        self._altitude_base    = 0.0
        self._is_land          = True
    

class Desert(Hex):
    def __init__(self, center=default_p, radius=1.0 ):
        Hex.__init__(self, center, radius )
        self.fill = 'goldenrod'
        self._temperature_base = 1.0
        self._humidity_base    = 0.0
        self._altitude_base    = 0.0
        self._is_land          = True




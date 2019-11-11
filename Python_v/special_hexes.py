from hex import Hex

class Overland(Hex):
    pass

class Ocean(Hex):
    self._temperature_base = 0.5
    self._humidity_base    = 1.0
    self._altitude_base    = 0.0
    self._is_land          = False
    pass

class Grassland(Hex):
    pass

class Forest(Hex):
    pass

class Mountain(Hex):
    pass

class Arctic(Hex):
    self._temperature_base = 0.0
    self._humidity_base    = 0.0
    self._altitude_base    = 0.0
    self._is_land          = True
    pass

class Desert(Hex):
    self._temperature_base = 1.0
    self._humidity_base    = 0.0
    self._altitude_base    = 0.0
    self._is_land          = True
    pass



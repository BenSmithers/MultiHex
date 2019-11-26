import MultiHex.point as point
import numpy as np

default_p = point.Point(0.0,0.0)
rthree = np.sqrt(3)

class Hex:
    """
    Datastructure to represent a single hex on a hex map

    @ build_name            - creates a name for hex biome - not implemented
    @ rescale_color         - recalculates the color based off of the current color and altitude
    """
    def __init__(self, center=default_p, radius=1.0 ):
        self._center = center
        self._radius = radius
        
#        self.id     = 1
        self.outline= (240,240,240)
        self.fill   = (100,100,100) 
        self._vertices = [ center for i in range(6) ]

        self._biodiversity     = 1.0
        self._rainfall_base    = 0.0
        self._altitude_base    = 1.0
        self._temperature_base = 1.0
        self._is_land          = True
        self.coastal           = False
        self.hex_edge          = False
        
        # used in procedural generation
        self.genkey            = '00000000'
        # 0 - ridgeline
        # 1 - mountain 
        # 2 - alive / dead 
        # 3 - dry / wet 
        # 4 - 
        # 5 - hot / cold
        # 6 - island
        # 7 - ocean


        self._vertices[0] = self._center + point.Point( -0.5, 0.5*rthree)*self._radius
        self._vertices[1] = self._center + point.Point(  0.5, 0.5*rthree)*self._radius
        self._vertices[2] = self._center + point.Point(  1.0, 0.0)*self._radius
        self._vertices[3] = self._center + point.Point(  0.5,-0.5*rthree)*self._radius
        self._vertices[4] = self._center + point.Point( -0.5,-0.5*rthree)*self._radius
        self._vertices[5] = self._center + point.Point( -1.0, 0.0)*self._radius

    def build_name(self):
        return("")
    def reset_color(self):
        pass

    def rescale_color(self):
        self.fill  = (min( 255, max( 0, self.fill[0]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[1]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[2]*( 1.0 + 0.4*(self._altitude_base) -0.2))))
             
   
    def __repr__(self):
        return("{}@{}".format(self.__clas__, self.id))

    
   

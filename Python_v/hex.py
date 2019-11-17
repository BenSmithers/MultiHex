import point 
import numpy as np

default_p = point.Point(0.0,0.0)
rthree = np.sqrt(3)

class Hex:
    """
    Datastructure to represent a single hex on a hex map

    @ build_name            - creates a name for hex biome
    @ get_flattened_points  - returns vertices in flattened list [x1 , y1, x2, ... ]
    """
    def __init__(self, center=default_p, radius=1.0 ):
        self._center = center
        self._radius = radius
        
#        self.id     = 1
        self.outline= (240,240,240)
        self.fill   = (100,100,100) 
        self._vertices = [ center for i in range(6) ]

        self._biodiversity     = 1.0
        self._humidity_base    = 1.0
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
    
    def get_flattened_points(self, displacement=None, zoom=1.0):
        """
        deprecated

        functionality moved up to hexmap.py
        """
        flat = []
        if displacement is None:
            for obj in self._vertices:
                flat+=[ obj.x*zoom, obj.y*zoom ]
        else:
            for obj in self._vertices:
                flat+=[ (obj.x + displacement.x)*zoom , (obj.y + displacement.y)*zoom ]
        return(flat)
              
   
    def __repr__(self):
        return("{}@{}".format(self.__clas__, self.id))

    
   

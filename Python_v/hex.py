import point 
import numpy as np

default_p = point.Point(0.0,0.0)
rthree = np.sqrt(3)

class Hex:
    """
    Datastructure to represent a single hex on a hex map
    """
    def __init__(self, center=default_p, radius=1.0 ):
        self._center = center
        self._radius = radius
        
#        self.id     = 1
        self.outline= '#ddd'
        self.fill   = '#05f' 
        self._vertices = [ center for i in range(6) ]

        self._temperature_base = 1.0
        self._humidity_base    = 1.0
        self._altitude_base    = 1.0
        self._is_land          = True

        self._vertices[0] = self._center + point.Point( -0.5, 0.5*rthree)*self._radius
        self._vertices[1] = self._center + point.Point(  0.5, 0.5*rthree)*self._radius
        self._vertices[2] = self._center + point.Point(  1.0, 0.0)*self._radius
        self._vertices[3] = self._center + point.Point(  0.5,-0.5*rthree)*self._radius
        self._vertices[4] = self._center + point.Point( -0.5,-0.5*rthree)*self._radius
        self._vertices[5] = self._center + point.Point( -1.0, 0.0)*self._radius

    def translate(self, vector):
        self._center += vector
        for vertex in self._vertices:
            vertex += vector 

    
    def get_flattened_points(self, displacement=None, zoom=1.0):
        flat = []
        if displacement is None:
            for obj in self._vertices:
                flat+=[ obj.x*zoom, obj.y*zoom ]
        else:
            for obj in self._vertices:
                flat+=[ (obj.x + displacement.x)*zoom , (obj.y + displacement.y)*zoom ]
        return(flat)
            
    
    @classmethod
    def _transformed_point(cls, unt_point ):
        new_point = point.Point( unt_point.x/rthree, unt_point.y - (unt_point.x/rthree))
        return( new_point )
    
    def __repr__(self):
        return("{}@{}".format(self.__clas__, self.id))

    
   

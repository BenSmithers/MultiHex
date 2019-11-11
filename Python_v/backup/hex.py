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
        
        self.id     = 1
        self.outline= '#ddd'
        self.fill   = '#05f' 
        self._vertices = [ center for i in range(6) ]

        self._selected = False

        self._vertices[0] = self._center + point.Point( -0.5, 0.5*rthree)*self._radius
        self._vertices[1] = self._center + point.Point(  0.5, 0.5*rthree)*self._radius
        self._vertices[2] = self._center + point.Point(  1.0, 0.0)*self._radius
        self._vertices[3] = self._center + point.Point(  0.5,-0.5*rthree)*self._radius
        self._vertices[4] = self._center + point.Point( -0.5,-0.5*rthree)*self._radius
        self._vertices[5] = self._center + point.Point( -1.0, 0.0)*self._radius
    

        _transformed = self._transformed_point( self._center )
        idx = int( np.floor( rthree*( _transformed.x/self._radius ) +0.5 ))
        idy = int( np.floor( rthree*( _transformed.y/self._radius ) +0.5 ))
        
        x_bitstr = '{0:032b}'.format(idx)
        y_bitstr = '{0:032b}'.format(idy)

        # if the number is negative, set the leading bit to a '1' to note that
        if x_bitstr[0]=='-':
            x_bitstr ='1' + x_bitstr[1:]
        if y_bitstr[0]=='-':
            y_bitstr ='1' + y_bitstr[1:]

        self.id = int( x_bitstr + y_bitstr, 2)
    
    def get_flattened_points(self):
        flat = []
        for object in self._vertices:
            flat+=[ object.x, object.y ]
        return(flat)
            
    
    @classmethod
    def _transformed_point(cls, unt_point ):
        new_point = point.Point( unt_point.x/rthree, unt_point.y - (unt_point.x/rthree))
        return( new_point )
    
    def __repr__(self):
        return("{}@".format(self.__clas__, self.id))

    
   

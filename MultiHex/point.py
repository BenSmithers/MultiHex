try:
    from numpy import sqrt, atan, pi
except ImportError:
    from math import sqrt, atan, pi

def is_number(object):
    try:
        a= 5+object
        return(True)
    except TypeError:
        return(False)

class Point:
    """
    A vector in 2D Cartesian space.

    @x          - x component of vector
    @y          - y component of vector
    @magnitude  - length of this vector
    """
    def __init__(self, ex =0.0, why=0.0):
        # do the thing
        self.x = ex
        self.y = why
        
        # use the bool so that we only have to calculate the magnitude once 
        self._mcalculated   = False
        self._magnitude     = 0.0
        
        self._acalculated   = False
        self._angle         = 0.0

    def __add__(self, obj):
        """
        Used to add a point to another one through vector addition 
        """
        if (obj.__class__!=self.__class__):
            raise TypeError("Cannot add type {} to Point object".format(obj.__class__)) 
        new = Point( self.x + obj.x, self.y + obj.y)
        return( new )
    def __sub__(self, obj):
        """
        Same as addition, but for subtraction
        """
        if (obj.__class__!=self.__class__):
            raise TypeError("Cannot subtract type {} from Point object".format(obj.__class__)) 
        new = Point( self.x - obj.x, self.y - obj.y)
        return( new )
    def __mul__(self, obj):
        """
        Calculate the inner product of two vector-points, or scale one vector-point by a scalar. 
        """
        if is_number(obj):
            return( Point( self.x*obj, self.y*obj ))
        elif obj.__class__==self.__class__:
            return( self.x*obj.x + self.y*obj.y )
        else:
            raise TypeError("Cannot multiply type {} with Point object".format(obj.__class__))
    def __eq__(self, obj):
        return( abs(self.x-obj.x)<0.01  and abs(self.y-obj.y)<0.01 )
    def __truediv__(self, obj):
        if not is_number(obj):
            raise TypeError("Cannot divide Point by object of type '{}'".format(type(obj)))
        else:
            return( Point( self.x/obj, self.y/obj ) )
    
    def __pow__(self, obj):
        if not is_number(obj):
            raise TypeError("Cannot raise vector to a non-number power")
        else:
            # returns a scalar! 
            return( self.x**obj + self.y**obj )

    @property
    def magnitude(cls):
        """
        Return the magnitude of the vector. If it hasn't been calculated, calculate it.
        """
        if cls._mcalculated:
            return( cls._magnitude )
        else:
            cls._magnitude = sqrt( cls.x**2 + cls.y**2 )
            cls._mcalculated = True
            return(cls._magnitude)
    
    @property
    def angle(cls):
        """
        returns the angle of the vector as measured from the x-axis. Calculates only once
        """
        if cls._acalculated:
            return( cls._angle )
        else:
            cls._acalculated = True
            prelim_angle = atan( cls.y / cls.x )

            if cls.y<0 and cls.x<0:
                prelim_angle += pi
            elif cls.y<0 and cls.x >0:
                prelim_angle += 2*pi
            elif cls.y>0 and cls.x<0:
                prelim_angle += pi
            else:
                # angle is in Quadrant I, this is fine
                pass
            cls._angle = prelim_angle 
            

    # casting this object as a string 
    def __str__(self):
        return( "({},{})".format( self.x, self.y ) )
    
    def __repr__(self):
        return("Point({},{})".format(self.x,self.y))
        

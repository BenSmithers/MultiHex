from point import Point
from hex import Hex
from numpy import sqrt, floor

rthree = sqrt(3)
def transform_x(pos_x, pos_y=0.0):
    return( pos_x/rthree )
def transform_y(pos_x, pos_y):
    return( pos_y - pos_x/rthree)

class Hexmap:
    """
    Object to maintain the whole hex catalogue, draw the hexes, etc...
    """
    def __init__(self):
        # public
        self.catalogue = {}
        
        #private 
        self._drawscale = 10.0
        self._active_id = 1
        
        self._draw_relative_to = Point(0.0,0.0)
    
    def register_hex(self, target_hex ):
        if target_hex.id in self.catalogue:
            raise NameError("A hex with ID {} is already registered")
        else:
            self.catalogue[target_hex.id] = target_hex
    
    def set_active_hex(self, id):
        self.catalogue[self._active_id].outline = '#05f'
        self._active_id = id
        self.catalogue[self._active_id].outline = '#f00'
    
    
    
    def get_id_from_point(self, pos_x, pos_y):
        # transform the point into the new coordinate system used to number hexes
        trans_x = transform_x( pos_x, pos_y )
        trans_y = transform_y( pos_x, pos_y )
        
        # calculate a "BaseID" derived from the geometric tiling of the hexes
        base_idx = 2*int(floor( trans_x/(2*rthree*self._drawscale)))
        base_idy =   int(floor( trans_y/(  rthree*self._drawscale)))
#        base_idx  = int(2*( trans_x % (3*self._drawscale)))
#        base_idy  = int(trans_y % (self._drawscale*rthree))
    

        # Find the offset from that BaseID location
        rel_y   = pos_y % (rthree*self._drawscale)
        rel_x   = pos_x % (2*self._drawscale)
        
        #by comparing the offset location relative to various border's lines, we can determine by how much we need to offset the basd ID
        line_h  = rel_y > (rthree*self._drawscale)*0.5
        line_p  = rel_y > rthree*rel_x
        line_n  = rel_y > (-1*rthree*rel_x +self._drawscale*rthree)
        line_n2 = rel_y > (-1*rthree*rel_x +3*self._drawscale*rthree)
        line_p2 = rel_y > (rthree*rel_x -2*self._drawscale*rthree)
        
        if line_h:
            if line_p:
                base_idy += 1
            else:
                base_idx += 1
                if line_n2:
                    base_idx += 1
        else:
            if line_n:
                base_idx +=1 
                if not line_p2:
                    base_idx+=1
                    base_idy-=1
        
        x_bitstr = '{0:032b}'.format(base_idx)
        y_bitstr = '{0:032b}'.format(base_idy)
        # this method puts a '-' sign in the leading character if this is a negative number 

        # if the number is negative, set the leading bit to a '1' to note that
        if x_bitstr[0]=='-':
            x_bitstr = '1' + x_bitstr[1:]
        if y_bitstr[0]=='-':
            y_bitstr = '1' + y_bitstr[1:]
        return( int( x_bitstr + y_bitstr, 2) )
    
    def get_point_from_id(self, id):
        # convert the id to a bit string
        bitstring = '{0:064b}'.format( id )
        # split the bit string in half, and reconvert these to integers 
        # I'm using the first bit to note +/- (0/1) sign
        idx = int(bitstring[1:32],  2)
        if bitstring[0]=='1':
            idx = -1*idx
        idy = int(bitstring[33:64], 2)
        if bitstring[32]=='1':
            idy = -1*idy 
        
        x_coord = 2*idx*self._drawscale*rthree
        y_coord = 2*idy*self._drawscale + x_coord/rthree
        return(Point( x_coord, y_coord))
                  

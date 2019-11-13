from point import Point #fundamental point, allows vector algegbra
from hex import Hex #your standard hexagon. Holds all the metadata
from special_hexes import *

# prefer to import the numpy functions since they are faster,
# but if the user doesn't have them installed let's just use the math ones 
# these are both needed to handle the geometry 
try:
    from numpy import sqrt, floor 
except ImportError:
    from math import sqrt, floor

"""
Ben Smithers
b.smithers.actual@gmail.com 

Implements the hexmap class
"""

# calculate this once, save it to the global scope! 
rthree = sqrt(3)
def transform_x(pos_x, pos_y=0.0):
    return( pos_x/rthree )
def transform_y(pos_x, pos_y):
    return( pos_y - pos_x/rthree)

class Hexmap:
    """
    Object to maintain the whole hex catalogue, draw the hexes, registers the hexes
    """
    def __init__(self):
        self.catalogue = {}
        
        self._drawscale = 15.0
        self._zoom      = 1.0
        self._active_id = None
        self._party_hex = None
        self._outline   = None

        self.draw_relative_to = Point(0.0,0.0)
    def remove_hex( self, target_id):
        try:
            del self.catalogue[target_id]
        except KeyError:
            pass

    def register_hex(self, target_hex, new_id ):
        if new_id in self.catalogue:
            raise NameError("A hex with ID {} is already registered")
        else:
            self.catalogue[new_id] = target_hex
    
    def set_active_hex(self, id):
        if self._active_id is not None:
            self.catalogue[self._active_id].outline = '#ddd'
        
        self._active_id = id
        self.catalogue[self._active_id].outline = '#f00'
    
    def rescale(self):
        pass

    def get_hex_neighbors(self, ID):
        """
        Calculates the IDs of a given Hexes' neighbors
        NOTE: Neighbors not guaranteed to exist! 

        @param ID - ID of center

        @returns a LIST of IDs 
        """

        # convert the id to a bit string
        x_id, y_id, grid = deconstruct_id(ID)


        neighbors = []
        neighbors.append(construct_id(x_id, y_id+1, grid) )
        neighbors.append(construct_id(x_id, y_id-1, grid) )

        if grid:
            neighbors.append(construct_id(x_id,   y_id,   not grid) )
            neighbors.append(construct_id(x_id,   y_id-1, not grid) )
            neighbors.append(construct_id(x_id-1, y_id,   not grid) )
            neighbors.append(construct_id(x_id-1, y_id-1, not grid) )
        else:
            neighbors.append(construct_id(x_id,   y_id+1,   not grid) )
            neighbors.append(construct_id(x_id,   y_id, not grid) )
            neighbors.append(construct_id(x_id+1, y_id+1,   not grid) )
            neighbors.append(construct_id(x_id+1, y_id, not grid) )

        return(neighbors)    

    def get_neighbor_outline(self, ID, size=1):
        """
        returns a flattened set of vertices tracing the circumference of the hex at ID's would-be neightbors 

        @param ID - ID of center

        @returns a LIST of Points 
        """
        center = self.get_point_from_id( ID )
        
        perimeter_points = []
        
        if size==1:
            perimeter_points +=[ center + Point( -0.5, 0.5*rthree)*self._drawscale]
            perimeter_points +=[ center + Point(  0.5, 0.5*rthree)*self._drawscale]
            perimeter_points +=[ center + Point(  1.0, 0.0)*self._drawscale]
            perimeter_points +=[ center + Point(  0.5,-0.5*rthree)*self._drawscale]
            perimeter_points +=[ center + Point( -0.5,-0.5*rthree)*self._drawscale]
            perimeter_points +=[ center + Point( -1.0, 0.0)*self._drawscale]
            return(perimeter_points)
        else:
            # these are shifts to the three unique vertices on the Northern Hexes' outer perimeter
            vector_shift = [ Point(self._drawscale, self._drawscale*rthree),Point(self._drawscale*0.5, 3*rthree*0.5*self._drawscale) , Point(-self._drawscale*0.5, 3*rthree*0.5*self._drawscale)] 
            perimeter_points += vector_shift 
            # now we will rotate these over 5 multiples of -60 degrees  (clockwise rotation)
            
            iteration=1
            while iteration<6:
                # rotate each of the three points by -60 degrees
                # from normal rotation matrix
                for i in range(3):                
                    vector_shift[i] = Point( vector_shift[i].x*0.5 - rthree*vector_shift[i].y*0.5 ,  vector_shift[i].x*rthree*0.5 + 0.5*vector_shift[i].y )

                # and append them to the list of points 
                perimeter_points +=  vector_shift
                # this will be done 5 times in addition to the initial one
                iteration += 1

            perimeter_points = [ i+center for i in perimeter_points ]
            #print("{}\n".format(perimeter_points))
            return( perimeter_points ) 



    def translate(self, vector):
        """
        Unused since this has been replaced by a working system 
        """
        for tile in self.catalogue.values():
            tile.translate( vector )

    def point_to_draw( self, list_of_points ):
        """
        this transforms a list of points into a flattened list of coordinates in Draw-Space
        """
        list_of_coords = []
        # transform and flatten
        for point in list_of_points:
            point += self.draw_relative_to
            point *= self._zoom
            list_of_coords += [point.x, point.y]
        return( list_of_coords )
        


    def draw(self, canvas):
        """
        Draws the canvas! 
        """
        #clear the canvas
        canvas.delete("all")
        # draw all the hexes
        for tile in self.catalogue.values():
            canvas.create_polygon( self.point_to_draw(tile._vertices), outline=tile.outline, fill=tile.fill, width=2.5,tag='background')
        
        # draw the selected one 
        if self._active_id is not None:
            canvas.create_polygon( self.point_to_draw(self.catalogue[ self._active_id ]._vertices), outline= self.catalogue[self._active_id].outline, fill=self.catalogue[self._active_id].fill, width=2.5, tag='background')
    
        if self._outline is not None:
            canvas.create_polygon( self.point_to_draw(self._outline), outline='gold',fill='',width=2.5,tag='background')

    def get_id_from_point(self, point):
        """
        Function to return either nearest hex center, or ID
        """

        # need to account for any zoom and translations applied to the drawing relative to the base global coordinates 
        point /= self._zoom
        point -= self.draw_relative_to 
        
        # keep a copy of the untranslated point! 
        og_point = Point( point.x, point.y )
                
        base_idy = int(floor((point.y/( rthree*self._drawscale)) + 0.5) )
        base_idx = int(floor((point.x/(3.*self._drawscale)) + (1./3.)))
         
        # this could be the point 
        candidate_point =Point(base_idx*3*self._drawscale, base_idy*rthree*self._drawscale )

         # the secondary grid is shifted over a bit, so let's do the same again... 
        point.x -= 1.5*self._drawscale
        point.y -= rthree*self._drawscale*0.5

        # recalculate these
        base_idy_2 = int(floor((point.y/( rthree*self._drawscale)) + 0.5))
        base_idx_2 = int(floor((point.x/(3.*self._drawscale)) + (1./3.)))
        
        # this is in the off-grid
        candidate_point_2 =Point(base_idx*3*self._drawscale, base_idy*rthree*self._drawscale )
        candidate_point_2 += Point( 1.5*self._drawscale, rthree*self._drawscale*0.5)
        
        if (og_point - candidate_point)**2 < (og_point - candidate_point_2)**2:
            return( construct_id(base_idx, base_idy, True ))
        else:
            return( construct_id(base_idx_2, base_idy_2, False ))
        
    
    def get_point_from_id(self, id):
        """
        Returns the UNTRANSFORMED center of the hex corresponding to the given ID
        """

        x_id, y_id, on_primary_grid = deconstruct_id(id)
        
        # build the poin
        built_point = Point( x_id*3*self._drawscale, y_id*rthree*self._drawscale )
        if not on_primary_grid:
            # transform it if it's on the shifted grid
            built_point += Point( 1.5*self._drawscale, rthree*self._drawscale*0.5)
        
        #built_point -= self.draw_relative_to

        return(built_point)


def construct_id( base_idx, base_idy, main_grid):
    """
    Takes grid coordinates and grid identifier, and returns the global ID
    """
    if type(main_grid)!=bool:
        raise TypeError("Expected type {} for object {}, got {}".format(bool, main_grid, type(main_grid) ))
       
    x_bitstr = '{0:031b}'.format(base_idx)
    y_bitstr = '{0:031b}'.format(base_idy)

    if x_bitstr[0]=='-':
        x_bitstr = '1' + x_bitstr[1:]
    if y_bitstr[0]=='-':
        y_bitstr = '1' + y_bitstr[1:]

    if main_grid:
        lead = '10'
    else:
        lead = '00'

    return(int( lead + x_bitstr + y_bitstr ,2 ))

def deconstruct_id( id ):
    bitstring = '{0:064b}'.format( id )
    
    """
    takes global ID, returns tuple ( x_coordinate, y_coordinate, grid)
    """

    # the first bit specifies which grid the hex is on. The second bit is unused 
    if bitstring[0]=='1':
        on_primary_grid = True
    else:
        on_primary_grid = False

    # extract the information to give the number
    # skipping the sign bits and the grid bits 
    x_id = int( bitstring[3:33], 2) # bit [2] specifies sign
    y_id = int( bitstring[34:], 2) # bit [33] specifies sign
    if bitstring[2]=='1':
        x_id*=-1
    if bitstring[33]=='1':
        y_id*=-1

    return((x_id,y_id, on_primary_grid))


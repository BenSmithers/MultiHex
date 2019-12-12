from PyQt5.QtWidgets import QGraphicsScene, QGraphicsDropShadowEffect, QGraphicsItem, QGraphicsPolygonItem
from PyQt5 import QtGui, QtCore

try:
    from numpy import sqrt, atan, pi, floor, cos, sin
except ImportError:
    from math import sqrt, atan, pi, floor, cos, sin

import pickle

"""
Ben Smithers
b.smithers.actual@gmail.com 

Core objects for MultiHex

Objects:
    basic tool      - interface for clicker control
    clicker control - interface between GUIs and tools 
    Point           - 2D vector with associated operators
    HexMap          - base upon which all the maps are built
        construct_id 
        deconstruct_id 
    Region          - A perimeter, lists of IDs associated with it, and means to modify this
        glom
    Entity          - static entity on a Hex
    Mobile          - a mobile object that travels between hexes
    Path            - path traveling between vertices. Generic implementation of roads/rivers/etc
"""


def is_number(object):
    try:
        a= 5+object
        return(True)
    except TypeError:
        return(False)

class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self, parent=None):
        pass
    def press(self,event):
        """
        Called when the right mouse button is depressed 

        @param event 
        """
        pass
    def activate(self, event):
        """
        This is called when the right mouse button is released from a localized click. 

        @param event - location of release
        """
        pass
    def hold(self,event ):
        """
        Called continuously while the right mouse button is moved and depressed 

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def select(self, event ):
        """
        Left click released event, used to select something

        @param event - Qt event object. has where the mouse is
        """
        pass
    def move(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass
    def drop(self):
        """
        Called when this tool is being replaced. Cleans up anything it has drawn and should get rid of (like, selection circles)
        """
        pass
    def toggle_mode(self, force=None):
        pass

class clicker_control(QGraphicsScene):
    """
    Manages the mouse interface for to the canvas.
    """
    def __init__(self, parent=None, master=None):
        QGraphicsScene.__init__(self, parent)

        self._active = None
        self._held = False
        
        self.master = master

        self._alt_held = False

    def keyPressEvent(self, event):
        event.accept()
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_held = True
    def keyReleaseEvent(self, event):
        event.accept()
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_held = False

    def mousePressEvent(self, event):
        """
        Called whenever the mouse is pressed within its bounds (The drawspace)
        """
        if event.button()==QtCore.Qt.RightButton: # or (event.button()==QtCore.Qt.LeftButton and self._alt_held):
            event.accept() # accept the event
            self._held = True # say that the mouse is being held 
            self._active.press( event )

    def mouseReleaseEvent( self, event):
        """
        Called when a mouse button is released 
        """
        if event.button()==QtCore.Qt.RightButton: # or (event.button()==QtCore.Qt.LeftButton and self._alt_held):
            # usually a brush event 
            event.accept()
            self._held = False
            self._active.activate(event)

        elif event.button()==QtCore.Qt.LeftButton:
            # usually a selection event
            event.accept()
            self._active.select( event )

   #mouseMoveEvent 
    def mouseMoveEvent(self,event):
        """
        called continuously as the mouse is moved within the graphics space. The "held" boolean is used to distinguish between regular moves and click-drags 
        """
        event.accept()
        if self._held:
            self._active.hold( event )
 
        self._active.move( event )

    # in c++ these could've been templates and that would be really cool 
    def to_hex(self):
        """
        We need to switch over to calling the writer control, and have the selector clean itself up. These two cleaners are used to git rid of any drawn selection outlines 
        """
        self._active.drop()
        self._active = self.master.writer_control

    def to_region(self):
        """
        same...
        """
        self._active.drop()
        self._active = self.master.region_control
 
class Point:
    """
    A vector in 2D Cartesian space.

    @x          - x component of vector
    @y          - y component of vector
    @magnitude  - length of this vector
    """
    def __init__(self, ex =0.0, why=0.0):
        if not is_number(ex):
            raise TypeError("Expected type {} for arg 'ex', received {}".format(float, type(ex)))
        if not is_number(why):
            raise TypeError("Expected type {} for arg 'why', received {}".format(float, type(why)))

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
        if (type(obj)!=Point):
            raise TypeError("Cannot add type {} to Point object".format(type(obj)) ) 
        new = Point( self.x + obj.x, self.y + obj.y)
        return( new )
    def __sub__(self, obj):
        """
        Same as addition, but for subtraction
        """
        if (type(obj)!=Point):
            raise TypeError("Cannot subtract type {} from Point object".format(type(obj))) 
        new = Point( self.x - obj.x, self.y - obj.y)
        return( new )
    def __mul__(self, obj):
        """
        Calculate the inner product of two vector-points, or scale one vector-point by a scalar. 
        """
        if is_number(obj):
            return( Point( self.x*obj, self.y*obj ))
        elif type(obj)==Point:
            return( self.x*obj.x + self.y*obj.y )
        else:
            raise TypeError("Cannot multiply type {} with Point object".format(type(obj)))
    def __eq__(self, obj):
        if type(obj)==Point:
            return( abs(self.x-obj.x)<0.01  and abs(self.y-obj.y)<0.01 )
        else:
            return(False)
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
            return( cls._angle ) 

    # casting this object as a string 
    def __str__(self):
        return( "({},{})".format( self.x, self.y ) )
    
    def __repr__(self):
        return("Point({},{})".format(self.x,self.y))

default_p = Point(0.0,0.0)
rthree = sqrt(3)

class Hex:
    """
    Datastructure to represent a single hex on a hex map

    @ build_name            - creates a name for hex biome - not implemented
    @ rescale_color         - recalculates the color based off of the current color and altitude
    """
    def __init__(self, center=default_p, radius=1.0 ):
        if type(center)!=Point:
            raise TypeError("Aarg 'center' must be of type {}, received {}".format( Point, type(center)))
        
        self._center = center
        self._radius = radius
        
        self.outline= (240,240,240)
        self.fill   = (100,100,100) 
        self._vertices = [ center for i in range(6) ]

        # used in procedural generation
        self.genkey            = '00000000'

        self._vertices[0] = self._center + Point( -0.5, 0.5*rthree)*self._radius
        self._vertices[1] = self._center + Point(  0.5, 0.5*rthree)*self._radius
        self._vertices[2] = self._center + Point(  1.0, 0.0)*self._radius
        self._vertices[3] = self._center + Point(  0.5,-0.5*rthree)*self._radius
        self._vertices[4] = self._center + Point( -0.5,-0.5*rthree)*self._radius
        self._vertices[5] = self._center + Point( -1.0, 0.0)*self._radius

    @property
    def center(self):
        return( Point( self._center.x, self._center.y) )

    @property
    def radius(self):
        copy = self._radius
        return( copy )

    @property 
    def vertices(self):
        copy = [ self.center for i in range(6) ] 
        copy[0] = self.center + Point( -0.5, 0.5*rthree)*self.radius
        copy[1] = self.center + Point(  0.5, 0.5*rthree)*self.radius
        copy[2] = self.center + Point(  1.0, 0.0)*self.radius
        copy[3] = self.center + Point(  0.5,-0.5*rthree)*self.radius
        copy[4] = self.center + Point( -0.5,-0.5*rthree)*self.radius
        copy[5] = self.center + Point( -1.0, 0.0)*self.radius
        return( copy )

    def build_name(self):
        return("")
    def reset_color(self):
        pass
            
   
    def __repr__(self):
        return("{}@{}".format(self.__clas__, self.id))

    



def save_map(h_map, filename):
    h_map.drawn_hexes = {}
    h_map._active_id = None
    h_map._outline = None
    h_map.outline_obj = None

    file_object = open(filename, 'wb')
    pickle.dump( h_map, file_object, -1)
    file_object.close()

def load_map(filename):
    if type(filename)==tuple:
        print(filename)
    file_object = open(filename, 'rb')
    hex_pickle = pickle.load(file_object)
    file_object.close()
    return( hex_pickle )


class Hexmap:
    """
    Object to maintain the whole hex catalogue, draw the hexes, registers the hexes

    Methods:
    @ remove_hex            - unregister hex from catalogue
    @ register_hex          - register a hex in the catalogue
    @ set_active_hex        - sets hex to "active"
    @ get_hex_neighbors         - get list of IDs for hexes neighboring this one
    @ get_neighbor_outline      - retursn list of points to outline cursor 
    @ points_to_draw        - takes list of map-Points, prepares flattened list of draw coordinates 
    @ get_id_from_point     - constructs neares ID to point
    @ get_point_from_id     - constructs point from ID
    @ register_new_region   - takes a region, registers it in the rid_catalogue with a unique region id (rid)
    @ add_to_region         - adds a single hex to a region
    @ remove_from_region    - removes hex from region
    @ merge_regions         - takes two rids, merges the regions

    Attributes:
    @ catalogue             - Dictionary of hexes. The hexIDs are keys to the hexes themselves 
    @ rid_catalogue         - 2-level dictionary: rid_catalogue[ layer ][ rID ]. Points to region object 
                                + layer is the region layer (biome/kingdom/etc)
                                + rID is the identifier of the region
    @ id_map                - similar data structure as rid_catalogue. Region layer and hexID returns rID hex belongs to. Raises key error if no association! 
    @ rivers                - dictionary containing lists of paths. Dict key for path type 
    @ drawscale             - scaling factor of entire map. Establishes hex size 
    """
    def __init__(self):
        self.catalogue = {}
        self.rid_catalogue = {} #region_id -> region object
        self.id_map = {} # hex_id -> reg_id 
        self.paths = {}

        # overal scaling factor 
        self._drawscale = 15.0

        self._active_id = None
        self._party_hex = None
        self._outline   = None
        self._outline_obj = None

        # These are used to convert from map-space to draw-space 
        self._zoom      = 1.0
        self.draw_relative_to = Point(0.0,0.0)
        self.origin_shift     = Point(0.0,0.0)
    def register_new_region( self, target_region, r_layer ):
        """
        Registers a new region with this Hexmap. Adds it to the dictionaries, give it a unique rID, and set up all the maps for its contained Hexes 
        """


        # make sure this region layer exists. If it doesn't, let's make it. 
        if r_layer not in self.id_map:
            self.id_map[r_layer] = {}
        if r_layer not in self.rid_catalogue:
            self.rid_catalogue[r_layer] = {}

        # verify that the target region doesn't have any hexes already belonging to a registered region
        for hex_id in target_region.ids:
            if hex_id in self.id_map[r_layer]:
                raise KeyError("Region contains hex {} belonging to other region: {}".format(hex_id, self.id_map[r_layer][hex_id]))

        # first settle on a new rid - want the smallest, unused rid 
        new_rid = 1
        while new_rid in self.rid_catalogue[r_layer]:
            new_rid += 1
        
        target_region.set_color( new_rid )
        # register the region in the hexmap's region catalogue 
        self.rid_catalogue[r_layer][ new_rid ] = target_region
        # register the connections between the new region's hexes and the new rid
        # this allows for quick correlations from point->hex->region
        for hex_id in target_region.ids:
            self.id_map[r_layer][ hex_id ] = new_rid 
        
        # return the new_rid
        return( new_rid )

    def add_to_region( self, rID, hex_id, r_layer ):
        """
        Adds a hex to a region. If the hex belongs to a different region, we remove if from that region first

        @param rID      - rID of region to which we are adding
        @param hex_id   - ID of hex to add to region
        @param r_layer  - string (key) for the desired region layer 
        """
        if r_layer not in self.rid_catalogue:
            raise KeyError("Region layer {} does not exist.".format(r_layer))

        # throws KeyError if rID not in catalogue
        # we aren't handling that error. Downstream problem...
        if rID not in self.rid_catalogue[r_layer]:
            raise KeyError("Region no. {} not recognized.".format( rID) )
        if hex_id not in self.catalogue:
            raise KeyError("Hex id no. {} not recognized.".format( hex_id ))

        other_rid = -1
        # If the hex is already in a region, remove it from that region 
        if hex_id in self.id_map[r_layer]:
            if self.id_map[r_layer][hex_id]==rID:
                return # nothing to do
            else:
                raise RegionPopError("Can't do that.")
                
                # removing this functionality. Lead to unexpected behavior where we popped a hex from another region regardless of whether or not it was possible to add anything to this region! 
                #other_rid = self.id_map[hex_id]
                #self.remove_from_region( hex_id )

        # the hex does not belong to a region, has no map in id_map
        # add the hex to the region and update the id map
        self.rid_catalogue[r_layer][ rID ].add_hex_to_self( hex_id )
        self.id_map[r_layer][ hex_id ] = rID

        return(other_rid)

    def remove_from_region( self, hex_id, r_layer ):
        """
        Removes a hex from a region

        @param hex_id   - ID of hex from which to remove region affiliation 
        @param r_layer  - string (key) for the desired region layer
        """
        if r_layer not in self.rid_catalogue:
            raise KeyError("Region layer {} does not exist.".format(r_layer))

        # removes the hex_id from whichever region it's in
        if hex_id not in self.id_map[r_layer]:
            raise KeyError("Hex no. {} not registered".format(hex_id))
        
        # update the region extents 
        self.rid_catalogue[r_layer][ self.id_map[r_layer][hex_id] ].pop_hexid_from_self( hex_id )
        
        # check if region still has size, if not, delete the region
        if len(self.rid_catalogue[r_layer][ self.id_map[r_layer][hex_id] ].ids)==0:
            del self.rid_catalogue[r_layer][ self.id_map[r_layer][hex_id] ]

        # delete the hexes' association to the now non-existent region
        del self.id_map[r_layer][hex_id]
        

    def merge_regions( self, rID_main, rID_loser, r_layer ):
        """
        Merges two regions

        @param rID_main  - rID of region which will accept the hexes from rID_loser
        @param rID_loser - rID of region which will be absorbed into rID_main
        @param r_layer   - string (key) for the desired region layer. Eg - biome, border, ...
        """
        if r_layer not in self.rid_catalogue:
            raise KeyError("Region layer {} does not exist.".format(r_layer))

        if (rID_main not in self.rid_catalogue[r_layer]):
            raise KeyError ("Region {} not recognized".format(rID_main))
        if (rID_loser not in self.rid_catalogue[r_layer]):
            raise KeyError("Region {} not recognized".format(rID_loser))
         
        # merge second region into first one
        self.rid_catalogue[r_layer][ rID_main ].merge_with_region( self.rid_catalogue[r_layer][rID_loser] )
        
        # update the entries in the id_map to point to the new region
        for hex_id in self.rid_catalogue[r_layer][rID_loser].ids:
            self.id_map[r_layer][ hex_id ] = rID_main

        # delete the old region
        del self.rid_catalogue[r_layer][ rID_loser ]


    def remove_hex( self, target_id):
        """
        Try popping a hex from the catalogue. Deletes the key, deletes the hex. 

        @param target_id - the ID of the removed hex
        """ 
        del self.catalogue[target_id] #delete the hex 
        if target_id == self._active_id:
            self._active_id = None
        elif self._party_hex == self._active_id:
            pass

    def register_hex(self, target_hex, new_id ):
        assert( target_hex._radius == self._drawscale )
        if not isinstance(target_hex, Hex):
            raise TypeError("Cannot register non-hexes, dumb dumb!")

        if new_id in self.catalogue:
            temp_altitude = self.catalogue[new_id]._altitude_base
            temp_temp     = self.catalogue[new_id]._temperature_base
            self.catalogue[new_id] = target_hex
            self.catalogue[new_id]._altitude_base = temp_altitude
            self.catalogue[new_id]._temperature_base = temp_temp
            self.catalogue[new_id].rescale_color()
        else:
            self.catalogue[new_id] = target_hex
    

    def set_active_hex(self, id):
        if self._active_id is not None:
            self.catalogue[self._active_id].outline = '#ddd'
        
        self._active_id = id
        self.catalogue[self._active_id].outline = '#f00'
    
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



        if grid:
            neighbors.append(construct_id(x_id-1, y_id,   not grid) )
            neighbors.append(construct_id(x_id, y_id+1, grid) )
            neighbors.append(construct_id(x_id,   y_id,   not grid) )
            neighbors.append(construct_id(x_id,   y_id-1, not grid) )
            neighbors.append(construct_id(x_id, y_id-1, grid) )
            neighbors.append(construct_id(x_id-1, y_id-1, not grid) )
        else:
            neighbors.append(construct_id(x_id+1, y_id+1,   not grid) )
            neighbors.append(construct_id(x_id, y_id+1, grid) )
            neighbors.append(construct_id(x_id,   y_id+1,   not grid) )
            neighbors.append(construct_id(x_id,   y_id, not grid) )
            neighbors.append(construct_id(x_id, y_id-1, grid) )
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

    def points_to_draw( self, list_of_points ):
        """
        Takes list of map-space points, converts it to list of QPoints in draw space
        """
        list_of_coords = []
        # transform and flatten
        for point in list_of_points:
            list_of_coords += [QtCore.QPointF( point.x, point.y )]
        return( list_of_coords )
    
    def get_vertices_beside( self, vertex, v_type=None):
        """
        Return the vertices that neighbor this one on the HexMap

        @ param vertex  - the vertex whose neighbors we want to find
        @ param v_type  - optional integer, (1 or 2). Specifies the vertex type so we can save some time in calculation. If not provided it discovers the vertex type itself. See `get_ids_around_vertex` for the vertext type descriptions 
        """
        if not isinstance( vertex, Point):
            raise TypeError("Expected type {} for 'vertex', received {}".format(Point, type(vertex)))
        
        if v_type is None:
            print("this shouldn't be called either")
            l_up    = self.get_id_from_point( place+Point( -0.25*self._drawscale,   rthree*0.25*self._drawscale ))
            l_down  = self.get_id_from_point( place+Point( -0.25*self._drawscale,-1*rthree*0.25*self._drawscale ))
            r_up    = self.get_id_from_point( place+Point(  0.25*self._drawscale,   rthree*0.25*self._drawscale ))
            r_down  = self.get_id_from_point( place+Point(  0.25*self._drawscale,-1*rthree*0.25*self._drawscale ))

            if l_up==l_down:
                v_type = 2
            elif r_up==r_down:
                v_type = 1
            else:
                raise ValueError("Not sure if {} is a vertex...".format(vertex) )
        

        assert( type(v_type) == int)

        if v_type==1:
            neighbors = [   vertex + (Point(-1.0,  0.0       )*self._drawscale), 
                            vertex + (Point( 0.5,  0.5*rthree)*self._drawscale), 
                            vertex + (Point( 0.5, -0.5*rthree)*self._drawscale) ]
        elif v_type==2:
            neighbors = [   vertex + (Point( 1.0,  0.0       )*self._drawscale), 
                            vertex + (Point(-0.5,  0.5*rthree)*self._drawscale), 
                            vertex + (Point(-0.5, -0.5*rthree)*self._drawscale) ]

        else:
            raise ValueError("Unrecognized vertex type {}".format(v_type))

        return( neighbors )

    def get_ids_around_vertex( self, place, v_type = None):
        """
        This returns three IDs. It is assumed that `place` is a vertex. will return inconsistent results otherwise 
        """
        
        if type(place)!=Point:
            raise TypeError("Expected type {} for object 'place', received {}".format(Point, type(place)))

        # there are one of two kinds of vertices:
        #
        #  1  __/   \__  2 
        #       \   /
        #
        # We don't know which 

        if v_type is None:
            print("this shouldn't be called")
            # deduce the vertex type
            l_up    = self.get_id_from_point( place+Point( -0.25*self._drawscale,   rthree*0.25*self._drawscale ))
            l_down  = self.get_id_from_point( place+Point( -0.25*self._drawscale,-1*rthree*0.25*self._drawscale ))
            r_up    = self.get_id_from_point( place+Point(  0.25*self._drawscale,   rthree*0.25*self._drawscale ))
            r_down  = self.get_id_from_point( place+Point(  0.25*self._drawscale,-1*rthree*0.25*self._drawscale ))

            if l_up==l_down:
                v_type = 2
                #return([ l_up, r_up, r_down]) # type 2
            elif r_up==r_down:
                v_type=1
                #return([ l_up, l_down, r_up]) # type 1
            else:
                raise ValueError("I don't think this place, {}, is a vertex".format(place))
        
        assert(type(v_type)==int)
        if v_type==1:
            return([    self.get_id_from_point( place + Point(1.0 ,  0.0       )*self._drawscale ), 
                        self.get_id_from_point( place + Point(-0.5,  0.5*rthree)*self._drawscale ),
                        self.get_id_from_point( place + Point(-0.5, -0.5*rthree)*self._drawscale ) ])
        elif v_type==2:
            return([    self.get_id_from_point( place + Point(-1.0 , 0.0       )*self._drawscale ), 
                        self.get_id_from_point( place + Point( 0.5,  0.5*rthree)*self._drawscale ),
                        self.get_id_from_point( place + Point( 0.5, -0.5*rthree)*self._drawscale ) ])

        else:
            raise ValueError("Invalid Vertex type value: {}".format(v_type))

    def get_ids_beside_edge(self, start, end):
        """
        Returns a pair of hexIDs to the left and right of the edge defined by 'start' and 'end'

        @param start    - type Point, defines start of edge
        @param end      - type Point, defines end of edge 

        start and end should be drawscale apart
        """

        if type(start)!=Point:
            raise TypeError("Arg 'start' is not type point, it is {}".format(start))
        if type(end)!=Point:
            raise TypeError("Arg 'end' is not type point, it is {}".format( end ))
        diff = start-end
        if (diff.magnitude - self._drawscale)/self._drawscale > 0.01:
            raise ValueError("Edge length is {}, expected {}".format( diff.magnitude, self._drawscale))
        # displacement vector from 'end' object. 
        #       points towards CW hex
        new_angle = diff.angle - 120.
        displacement = Point( cos( new_angle) , sin(new_angle) )*self._drawscale 
        CW_hex  = end + displacement 

        new_angle_ccw = diff.angle + 120.
        displacement_ccw = Point( cos(new_angle_ccw), sin(new_angle_ccw))*self._drawscale
        CCW_hex = end + displacement_ccw

        return( self.get_id_from_point( CW_hex) , self.get_id_from_point( CCW_hex ) )


    def get_id_from_point(self, point):
        """
        Function to return either nearest hex center, or ID
        """
        if type(point)!=Point:
            raise TypeError("{} is not a Point, it is {}".format(point, type(point)))


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

    bit      1 - grid specifier 
    bit      2 - unused
    bit      3 - x coord sign
    bits  4-33 - x coordinate 
    bit     34 - y coord sign
    bits 35-64 - y coordinate
    
    These are all ligned up, and it is treated as a 64 bit unsigned integer. 
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

    Opposite process as described in 'construct id'
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

"""
@class  Region  - representation of a collection of hexes
@method glom    - combines two lists of points into a single list of points
"""

# by the four-color theorem, we only need four colors
# six just makes it easier and prettier 
region_colors= (    (187,122,214),
                    (29,207,189),
                    (74,16,54),
                    (255,81,0),
                    (30,255,0),
                    (74,255,255) )

class RegionMergeError( Exception ):
    pass
class RegionPopError( Exception ):
    pass

class Region:
    """
    A Region is a colleciton of neighboring of Hexes on a Hexmap. Regions are continuous.

    @ add_hex_to_self       - take the hex at hex_id and add its extent to this region
    @ merge_with_region     - take the given region, merge with it
    @ cut_region_from_self  - remove the extent of any hexes in other region form self
    @ pop_hexid_from_self   - remove the extent of one hex from the self
    """

    def __init__(self, hex_id, parent):
        self.enclaves = [  ]
        self.ids = [ hex_id ]
        # regions don't know their own region_id. That's a hexmap thing
        # self.reg_id = 0
        self.name = ""

        self.color = (0, 0, 0)
        
        self.parent = parent
        # may throw KeyError! That's okay, should be handled downstream 
        self.perimeter = self.parent.catalogue[hex_id]._vertices
         
    def get_center_size(self):
        min_x = None
        max_x = None 
        min_y = None
        max_y = None

        # average all of the IDs positions to get an average point 
        center = Point(0.0, 0.0)
        for hex_id in self.ids:
            this_hex = self.parent.catalogue[hex_id]
            center += this_hex.center
            if min_x == None:
                min_y = this_hex.center.y
                max_y = this_hex.center.y
                min_x = this_hex.center.x
                max_x = this_hex.center.x
            else:
                if min_x>this_hex.center.x:
                    min_x=this_hex.center.x
                if max_x<this_hex.center.x:
                    max_x=this_hex.center.x
                if min_y>this_hex.center.y:
                    min_y=this_hex.center.y
                if max_y<this_hex.center.y:
                    max_y=this_hex.center.y

        extent = Point( max_x-min_x, max_y-min_y )
        center = center*(1.0/len(self.ids))
        return( center, extent )

    def set_color(self, number):
        # not hard-coding the number of colors in case I add more
        self.color = region_colors[ number % len(region_colors) ]

    def add_hex_to_self( self, hex_id ):
        # build a region around this hex and merge with it
        if hex_id in self.ids:
            return #nothing to do...
        
        temp_region = Region( hex_id , self.parent )
        self.merge_with_region( temp_region )

    def merge_with_region( self, other_region ):
        """
        Takes another region and merges it into this one.

        """
        #TODO: prepare a write up of this algorithm 

        # determine if Internal or External region merge
        internal = False  # is 

        # we need to start on the beginning of a border, so we get the first point that's on the border
        start_index = 0
        while (self.perimeter[start_index] not in other_region.perimeter) and (self.perimeter[(start_index+1)%len(self.perimeter)] in other_region.perimeter):
            start_index+=1  

        internal = True
        for point in self.perimeter:
            if point in other_region.perimeter:
                internal = False


        # if we found a border on the perimeter, this is an external type merge
        #if start_index!=len(self.perimeter):
        #    internal = False
                
        if not internal: #external merge!  
            # count the number of borders, find the "starting points" for the new enclaves and perimeter
            on_border = False   
            start_indices = []
            for point in range(len(self.perimeter)+1):
                if self.perimeter[ (point+start_index)%len(self.perimeter) ] in other_region.perimeter:
                    if not on_border:
                        on_border = True
                else:
                    if on_border:
                        start_indices.append( (point+start_index)%len(self.perimeter)) 
                        on_border = False
            loops = [glom( self.perimeter, other_region.perimeter, ind ) for ind in start_indices]
            max_x = None
            which = None
            # the perimeter loop will, of course, have a greater extent in every direction. So we just find the loop which goes the furthest in x and know that's the perimeter
            #   all the other loops are enclaves 
            for loop in loops:
                for point in loop:
                    if max_x is None:
                        max_x = point.x
                        which = loop
                    else:
                        if point.x>max_x:
                            max_x = point.x
                            which = loop
            if which is None:
                print("start indices: {}".format( start_indices ))
                print("Loops: {}".format(loops))
                print("self.perimeter: {}".format(self.perimeter))
                print("other one: {}".format(other_region.perimeter))
                raise TypeError("Some bullshit has happened. Tell Ben because this shouldn't happen.")
            self.perimeter = which
            for loop in loops:
                if loop!=which:
                    self.enclaves += [ loop ]

        else:
            # need to find the enclave this other region is bordering 
            found_enclave = False
            for enclave in self.enclaves:
                start_index = 0
                while enclave[start_index] not in other_region.perimeter:
                    start_index+= 1
                    if start_index==len(enclave):
                        # does not border this enclave 
                        break
                if start_index==len(enclave):
                    # let's go to the next one
                    continue
                
                # if the new region borders two distinct enclaves, there needs to be overlap between the regions, and this method is broken
                #assert( not found_enclave )
                found_enclave = True
                
                # same as before, we walk around 
                start_indices = []
                on_border = False
                for point in range(len( enclave )):
                    if enclave[ (point + start_index)%len(enclave) ] in other_region.perimeter:
                        if not on_border:
                            on_border = True
                    else:
                        if on_border:
                            start_indices.append( ( point + start_index) % len(enclave ))
                            on_border = False

                # that old enclave is split into multiple new enclaves (or even just one)
                self.enclaves.pop( self.enclaves.index( enclave ) )
                self.enclaves += [ glom( enclave, other_region.perimeter, index) for index in start_indices ] 
            if not found_enclave:
                # the target region doesn't border an enclave and it doesn't border the perimeter.
                # we can't merge these
                raise RegionMergeError("Regions must share some border/enclave")

        # these are just added on in
        self.enclaves   += other_region.enclaves 
        self.ids        += other_region.ids
    
    def cut_region_from_self( self, other_region):
        # the order these hexes are popped is suuuper important.
        # As is, this will lead to unexpected behavior!! 
        for ID in other_region.ids:
            if ID in self.ids:
                self.pop_hexid_from_self( ID )

        
    def pop_hexid_from_self( self, hex_id ):
        """
        Pops a hex from this region

        Why was this the hardest thing to write in all of MultiHex... 
        """

        #TODO: Case where removing a hex splits the region into 2-3 smaller regions 
        #           + such cases are distringuished by their perimeters having more than 1 border with the pop hex

        if len(self.ids)==1:
            if self.ids[0]==hex_id:
                self.ids.pop(0)
                self.perimeter = []

        which = None
        for each in range(len( self.ids )):
            if hex_id==self.ids[each]:
                which=each
                break
        if which is None:
            print("Looking for {}, but only have {}".format( hex_id, self.ids))
            raise ValueError("id not in region")
       

        
        # countable number of cases
        #    1. hex shares no border with either perimeter or any enclave: popped and made into enclave
        #    2. hex _only_ shares border with perimeter: glom perimeter to hex
        
        #    3. hex borders perimeter multiple times. Popping hex will create multiple regions. We forbid this possibility... 

        this_hex = self.parent.catalogue[ hex_id ]
        hex_perim = this_hex._vertices[::-1]

        # check perimeter

        outer_hex = False
        n_borders = 0
        on_border = False

        start_index = 0
        while self.perimeter[ start_index ] in hex_perim:
            start_index+=1

        for point in range(len(self.perimeter)):
            if self.perimeter[(point+start_index)%len(self.perimeter)] in hex_perim:
                outer_hex = True
                if not on_border:
                    on_border = True
                    n_borders+=1 
            else:
                if on_border:
                    on_border = False
        if n_borders>1:
            raise RegionPopError("Can't pop a hex that would divide a region into several")
        
        enclave_start_points = []
        # check the enclaves
        for enclave in self.enclaves:
            index = 0
            while index <len(enclave) :
                if (enclave[index] in hex_perim) and (enclave[(index + 1) % len(enclave)] not in hex_perim):
                    # note the hex indices where we'll switch to an enclave, and also note which enclave to switch to! 
                    enclave_start_points.append( [ hex_perim.index( enclave[index] ), enclave ] )
                    break
                index += 1


        # It is now known whether the hex is on the outer rim or within the region
        if outer_hex:
            new_perim = []

            # walk around the outer perimeter until we get to a point 
            start_index = 0
            while self.perimeter[start_index] not in hex_perim:
                start_index += 1

            index = start_index
            while self.perimeter[index % len(self.perimeter)] not in hex_perim:
                new_perim.append( self.perimeter[ index % len( self.perimeter) ] )
                index += 1

            new_perim.append( self.perimeter[ index % len( self.perimeter) ] )

            hex_index = (hex_perim.index( self.perimeter[index %len(self.perimeter)] ) + 1 )%len(hex_perim)

            while hex_perim[hex_index % len(hex_perim)] not in self.perimeter:
                
                # check if this is the beginning of a thingy
                loop_complete = False
                for possibility in enclave_start_points:
                    if possibility[0]==(hex_index % len(hex_perim)):
                        new_perim.append( hex_perim[possibility[0]])
                        enclave_counter = (possibility[1].index( hex_perim[possibility[0]] ) + 1)%len(possibility[1])

                        while possibility[1][ enclave_counter % len(possibility[1]) ] not in hex_perim:
                            new_perim.append( possibility[1][ enclave_counter % len(possibility[1])] )
                            enclave_counter += 1
                        

                        hex_index = hex_perim.index( possibility[1][ enclave_counter % len(possibility[1])] )
                        loop_complete = True
                        break
                if not loop_complete:
                    new_perim.append( hex_perim[ hex_index % len(hex_perim)] )
                    hex_index += 1
            
            index = self.perimeter.index( hex_perim[hex_index % len(hex_perim)] )
            while (index % len(self.perimeter))!=start_index:
                new_perim.append( self.perimeter[index % len(self.perimeter)])
                index+=1
            
            self.perimeter = new_perim
            for possibility in enclave_start_points:
                self.enclaves.pop( self.enclaves.index( possibility[1] ) )
            
        else:
            if len(enclave_start_points) == 0:
                self.enclaves.append( hex_perim )
            else: 

                # internal placement. Perimeter will remain unchanged! 
                # will be adding an enclave (may merge 2-3 enclaves into 1)
                # already have all of those neighbor enclaves! 
                # popping internal hex. This will probably be a lot like the other case 
                hex_start = 0
                while( (hex_start % len(hex_perim)) not in [part[0] for part in enclave_start_points] ):
                    hex_start += 1
                new_enclave = []
                counter = hex_start % len(hex_perim)
                while True:
                    loop_complete = False
                    for part in enclave_start_points:

                        if ( counter % len(hex_perim)) == part[0]:
                            new_enclave.append( hex_perim[ part[0] ] )
                            enclave_counter = ( part[1].index( hex_perim[part[0]] ) + 1 )%len(part[1])
                            while part[1][ enclave_counter % len( part[1] )] not in hex_perim:
                                new_enclave.append( part[1][enclave_counter % len(part[1])]) 
                                enclave_counter += 1

                            
                            new_enclave.append( part[1][enclave_counter%len(part[1])] )
                            counter = (hex_perim.index( part[1][ enclave_counter % len( part[1] )] ) + 1) %len(hex_perim)
                            loop_complete = True
                            break
                    
                    if not loop_complete:
                        new_enclave.append( hex_perim[ counter % len(hex_perim)])
                        counter += 1
                    if (counter%len(hex_perim))==hex_start:
                        break
                    
                # each of the old enclaves that we found need tobe popped
                for part in enclave_start_points:
                    self.enclaves.pop( self.enclaves.index( part[1] ))

                self.enclaves.append( new_enclave )

        
        self.ids.pop( which )

def glom( original, new, start_index):
    """
    Partially gloms two perimeters together.

    Walks clockwise around one perimeter, switches to the other, walks more, switches back, and eventually forms a closed loop. 
    """

    new_perimeter = []

    index = start_index 
    while original[ index % len(original) ] not in new:
        new_perimeter += [original[ index % len(original) ]]
        index += 1
    
    new_perimeter+= [ original[index % len(original)] ]
    # returns index for start of border on "new" loop 
    index = (new.index( original[index % len(original)] ) + 1) % len(new)

    
    while (new[ index % len(new) ] not in original): # and (new[(index+1)%len(new)] not in original):
        new_perimeter += [new[index % len( new) ]]
        index += 1
    
    new_perimeter+= [ new[index%len(new)] ]
    try:
        index = (original.index( new[index % len(new)] ) + 1)%len(original)
    except ValueError as e:
        print( original)
        print( new)
        print(e)
        sys.exit()

    while (index % len(original) != start_index ):
        new_perimeter += [ original[index % len(original)] ]
        index +=1
    

    if new_perimeter == []:
        raise Exception("Something terribly unexpected happened: {}, {}, {}".format(original, new, start_index))

    return( new_perimeter )

class Entity:
    """
    Defines static entity that can be placed on a Hex
    """
    def __init__(self, name):
        if not type(name)==str:
            raise TypeError("Arg 'name' must be {}, received {}".format(str, type(name)))
        self.name = name

        self.speed  = 1. #miles/minute
        self.contains = {}

class Mobile:
    """
    Defines a mobile map entity
    """
    def __init__(self, name):
        if not type(name)==str:
            raise TypeError("Arg 'name' must be {}, received {}".format(str, type(name)))
        self.name = name

class Path:
    """
    Generic path following the borders of the hexes
    Basically a glorified list where we force it to be made of Points

    @attr color      - 
    @attr _vertices  - list of this path's vertices 
    @attr _step_calc - whether or not the 'step size' has been calculated
    @attr _step      - length of the step sizes between placed points 
    """

    def __init__(self, start):
        if not isinstance(start , Point):
            raise TypeError("Expected type {} for arg 'start', got {}".format(Point, type(start)))
        self._vertices      = [ Point( start.x, start.y ) ]

        self.color          = (0.0, 0.0, 0.0)
        self._step_calc     = False
        self._step          = None 
    def end(self, offset=0):
        if len(self._vertices)==0:
            return(None)
        else:
            return( Point( self._vertices[-1-offset].x, self._vertices[-1-offset].y ) )

    @property
    def vertices(self):
        """
        The points defining this path. Returns a copy! 
        """
        built = []
        for vert in self._vertices:
            built.append( Point( vert.x, vert.y ) )
        return( built)
    
    def trim_at( self, where):
        p_type = False 
        if isinstance( where, int ):
            p_type = True
        elif not isinstance( where , Point ):
            raise TypeError("Arg 'where' must be type {}, received {}".format( Point, type(where)))
        
        if p_type:
            which_index = where
        else:
            try:
                which_index = self._vertices.index( where )
            except ValueError:
                raise ValueError("Point {} is not in list of vertices for obj {}".format(where, type(self)))

        
        # this leaves the self-intersect point there. Good!
        self._vertices = self._vertices[which_index:]


    def add_to_end( self, end ):
        """
        Append Point to end of path

        @param end  - object of type Point
        """
        if not isinstance( end, Point):
            raise TypeError("Expected type {} for arg 'end', got {}".format( Point, type(end )))

        if not self._step_calc:
            # get the magnitude between the last point and the one we're adding, that's the step size 
            self._step = ( end - self.end() ).magnitude 
            self._step_calc = True 
        else:
            # if the difference between this step and the precalculated step is >1%, raise an exception! 
            if (( end - self.end() ).magnitude - self._step)/self._step  > 0.01:
                print("Step of {}".format( (end-self.end()).magnitude ))
                print("Expected {}".format(self._step))
                print("From {} to {}".format(self.end(), end))
                raise ValueError("Paths must have consistently spaced entries")

        self._vertices.append( end )

    def add_to_start( self, start):
        """
        Append Point to start of path
        
        @param start    - object of type Point 
        """
        if not isinstance( end, Point):
            raise TypeError("Expected type {} for arg 'end', got {}".format( Point, type(end )))

        if not _step_calc:
            # get the magnitude between the last point and the one we're adding, that's the step size 
            self._step = ( end - self._vertices[0] ).magnitude 
            self._step_calc = True 
        else:
            # if the difference between this step and the precalculated step is big, raise an exception! 
            if (( end - self._vertices[0] ).magnitude - self._step)/self._step  > 0.01:
                raise ValueError("Paths must have consistently spaced entries")


        self._vertices = [ start ] + self._vertices

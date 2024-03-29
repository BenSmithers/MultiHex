from PyQt5 import QtCore, QtWidgets
from MultiHex.objects import Entity, Mobile

try:
    from numpy import sqrt, atan, pi, floor, cos, sin, inf
except ImportError:
    from math import sqrt, atan, pi, floor, cos, sin, inf

import os, json, sys
from collections import deque
import pickle

from MultiHex.logger import Logger

"""
Ben Smithers
b.smithers.actual (at) gmail.com 

Core objects for MultiHex

Objects:
    Point           - 2D vector with associated operators
    HexMap          - base upon which all the maps are built
        construct_id 
        deconstruct_id 
    Region          - A perimeter, lists of IDs associated with it, and means to modify this
        glom
    Path            - path traveling between vertices. Generic implementation of roads/rivers/etc
"""

multihex_version = "0.3.0"
map_version = "0.5"


def is_number(object):
    return( isinstance(object, int) or isinstance(object,float) )

class Point:
    """
    A vector in 2D Cartesian space.

    @x          - x component of vector
    @y          - y component of vector
    @magnitude  - length of this vector
    """
    def __init__(self, x =0.0, y=0.0):
        if not is_number(x):
            raise TypeError("Expected type {} for arg 'x', received {}".format(float, type(x)))
        if not is_number(y):
            raise TypeError("Expected type {} for arg 'y', received {}".format(float, type(y)))

        # protected vector components
        self._coords = [x,y]

        # use the bool so that we only have to calculate the magnitude once 
        self._mcalculated   = False
        self._magnitude     = 0.0
        
        self._acalculated   = False
        self._angle         = 0.0

    @property
    def coords(self):
        built = [ value for value in self._coords]
        return(built)

    def normalize(self):
        for element in range(len(self._coords)):
            self._coords[element] /= self.magnitude

        self._magnitude = 1.0


    def __add__(self, obj):
        """
        Used to add a point to another one through vector addition 
        """
        if not isinstance(obj, Point):
            raise TypeError("Cannot add type {} to Point object".format(type(obj)) )

        new = self.__class__()
        new._coords = [ self._coords[component] + obj._coords[component] for component in range(len(self._coords))]
        return( new )

    def __sub__(self, obj):
        """
        Same as addition, but for subtraction
        """
        new = self + (obj*-1)
        return( new )

    def __mul__(self, obj):
        """
        Calculate the inner product of two vector-points, or scale one vector-point by a scalar. 
        """
        if is_number(obj):
            new = self.__class__()
            new._coords = [obj*coord for coord in self.coords]
            return( new )
        elif isinstance(obj, Point):
            value = 0.0
            for comp in range(len(self._coords)):
                # support dotting a high-dimensionality Point with one in a lower dimension
                if comp>=len(obj._coords):
                    break
                else:
                    value += self._coords[comp]*obj._coords[comp]
            return( value)
        else:
            raise TypeError("Cannot multiply type {} with Point object".format(type(obj)))

    def __eq__(self, obj):
        if isinstance(obj, Point):
            is_same = True
            if len(self._coords)!=len(obj._coords):
                return(False)

            for comp in range(len(self._coords)):
                is_same &= abs(self._coords[comp] - obj._coords[comp])<0.01
                if not is_same:
                    return(False)
            return( is_same )
        else:
            return(False)
    def __truediv__(self, obj):
        if not is_number(obj):
            raise TypeError("Cannot divide Point by object of type '{}'".format(type(obj)))
        else:
            return( self*(1./obj) )
    
    def __pow__(self, obj):
        if not is_number(obj):
            raise TypeError("Cannot raise vector to a non-number power")
        else:
            # returns a scalar! 
            partial_sum = 0.0
            for comp in range(len(self._coords)):
                partial_sum += self._coords[comp]**obj

            return( partial_sum )

    # functions used to access vector components

    @property
    def x(self):
        copy = self._coords[0]
        return( copy )

    @property
    def y(self):
        copy = self._coords[1]
        return( copy )

    @property
    def magnitude(cls):
        """
        Return the magnitude of the vector. If it hasn't been calculated, calculate it.
        """
        if cls._mcalculated:
            return( cls._magnitude )
        else:
            cls._magnitude = sqrt( cls**2 )
            cls._mcalculated = True
            return(cls._magnitude)
    
    @property
    def angle(cls):
        """
        returns the planar angle of the vector as measured from the x-axis. Calculates only once
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

class Point3d(Point):
    """
    Implements the 2D point but now in 3D. 
    
    Distinct so as to save memory 
    """
    def __init__(self, x=0., y=0., z=0.):
        Point.__init__(self, x, y)
        if not is_number(z):
            raise TypeError("Expected type {} for arg 'z', received {}".format(float, type(z)))
        self._coords.append(z)

    @property
    def z(self):
        copy = self._coords[2]
        return( copy )
        

class PointNd( Point ):
    """
    Implements the 2D point but now with arbitrary dimensionality

    Does not allow for easy access functions like .z 
    """
    def __init__(self, *coords):
        Point.__init__(self, 0,0)

        if not (isinstance( coords, list) or isinstance(coords,tuple)):
            raise Exception("Coordinates need to be specified as {}, got {}".format(list, type(coords)))

        # if we receive a single list-like argument ([x,y,z,w,...]), parse it as our coordinates 
        if len(coords)==1 and (isinstance(coords[0],list) or isinstance(coords[0],tuple)):
            self._coords = coords[0]
        else:
            # otherwise the arguments were passed variable-style (x,y,z,w,...) and we parse that list as our coordinates
            self._coords = coords

        for entry in self.coords:
            if not (isinstance( entry, float) or isinstance( entry, int )):
                raise TypeError("Each coordinate should be number-like, got {}".format( type(entry)))

        


    def __str__(self):
        out = ""
        for comp in self.coords:
            if out!="":
                out = out+", "
            out+="{:.2f}".format(comp)

        return("("+out+")")




default_p = Point(0.0,0.0)
rthree = sqrt(3)

class Hex:
    """
    Datastructure to represent a single hex on a hex map

    @ build_name            - creates a name for hex biome - not implemented
    """
    def __init__(self, center=default_p, radius=1.0 ):
        if not isinstance(center, Point):
            raise TypeError("Arg 'center' must be of type {}, received {}".format( Point, type(center)))
        if not (isinstance(radius, float) or isinstance(radius, int)):
            raise TypeError("Arg 'radius' must be {}, received {}".format(float, type(radius)))
        
        self._center = center
        self._radius = radius
        
        self._outline= (240,240,240)
        self._fill   = (100,100,100) 

        # used in procedural generation
        self.genkey            = '00000000'

    @property
    def outline(self):
        return self._outline
    
    @property
    def fill(self):
        return self._fill

    def get_cost(self, other):
        """
        Default get_cost function. 
        Should be reimplemented in derived classes. 
        """
        raise NotImplementedError('subclasses must override')

    def get_heuristic(self, other):
        """
        Tries to predict the total cost of stepping to a distant Hex
        """
        raise NotImplementedError('subclasses must override')

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
            
    def __eq__(self, other):
        same = self.center==other.center and self.radius==other.radius \
            and self.outline==other.outline and self.fill==other.fill
        return(same)

    def __repr__(self):
        return("{}@{}".format("Hex", self.center))


    


def _update_to_0_1( which ):
    """
    Updates hexmap from before version numbering to the first numbered version 
    """
    which._version = "0.1"
    which.__class__ = Hexmap
    _update_to_0_2(which)
def _update_to_0_2(which):
    def update_point( this ):
        setattr( this, "_coords", [this._x, this._y ])
        this.__class__ = Point

    which._version = "0.2"
    # go to every hex, update it to use the new point
    update_point( which.draw_relative_to)
    update_point( which.origin_shift )
    # update all the verices on the hexes... and their centers
    for hexid in which.catalog:
        for i in range(6):
            #update_point( which.catalog[hexid]._vertices[i] )
            update_point( which.catalog[hexid]._center )
    # update the perimeter of all regions
    for r_layer in which.rid_catalog:
        for rid in which.rid_catalog[r_layer]:
            for vert in range(len(which.rid_catalog[r_layer][rid].perimeter)):
                update_point( which.rid_catalog[r_layer][rid].perimeter[vert] )
            # update the enclaves
            for enclave in which.rid_catalog[r_layer][rid].enclaves:
                for vert in enclave:
                    update_point(vert)

    def update_path( this_one):
        for vert in range(len( this_one._vertices)):
            update_point( this_one._vertices[vert] )
        if hasattr( this_one, "tributaries"):
            if this_one.tributaries is not None:
                update_path( this_one.tributaries[0] )
                update_path( this_one.tributaries[1] )

    # update the vertices on all the paths. Rivers have tributaries, so we update those (recursively)
    for p_layer in which.path_catalog:
        for pid in which.path_catalog[p_layer]:
            update_path( which.path_catalog[p_layer][pid] )
    _update_to_0_3(which)

def _update_to_0_3(which):
    which._version = "0.3"
    which.__class__ = Hexmap
    setattr( which, "_tileset", "standard")
    _update_to_0_4(which)

def _update_to_0_4(which):
    # need to update the hexes, the points
    
    # update hexes
    which._version = "0.4"
    for hexID in which.catalog:
        del which.catalog[hexID]._vertices
    _update_to_0_5(which)

def _update_to_0_5(which):
    which._version = "0.5"
    setattr(which, "catalog", which.catalogue)
    setattr(which, "rid_catalog", which.rid_catalogue)
    setattr(which, "eid_catalog", which.eid_catalogue)

def _update_save(which):
    """
    This function figures out the version mismatch of the given Hexmap and applies necessary updates
    """
    assert( isinstance( which, Hexmap ))
    Logger.Log("Updating Map")
    if not hasattr( which, "_version"):
        _update_to_0_1( which )
        
    elif which.version < map_version:
        if which._version == "0.1":
            _update_to_0_2( which )
        if which._version == "0.2":
            _update_to_0_3(which)
        elif which._version=="0.3":
            _update_to_0_4(which)
        elif which._version=="0.4":
            _update_to_0_5(which)

    elif which.version > map_version:
        raise NotImplementedError("Trying to load HexMap version {} with MultiHex version {}".format(which.version, map_version))
    
    Logger.Log("Updated map to version {}. You should save!".format(map_version))
    

def save_map(h_map, filename):
    h_map.drawn_hexes = {}
    h_map._active_id = None
    h_map._outline = None
    h_map.outline_obj = None

    file_object = open(filename, 'wb')
    pickle.dump( h_map, file_object, -1)
    file_object.close()

def load_map(filename):
    file_object = open(filename, 'rb')
    hex_pickle = pickle.load(file_object)
    file_object.close()

    # need to make sure that the loaded hexmap is up to date! 
    if not hasattr(hex_pickle, "_version"):
        _update_save( hex_pickle )
    elif hex_pickle.version != map_version:
        _update_save( hex_pickle )

    return( hex_pickle )


class Hexmap:
    """
    Object to maintain the whole hex catalog, draw the hexes, registers the hexes

    Methods:
    @ remove_hex            - unregister hex from catalog
    @ register_hex          - register a hex in the catalog
    @ get_hex_neighbors         - get list of IDs for hexes neighboring this one
    @ get_neighbor_outline      - retursn list of points to outline cursor 
    @ points_to_draw        - takes list of map-Points, prepares flattened list of draw coordinates 
    @ get_id_from_point     - constructs neares ID to point
    @ get_point_from_id     - constructs point from ID
    @ register_new_region   - takes a region, registers it in the rid_catalog with a unique region id (rid)
    @ add_to_region         - adds a single hex to a region
    @ remove_from_region    - removes hex from region
    @ merge_regions         - takes two rids, merges the regions

    Attributes:
    @ catalog             - Dictionary of hexes. The hexIDs are keys to the hexes themselves 
    @ rid_catalog         - 2-level dictionary: rid_catalog[ layer ][ rID ]. Points to region object 
                                + layer is the region layer (biome/kingdom/etc)
                                + rID is the identifier of the region
    @ id_map                - similar data structure as rid_catalog. Region layer and hexID returns rID hex belongs to. Raises key error if no association! 
    @ rivers                - dictionary containing lists of paths. Dict key for path type 
    @ drawscale             - scaling factor of entire map. Establishes hex size 
    """
    def __init__(self):
        self.catalog = {}
        
        self.rid_catalog = {} #region_id -> region object
        self.id_map = {} # hex_id -> reg_id 
        
        # catalog of entities
        self.eid_catalog = {} # eID -> Entity obj
        self.eid_map = {} # hex_id -> [ list of eIDs ]

        self.path_catalog = {}

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

        self._tileset = "standard"
        self._version = map_version 

        self.dimensions = None

    @property
    def tileset(self):
        return(self._tileset)
    
    def set_tileset(self, new):
        """
        Change the map's tileset to one of the definitions in the tilesets json file
        """
        if not isinstance(new,str):
            raise TypeError("Expected {}, got {}".format(str, type(new)))

        loc = os.path.join(os.path.dirname(__file__) ,'resources', 'tilesets.json')
        file_object = open( loc, 'r')
        config = json.load( file_object )
        file_object.close()

        if new not in config:
            raise ValueError("Unrecognized tileset {}".format(new))

        self._tileset = new

    @property 
    def version(self):
        return( self._version )

    @property 
    def drawscale(self):
        copy = self._drawscale
        return( copy )

    def _get_cost_between(self, start_id, end_id):
        """
        Function for calculating the movement cost between neighboring hexes 
        Used by the get_route_between_hexes functionm

        -> does not account for locations on map. This is just a raw distance, not including getting closer to the final destination 
        """
        if start_id not in self.catalog:
            raise KeyError("start_id {} not in catalog!".format(start_id))
        if end_id not in self.catalog:
            return(inf)

        start_neighs = self.get_hex_neighbors(start_id)
        if end_id not in start_neighs:
            return(inf) #you can't teleport. This is an infiinite cost move...

        # We need to be able to have type-specific cost implementations. The Hexmap does not know what kind of map it is
        # So the Hexes themselves will be responsible for calculating the cost.
        # Subtypes of Hexes will implement unique cost functions 

        start_hex = self.catalog[start_id]
        return(start_hex.get_cost( self.catalog[end_id]))

    def _get_heuristic(self, start_id, end_id):
        if not isinstance(start_id, int):
            raise TypeError("IDs are of type {}, got {}".format(int, type(start_id)))
        if not isinstance(end_id, int):
            raise TypeError("IDs are of type {}, got {}".format(int, type(end_id)))
        if start_id not in self.catalog:
            raise ValueError("Start ID {} not found in catalog!".format(start_id))
        if end_id not in self.catalog:
            raise ValueError("End ID {} not found in catalog!".format(end_id))

        return( self.catalog[start_id].get_heuristic(self.catalog[end_id]) )


    def get_route_a_star(self, start_id, end_id):
        """
        Finds quickest route between two given HexIDs. Both IDs must be on the Hexmap.
        Always steps closer to the target

        Returns ordered list of HexIDs representing shortest found path between start and end (includes start and end)
        """
        if not isinstance(start_id, int):
            raise TypeError("IDs are of type {}, got {}".format(int, type(start_id)))
        if not isinstance(end_id, int):
            raise TypeError("IDs are of type {}, got {}".format(int, type(end_id)))
        if start_id not in self.catalog:
            raise ValueError("Start ID {} not found in catalog!".format(start_id))
        if end_id not in self.catalog:
            raise ValueError("End ID {} not found in catalog!".format(end_id))


        openSet = deque([start_id])
        cameFrom = {}

        gScore = {}
        gScore[start_id] = 0.

        fScore = {}
        fScore[start_id] = self._get_heuristic(start_id,end_id)

        def reconstruct_path(cameFrom, current):
            total_path = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                total_path.append(current)
            
            return(total_path[::-1])

        while len(openSet)!=0:
            # find minimum fScore thing in openSet
            min_id = None
            min_cost = None
            current = openSet[0]

            if current==end_id:
                return reconstruct_path(cameFrom, current)

            openSet.popleft()
            for neighbor in self.get_hex_neighbors(current):
                try:
                    tentative_gScore = gScore[current] + self._get_cost_between(current, neighbor)
                except KeyError:
                    tentative_gScore = inf

                if neighbor in gScore:
                    neigh = gScore[neighbor]
                else:
                    neigh = inf

                if tentative_gScore < neigh:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self._get_heuristic(neighbor,end_id)
                    if neighbor not in openSet:

                        if len(openSet)==0:
                            openSet.appendleft(neighbor)
                        else:
                            iter = 0
                            while fScore[neighbor]>fScore[openSet[iter]]:
                                iter += 1
                                if iter==len(openSet):
                                    break

                            openSet.insert(iter,neighbor)
        return([])

    
    def get_region_neighbors( self, rID, layer):
        """
        Returns the Region IDs of those regions neighboring the provided Region with ID `rID`
        """
        if layer not in self.rid_catalog:
            raise ValueError("Layer {} not in catalog.".format(layer))
        if not isinstance(rID, int):
            raise TypeError("Invalid rID of type {}".format(type(rID)))
        if rID not in self.rid_catalog[layer]:
            raise ValueError("Region {} not in catalog.".format(rID))

        this_region = self.rid_catalog[ layer ][rID]
        if not this_region.known_neighbors:
            # if this region's neighbors are unknown, let's find them! 
            
            neighbor_rids = [ ]
            vertices = this_region.perimeter
            # go around the perimeter
            for iter in range(len(vertices)):
                inside_id, outside_id = self.get_ids_beside_edge( vertices[iter], vertices[(iter+1) %len(vertices)])
            
                try:
                    new_rid = self.id_map[layer][outside_id]
                    if new_rid not in neighbor_rids:
                        neighbor_rids.append( new_rid )
                except KeyError:
                    continue

            for enclave in this_region.enclaves:
                # enclave is a list of points
                for iter in range(len(enclave)):
                    inside_id, outside_id = self.get_ids_beside_edge( enclave[iter], enclave[(iter+1) %len(enclave)])
                    try:
                        new_rid = self.id_map[layer][outside_id]
                        if new_rid not in neighbor_rids:
                            neighbor_rids.append( new_rid )
                    except KeyError:
                        continue

            # Failing this assertion would imply that there's an issue with the way we look for hexes _outside_ this Region
            assert( rID not in neighbor_rids )
            this_region.neighbors = neighbor_rids
            this_region.known_neighbors = True

        return( this_region.neighbors )


    def register_new_path( self, target_path , layer):
        if not isinstance( target_path, Path):
            raise TypeError("{} not of type {}, it's a {}!".format(target_path, Path, type(target_path)))

        new_pID = 0
        if layer not in self.path_catalog:
            self.path_catalog[layer] = {}

        while new_pID in self.path_catalog[layer]:
            new_pID += 1

        self.path_catalog[layer][ new_pID ]  = target_path 

        return( new_pID )

    def unregister_path( self, pID, layer):
        if not type(pID)==int:
            raise TypeError("Expected {} for rivid, got {}".format(int, type(pID)))
        
        if layer not in self.path_catalog:
            raise ValueError("{} is not a layer in the path catalog".format( layer))

        if pID not in self.path_catalog[layer]:
            raise ValueError("pID {} not in Path catalog".format(pID))

        del self.path_catalog[layer][pID] 


    def register_new_entity( self, target_entity):
        """
        Registers a new entity with the Entity catalog and map

        @param target_entity    - the Entity
        """
        if not isinstance( target_entity, Entity):
            raise TypeError("Cannot register non-Entity of type {}".format( type(target_entity)) )
       
        if (target_entity.location is not None) and (target_entity.location not in self.catalog):
            # -1 represents 'outside' the map! 
            target_entity.set_location = -1 

        new_eid = 0 
        while new_eid in self.eid_catalog:
            new_eid += 1

        
        self.eid_catalog[ new_eid ] = target_entity 
        
        # you can register an entity without it being in the map
        if target_entity.location in self.catalog:
            if target_entity.location not in self.eid_map:
                self.eid_map[target_entity.location] = [ new_eid ]
            else:
                self.eid_map[target_entity.location].append( new_eid )

        return( new_eid )
    
    def move_mobile( self, eID, new_location):
        """
        Moves the Mobile from where it is to the new location
        
        @param eID  - the eID of the Mobile to move 
        @param new_location     - the hexID of the new location
        """
        if not isinstance( eID, int):
            raise TypeError("eID provided is of type {}, should be of type {}".format(type(eID), int))
        if eID not in self.eid_catalog:
            raise ValueError("No registered entity of eID {}".format(eID))

        if not isinstance( self.eid_catalog[eID], Mobile):
            raise TypeError("Cannot mobe object of type {}. Only {} objects can move".format( type(self.eid_catalog[eID]), Mobile))

        curr_id = self.eid_catalog[eID].location

        # removing Entity from the map. That's fine
        if curr_id not in self.catalog:
            # this is fine, curr_id could be None
            pass 
        else:
            # Remove its previous map location associaiton
            if curr_id not in self.eid_map:
                raise ValueError("Mobile no {} thought it was here: {}. No entry for this ID in eID_map!".format(eID, curr_id))
            else:
                if eID not in self.eid_map[curr_id]:
                    raise ValueError("Mobile with eID {} thought it was here: {}. Hex only contains eIDs {}".format(eID, curr_id, self.eid_map[curr_id]))
                else:
                    # remove the mapping to this entity from its old location
                    self.eid_map[curr_id].pop( self.eid_map[curr_id].index( eID ) )
            # After this, if there are no more entities at this Hex, just remove the mapping! 
            if len(self.eid_map[curr_id])==0:
                del self.eid_map[curr_id]
        
        # this just changes the location that the Mobile has for itself 
        self.eid_catalog[eID].set_location(new_location)

        if new_location not in self.catalog:
            new_location = -1 

        if new_location in self.eid_map:
            self.eid_map[ new_location ].append( eID )
        else:
            self.eid_map[ new_location ] = [ eID ]


    def remove_entity( self, eID ):
        """
        Removes the entity with the given eID. Updates both the eid_catalog and the eid_map

        @param eID  - the eID of the Entity to remove. Deletes the entity! 
        """

        if not isinstance( eID, int):
            raise TypeError("eID provided is of type {}, should be of type {}".format(type(eID), int))
        if eID not in self.eid_catalog:
            raise ValueError("No registered entity of eID {}".format(eID))

        # first remove the entity from the eid_map
        ent = self.eid_catalog[ eID ]
        loc_id = ent.location 

        # Entity may not have a location.     
        if loc_id not in self.eid_map:
            # that means the Entity thought it was somewhere that the Map thought had nothing

            Logger.Warn("Inconsistency in eIDs")
        else:
            if eID not in self.eid_map[loc_id]:
                # means that the Entity thought it was somewhere that the Map that had some things, just not this thing 
                Logger.Warn("Inconsistency in eIDS (2)")
            else:
                # otherwise remove the eID from this list 
                self.eid_map[loc_id].pop( self.eid_map[loc_id].index( eID ) )

            # if we removed the last entity from this hex then delete the entry 
            if len( self.eid_map[loc_id] )==0:
                del self.eid_map[loc_id]
        
        # delete the entity from the catalog 
        del self.eid_catalog[ eID ]

    def get_next_rid(self, r_layer:str)->int:
        if r_layer not in self.id_map:
            self.id_map[r_layer] = {}
        if r_layer not in self.rid_catalog:
            self.rid_catalog[r_layer] = {}

        new_rid = 1
        while new_rid in self.rid_catalog[r_layer]:
            new_rid += 1

        return new_rid

    def register_new_region( self, target_region, r_layer ):
        """
        Registers a new region with this Hexmap. Adds it to the dictionaries, give it a unique rID, and set up all the maps for its contained Hexes 
        """


        # make sure this region layer exists. If it doesn't, let's make it. 
        if r_layer not in self.id_map:
            self.id_map[r_layer] = {}
        if r_layer not in self.rid_catalog:
            self.rid_catalog[r_layer] = {}

        # verify that the target region doesn't have any hexes already belonging to a registered region
        for hex_id in target_region.ids:
            if hex_id in self.id_map[r_layer]:
                raise KeyError("Region contains hex {} belonging to other region: {}".format(hex_id, self.id_map[r_layer][hex_id]))

        # first settle on a new rid - want the smallest, unused rid 
        new_rid = self.get_next_rid(r_layer)
        
        target_region.set_color( new_rid )
        # register the region in the hexmap's region catalog 
        self.rid_catalog[r_layer][ new_rid ] = target_region
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
        if r_layer not in self.rid_catalog:
            raise KeyError("Region layer {} does not exist.".format(r_layer))

        # throws KeyError if rID not in catalog
        # we aren't handling that error. Downstream problem...
        if rID not in self.rid_catalog[r_layer]:
            raise KeyError("Region no. {} not recognized.".format( rID) )
        if hex_id not in self.catalog:
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
        self.rid_catalog[r_layer][ rID ].add_hex_to_self( hex_id )
        self.id_map[r_layer][ hex_id ] = rID

        return(other_rid)

    def remove_from_region( self, hex_id, r_layer ):
        """
        Removes a hex from a region

        @param hex_id   - ID of hex from which to remove region affiliation 
        @param r_layer  - string (key) for the desired region layer
        """
        if r_layer not in self.rid_catalog:
            raise KeyError("Region layer {} does not exist.".format(r_layer))

        # removes the hex_id from whichever region it's in
        if hex_id not in self.id_map[r_layer]:
            raise KeyError("Hex no. {} not registered".format(hex_id))
        
        if len(self.rid_catalog[r_layer][ self.id_map[r_layer][hex_id] ].ids )==1:
            # if this is the last hex in the region, just delete this guy. It's the responsibility of the calling function to redraw the region (if desired)
            del self.rid_catalog[r_layer][self.id_map[r_layer][hex_id]]

        else:

            # update the region extents 
            self.rid_catalog[r_layer][ self.id_map[r_layer][hex_id] ].pop_hexid_from_self( hex_id )

            # delete the hexes' association to the now non-existent region
            del self.id_map[r_layer][hex_id]
        

    def merge_regions( self, rID_main, rID_loser, r_layer ):
        """
        Merges two regions

        @param rID_main  - rID of region which will accept the hexes from rID_loser
        @param rID_loser - rID of region which will be absorbed into rID_main
        @param r_layer   - string (key) for the desired region layer. Eg - biome, border, ...
        """
        if r_layer not in self.rid_catalog:
            raise KeyError("Region layer {} does not exist.".format(r_layer))

        if (rID_main not in self.rid_catalog[r_layer]):
            raise KeyError ("Region {} not recognized".format(rID_main))
        if (rID_loser not in self.rid_catalog[r_layer]):
            raise KeyError("Region {} not recognized".format(rID_loser))
         
        # merge second region into first one
        self.rid_catalog[r_layer][ rID_main ].merge_with_region( self.rid_catalog[r_layer][rID_loser] )
        
        # update the entries in the id_map to point to the new region
        for hex_id in self.rid_catalog[r_layer][rID_loser].ids:
            self.id_map[r_layer][ hex_id ] = rID_main

        # delete the old regionNone
        del self.rid_catalog[r_layer][ rID_loser ]


    def remove_hex( self, target_id):
        """
        Try popping a hex from the catalog. Deletes the key, deletes the hex. 

        @param target_id - the ID of the removed hex
        """ 
        del self.catalog[target_id]
        if target_id == self._active_id:
            self._active_id = None
        elif self._party_hex == self._active_id:
            pass

    def register_hex(self, target_hex, new_id ):
        if not isinstance(target_hex, Hex):
            raise TypeError("Can only register {} objects".format(Hex))
        assert( target_hex._radius == self.drawscale )
        if not isinstance(new_id, int):
            raise TypeError("ID must be {} type, not {}".format(int, type(new_id)))

        if new_id in self.catalog:
            raise NameError()
            temp_altitude = self.catalog[new_id]._altitude_base
            temp_temp     = self.catalog[new_id]._temperature_base
            self.catalog[new_id] = target_hex
            self.catalog[new_id]._altitude_base = temp_altitude
            self.catalog[new_id]._temperature_base = temp_temp
        else:
            self.catalog[new_id] = target_hex

    def remove_region(self, rid, r_layer):
        if not isinstance(rid, int):
            raise TypeError("Expected type {} for arg `int`, got{}".format(int, type(rid)) )
        if rid not in self.rid_catalog[r_layer]:
            raise KeyError("Region ID {} not in catalog".format(rid))

        for ID in self.rid_catalog[r_layer][rid].ids:
            try:
                del self.id_map[r_layer][ID]
            except KeyError:
                pass
         
        del self.rid_catalog[r_layer][rid] 


    def set_active_hex(self, id):
        # totally deprecated... I think 

        if self._active_id is not None:
            self.catalog[self._active_id].outline = '#ddd'
        
        self._active_id = id
        self.catalog[self._active_id].outline = '#f00'
    
    def get_hex_neighbors(self, ID, radius=1):
        """
        Calculates the IDs of a given Hexes' neighbors
        NOTE: Neighbors not guaranteed to exist! 

        @param ID - ID of center
        @param radius - how far out from which to collect neighbors 

        @returns a LIST of IDs 
        """
        if not isinstance(radius,int):
            raise TypeError("Arg 'radius' must be {}, got {}".format(int, type(radius)))
        if radius<1:
            raise ValueError("Invalid radius {}".format(0))

        # convert the id to a bit string
        x_id, y_id, grid = deconstruct_id(ID)

        neighbors = [0 for i in range(radius*6)]

        # returns IDs starting from up and to the left, and going around clockwise 
        if radius==1:
            if grid:
                neighbors[0]=construct_id(x_id-1, y_id,   not grid) 
                neighbors[1]=construct_id(x_id, y_id+1, grid) 
                neighbors[2]=construct_id(x_id,   y_id,   not grid) 
                neighbors[3]=construct_id(x_id,   y_id-1, not grid) 
                neighbors[4]=construct_id(x_id, y_id-1, grid) 
                neighbors[5]=construct_id(x_id-1, y_id-1, not grid)
            else:
                neighbors[0]=construct_id(x_id,   y_id+1,   not grid) 
                neighbors[1]=construct_id(x_id,   y_id+1, grid) 
                neighbors[2]=construct_id(x_id+1, y_id+1,   not grid) 
                neighbors[3]=construct_id(x_id+1, y_id,     not grid) 
                neighbors[4]=construct_id(x_id,   y_id-1, grid) 
                neighbors[5]=construct_id(x_id,   y_id,     not grid) 
            return(neighbors)    
        else:
            
            center = self.get_point_from_id(ID)
            angles = [ float(iter)*2*pi/len(neighbors) for iter in range(len(neighbors)) ]
            for iter in range(len(neighbors)):
                step= Point(sin(angles[iter]) , cos(angles[iter]))*self.drawscale*(rthree*radius)
                neighbors[iter] = self.get_id_from_point( Point( center.x + step.x, center.y+ step.y)  )
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
            perimeter_points +=[ center + Point( -0.5, 0.5*rthree)*self.drawscale]
            perimeter_points +=[ center + Point(  0.5, 0.5*rthree)*self.drawscale]
            perimeter_points +=[ center + Point(  1.0, 0.0)*self.drawscale]
            perimeter_points +=[ center + Point(  0.5,-0.5*rthree)*self.drawscale]
            perimeter_points +=[ center + Point( -0.5,-0.5*rthree)*self.drawscale]
            perimeter_points +=[ center + Point( -1.0, 0.0)*self.drawscale]
            return(perimeter_points)
        else:
            # these are shifts to the three unique vertices on the Northern Hexes' outer perimeter
            vector_shift = [ Point(self.drawscale, self.drawscale*rthree),Point(self.drawscale*0.5, 3*rthree*0.5*self.drawscale) , Point(-self.drawscale*0.5, 3*rthree*0.5*self.drawscale)] 
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
            l_up    = self.get_id_from_point( vertex+Point( -0.5*self.drawscale,   rthree*0.25*self.drawscale ))
            l_down  = self.get_id_from_point( vertex+Point( -0.5*self.drawscale,-1*rthree*0.25*self.drawscale ))
            r_up    = self.get_id_from_point( vertex+Point(  0.5*self.drawscale,   rthree*0.25*self.drawscale ))
            r_down  = self.get_id_from_point( vertex+Point(  0.5*self.drawscale,-1*rthree*0.25*self.drawscale ))

            if l_up==l_down:
                v_type = 2
            elif r_up==r_down:
                v_type = 1
            else:
                raise ValueError("Not sure if {} is a vertex...".format(vertex) )
        

        assert( type(v_type) == int)

        if v_type==1:
            neighbors = [   vertex + (Point(-1.0,  0.0       )*self.drawscale), 
                            vertex + (Point( 0.5,  0.5*rthree)*self.drawscale), 
                            vertex + (Point( 0.5, -0.5*rthree)*self.drawscale) ]
        elif v_type==2:
            neighbors = [   vertex + (Point( 1.0,  0.0       )*self.drawscale), 
                            vertex + (Point(-0.5,  0.5*rthree)*self.drawscale), 
                            vertex + (Point(-0.5, -0.5*rthree)*self.drawscale) ]

        else:
            raise ValueError("Unrecognized vertex type {}".format(v_type))

        return( neighbors )

    def get_ids_around_vertex( self, place, v_type = None):
        """
        This returns three IDs. It is assumed that `place` is a vertex. will return inconsistent results otherwise 

        @param place    - Point type object. Should be a vertex of a hex in a hexmap
        @param v_type   = optional argument. Specify the vertex type (see below) to save time in calculating it 
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
            Logger.Warn("This shouldn't be called")
            # deduce the vertex type
            l_up    = self.get_id_from_point( place+Point( -0.25*self.drawscale,   rthree*0.25*self.drawscale ))
            l_down  = self.get_id_from_point( place+Point( -0.25*self.drawscale,-1*rthree*0.25*self.drawscale ))
            r_up    = self.get_id_from_point( place+Point(  0.25*self.drawscale,   rthree*0.25*self.drawscale ))
            r_down  = self.get_id_from_point( place+Point(  0.25*self.drawscale,-1*rthree*0.25*self.drawscale ))

            if l_up==l_down:
                v_type = 2
                #return([ l_up, r_up, r_down]) # type 2
            elif r_up==r_down:
                v_type=1
                #return([ l_up, l_down, r_up]) # type 1
            else:
                Logger.Fatal("I don't think this place, {}, is a vertex".format(place), ValueError)
        
        assert(type(v_type)==int)
        if v_type==1:
            return([    self.get_id_from_point( place + Point(1.0 ,  0.0       )*self.drawscale ), 
                        self.get_id_from_point( place + Point(-0.5,  0.5*rthree)*self.drawscale ),
                        self.get_id_from_point( place + Point(-0.5, -0.5*rthree)*self.drawscale ) ])
        elif v_type==2:
            return([    self.get_id_from_point( place + Point(-1.0 , 0.0       )*self.drawscale ), 
                        self.get_id_from_point( place + Point( 0.5,  0.5*rthree)*self.drawscale ),
                        self.get_id_from_point( place + Point( 0.5, -0.5*rthree)*self.drawscale ) ])

        else:
            Logger.Fatal("Invalid Vertex type value: {}".format(v_type), ValueError)

    def get_ids_beside_edge(self, start, end):
        """
        Returns a pair of hexIDs to the left and right of the edge defined by 'start' and 'end'

        @param start    - type Point, defines start of edge
        @param end      - type Point, defines end of edge 

        start and end should be drawscale apart
        """
        
        # verify the arguments passed are of the right type: `Point` 
        if type(start)!=Point:
            raise TypeError("Arg 'start' is not type point, it is {}".format(start))
        if type(end)!=Point:
            raise TypeError("Arg 'end' is not type point, it is {}".format( end ))

        # verify that this edge is the right length (drawscale)
        diff = end - start 
        if (diff.magnitude - self.drawscale)/self.drawscale > 0.01:
            raise ValueError("Edge length is {}, expected {}".format( diff.magnitude, self.drawscale))
        # displacement vector from 'end' object. 
        #       points towards CW hex
         
        diag_cw  = start + diff*0.5 + Point( diff.y, -diff.x)*0.5*rthree*self.drawscale/diff.magnitude
        diag_ccw = start + diff*0.5 + Point(-diff.y,  diff.x)*0.5*rthree*self.drawscale/diff.magnitude
        return( self.get_id_from_point( diag_cw ) , self.get_id_from_point( diag_ccw ) )


    def get_id_from_point(self, point):
        """
        Function to return either nearest hex center, or ID
        """
        if type(point)!=Point:
            raise TypeError("{} is not a Point, it is {}".format(point, type(point)))


        # keep a copy of the untranslated point! 
        og_point = Point( point.x, point.y )
                
        base_idy = int(floor((point.y/( rthree*self.drawscale)) + 0.5) )
        base_idx = int(floor((point.x/(3.*self.drawscale)) + (1./3.)))
         
        # this could be the point 
        candidate_point =Point(base_idx*3*self.drawscale, base_idy*rthree*self.drawscale )

         # the secondary grid is shifted over a bit, so let's do the same again... 
        point -= Point( 1.5*self.drawscale, rthree*self.drawscale*0.5)

        # recalculate these
        base_idy_2 = int(floor((point.y/( rthree*self.drawscale)) + 0.5))
        base_idx_2 = int(floor((point.x/(3.*self.drawscale)) + (1./3.)))
        
        # this is in the off-grid
        candidate_point_2 =Point(base_idx_2*3*self.drawscale, base_idy_2*rthree*self.drawscale )
        candidate_point_2 += Point( 1.5*self.drawscale, rthree*self.drawscale*0.5)
        
        if (og_point - candidate_point)**2 < (og_point - candidate_point_2)**2:
            return( construct_id(base_idx, base_idy, True ))
        else:
            return( construct_id(base_idx_2, base_idy_2, False ))
    
    def get_vert_from_point(self, point):
        """
        Returns the closest vertex to the specified point

        @arg point - object of type Point
        """
        if not isinstance(point, Point):
            raise TypeError("Expected type {}, got {}. Ya dun goofed.".format(Point, type(point)))

        loc_id = self.get_id_from_point( point )
        here = self.get_point_from_id( loc_id )

        temp_hex = Hex( here, self.drawscale )
        verts = temp_hex.vertices
        
        which = 0
        dist = (verts[0]- point)**2

        for iter in range(len(verts)-1):
            this_dist = (verts[iter]-point)**2

            if this_dist<dist:
                which = iter
                dist = this_dist

        return( verts[which] )


    def get_point_from_id(self, id):
        """
        Returns the UNTRANSFORMED center of the hex corresponding to the given ID
        """

        x_id, y_id, on_primary_grid = deconstruct_id(id)
        
        # build the poin
        built_point = Point( x_id*3*self.drawscale, y_id*rthree*self.drawscale )
        if not on_primary_grid:
            # transform it if it's on the shifted grid
            built_point += Point( 1.5*self.drawscale, rthree*self.drawscale*0.5)
        
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

class RegionTab(QtWidgets.QWidget):
    def __init__(self, parent=None, config_region=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        if not isinstance(config_region, Region):
            Logger.Fatal("Expected {}, got {}".format(Entity, type(config_region)), TypeError)

        # color
        # name
        # symbol? 
        # Buttons to  add/remove hexes
        # delete button

        self.layout = QtWidgets.QFormLayout(self)
        self.namelbl = QtWidgets.QLineEdit(self)
        self.namelbl.setObjectName("namelbl")
        self.layout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.namelbl)

        self.colorbutton = QtWidgets.QPushButton(self)
        self.colorbutton.setObjectName("colorbutton")
        self.colorbutton.setText("Set Color")



        #self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.speed_lbl) #FieldRole SpanningRole

    def set_configuration(self, region):
        if not isinstance(region, Region):
            raise TypeError("Cannot configure object of type {}".format(type(region)))

    def get_configuration(self, region):
        if not isinstance(region, Region):
            raise TypeError("Cannot configure object of type {}".format(type(region)))

class Region:
    """
    A Region is a colleciton of neighboring of Hexes on a Hexmap. Regions are continuous.

    @ add_hex_to_self       - take the hex at hex_id and add its extent to this region
    @ merge_with_region     - take the given region, merge with it
    @ cut_region_from_self  - remove the extent of any hexes in other region form self
    @ pop_hexid_from_self   - remove the extent of one hex from the self
    """

    def __init__(self, hex_id, parent):
        """
        Constructor for Region class

        @param hex_id   - int64_t, key for the starting Hex of the region in param `parent`s Hex catalog
        @param parent   - Hexmap containing this Region
        """
        if not isinstance( parent, Hexmap):
            raise TypeError("Arg `parent` must by type {}, received {}.".format(Hexmap, type(parent)))

        self.enclaves = [  ]
        self.ids = [ hex_id ]
        # regions don't know their own region_id. That's a hexmap thing
        # self.reg_id = 0
        self.name = ""

        self.color = (0, 0, 0)
        
        self.parent = parent
        # may throw KeyError! That's okay, should be handled downstream 
        self.perimeter = self.parent.catalog[hex_id].vertices
         
        self.known_neighbors = False
        self.neighbors = []

    def get_center_size(self):
        """
        Calculates and returns an approximate size of the region. 

        Returns tuple:
             - `center`     - Point representing approximate center
             - `extent`     - Point (as vector) representing length in X and Y
        """
        min_x = None
        max_x = None 
        min_y = None
        max_y = None

        # average all of the IDs positions to get an average point 
        center = Point(0.0, 0.0)
        for hex_id in self.ids:
            this_hex = self.parent.catalog[hex_id]
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
        """
        Sets the color of the region

        @param `number`    - which color to use
        """
        if not isinstance(number, int):
            raise TypeError("Expected arg of type {}, received {}".format(int, type(number)))

        self.color = region_colors[ number % len(region_colors) ]

    def add_hex_to_self( self, hex_id ):
        """
        Add the hex at `hex_id` in this region's Hexmap to this region
        """

        # build a region around this hex and merge with it
        if hex_id in self.ids:
            return #nothing to do...
        
        temp_region = self.__class__( hex_id , self.parent )
        self.merge_with_region( temp_region )
        self.known_neighbors = False 

    def merge_with_region( self, other_region ):
        """
        Takes another region and merges it into this one.

        @param other_region     - region to merge with this one
        """
        #TODO: prepare a write up of this algorithm 


        if not isinstance( other_region, Region):
            raise TypeError("Arg `other_region` is of type {}, expected {}".format(type(other_region), Region))

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
            loops = [_glom( self.perimeter, other_region.perimeter, ind ) for ind in start_indices]
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
                Logger.Trace("start indices: {}".format( start_indices ))
                Logger.Trace("Loops: {}".format(loops))
                Logger.Trace("self.perimeter: {}".format(self.perimeter))
                Logger.Trace("other one: {}".format(other_region.perimeter))
                Logger.Fatal("Some bad stuff has happened.")
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
                self.enclaves += [ _glom( enclave, other_region.perimeter, index) for index in start_indices ] 
            if not found_enclave:
                # the target region doesn't border an enclave and it doesn't border the perimeter.
                # we can't merge these
                raise RegionMergeError("Regions must share some border/enclave")

        # these are just added on in
        self.enclaves   += other_region.enclaves 
        self.ids        += other_region.ids
        self.known_neighbors = False 

    def cut_region_from_self( self, other_region):
        # the order these hexes are popped is suuuper important.
        # As is, this will lead to unexpected behavior!! 
        for ID in other_region.ids:
            if ID in self.ids:
                self.pop_hexid_from_self( ID )

        self.known_neighbors = False 
        
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
            Logger.Trace("Looking for {}, but only have {}".format( hex_id, self.ids))
            Logger.Fatal("id not in region", ValueError)
       

        
        # countable number of cases
        #    1. hex shares no border with either perimeter or any enclave: popped and made into enclave
        #    2. hex _only_ shares border with perimeter: glom perimeter to hex
        
        #    3. hex borders perimeter multiple times. Popping hex will create multiple regions. We forbid this possibility... 

        this_hex = self.parent.catalog[ hex_id ]
        hex_perim = this_hex.vertices[::-1]

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
            while (self.perimeter[start_index] in hex_perim):
                start_index += 1

            index = start_index

            while self.perimeter[index % len(self.perimeter)] not in hex_perim:
                new_perim.append( self.perimeter[ index % len( self.perimeter) ] )
                index += 1

            new_perim.append( self.perimeter[ index % len( self.perimeter) ] )

            hex_index = (hex_perim.index( self.perimeter[index %len(self.perimeter)] ) + 1 ) % len(hex_perim)

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
        self.known_neighbors = False 

def _glom( original, new, start_index):
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
        Logger.Fatal("Something terribly unexpected happened: {}, {}, {}".format(original, new, start_index))

    return( new_perimeter )


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

        self.width          = 1.0
        self.color          = (0.0, 0.0, 0.0)
        self._step_calc     = False
        self._step          = None 
        self.z_level       = 2

        self.name = ""

    def end(self, offset=0):
        """
        Returns the a copy of the endPoint of this Path. Note: the endpoint is the last point added

        @param offset   - a shift from that endpoint. Number of indices away from the endpoint. Positive values of offset step towards the beginning! 
        """
        if isinstance(offset, int):
            pass
        elif isinstance( offset, float):
            offset = int(offset)
            Logger.Warn("ATTN: received `offset` of type {}, rounding. This may be an issue!".format(float))
        else:
            raise TypeError("Received type {} for arg `offset`, expected {}".format( type(offset), int))

        if len(self._vertices)==0:
            return(None)
        else:
            which_vertex = -1-offset
            if abs(which_vertex)>len(self._vertices):
                raise ValueError("Invalid vertex requested")
            else:
                return( Point( self._vertices[which_vertex].x, self._vertices[which_vertex].y ) )

    def start(self, offset=0):
        """
        Returns a copy of start point of this Path. Note: start point is the first point added. 

        @param offset   - number of steps away from the start point. Positive offset steps towards the end
        """
        reversed_offset = -1 - offset  
        return( self.end( reversed_offset ) )
        

    @property
    def vertices(self):
        """
        The points defining this path. Returns a copy! 
        """
        built = []
        for vert in self._vertices:
            built.append( Point( vert.x, vert.y ) )
        return( built)
    
    def trim_at( self, where, keep_upper=False):
        """
        Trims the path just before the 'where' entry.

        If "keep_upper" is False we keep the "start--> /" half
        If "keep_upper" is true we keep the  "which-->end" half

        @param where        - type Int or Point. If Int, trims the path at the vertex indexed by `where', else trims the path at the vertex `where`
        @param keep_upper   - type Bool. start--->where if "keep_upper" is True 
        """

        p_type = False 
        if isinstance( where, int ):
            p_type = True
        elif not isinstance( where , Point ):
            raise TypeError("Arg 'where' must be type {} or {}, received {}".format( Point, int , type(where)))
        
        if not isinstance(keep_upper, bool):
            raise TypeError("Arg 'keep_upper' must be type {}, received {}.".format(bool, type(keep_upper)))

        if p_type:
            which_index = where
        else:
            try:
                which_index = self._vertices.index( where )
            except ValueError:
                raise ValueError("Point {} is not in list of vertices for obj {}".format(where, type(self)))

        # make sure it's not trying to trim at too long of a point
        if which_index>= len(self._vertices):
            raise ValueError("Index {} invalid, only {} Points on Path.".format(which_index, len(self._vertices)))

        
        # this leaves the self-intersect point there. Good!
        if keep_upper:
            self._vertices = self._vertices[:which_index]
        else:
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
                raise ValueError("Paths must have consistently spaced entries")

        self._vertices.append( end )

    def add_to_start( self, start):
        """
        Append Point to start of path
        
        @param start    - object of type Point 
        """
        if not isinstance( start, Point):
            raise TypeError("Expected type {} for arg 'end', got {}".format( Point, type(start )))

        if not self._step_calc:
            # get the magnitude between the last point and the one we're adding, that's the step size 
            self._step = ( start - self.start() ).magnitude 
            self._step_calc = True 
        else:
            # if the difference between this step and the precalculated step is big, raise an exception! 
            if (( start - self.start() ).magnitude - self._step)/self._step  > 0.01:
                raise ValueError("Paths must have consistently spaced entries")


        self._vertices = [ start ] + self._vertices

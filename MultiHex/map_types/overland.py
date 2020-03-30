from MultiHex.core import Hex, Point, Region, Path, Hexmap
from MultiHex.core import RegionMergeError, RegionPopError

from MultiHex.objects import Settlement, Government
from MultiHex.tools import hex_brush, entity_brush, path_brush, region_brush, basic_tool, clicker_control

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsPathItem

"""
Implements the overland map type, its brushes, and its hexes 

Entries:
    Town            - Settlement (Entity) implementation 
    River           - Path implementation. For rivers
    Road            - Path implementation. For roads...
    County          - Region implementation to create counties 
    Biome           - Region implementation for, well, biomes
    region_brush    - basic tool, makes regions
    hex_brush       - basic tool, makes hexes
    OHex            - Hex implementation for land hexes
"""

default_p = Point(0.0,0.0)

def point_on_river( point, river ):
    """
    returns whether or not the Point `point` is somewhere on the River object `river`

    @param point    - the Point...
    @param river    - the River... 
    """

    assert( isinstance( point, Point))
    assert( isinstance( river, River))

    if river.tributaries is not None:
        # see if the point is on the river body, or one of the tributaries. Call this function on each of the tributaries 
        return( (point in river.vertices) or (point_on_river( point, river.tributaries[0])) or (point_on_river( point, river.tributaries[1] )))
    else:

        return( point in river.vertices )

class ol_clicker_control( clicker_control ):
    """
    Implements the "clicker_control", which is itself a QtScene

    This is used so that when a QPainterRiver is registered, the returned 
    QtPathItem is of a special type that has a tribs object too
    """
    def __init__(self, parent=None, master = None):
        clicker_control.__init__(self, parent, master)

    def addPath(self, new_path, pen=QtGui.QPen(), brush=QtGui.QBrush() ):
        obj = clicker_control.addPath( self, new_path, pen, brush)

        if isinstance(new_path, QPainterRiver):
            setattr(obj, 'tribs', new_path.tribs)

        return(obj)


class QPainterRiver( QtGui.QPainterPath ):
    """
    Derived class of the QPainterPath which simply adds a "tribs" attribute
    """
    def __init__(self, tribs=None):
        QtGui.QPainterPath.__init__(self)

        if tribs is not None:
            if not isinstance(tribs, tuple):
                raise TypeError("Should be {}, not {}".format(tuple, type(tribs)))
            if len(tribs)!=2:
                raise ValueError("Should be len {}, not {}".format(2, len(tribs)))

        self.tribs = tribs


class Town( Settlement ):
    """
    Implements settlements for overland medieval towns! 
    """
    def __init__(self, name, location = None, is_ward = False):
        Settlement.__init__( self, name, location, is_ward )

        self.walled = False 
       
    def update_icon(self):
        temp = self.size.lower() 

        if temp!="ward":
            self.icon = temp

    @property
    def size( self ):
        total_pop = self.population
        
        if self._is_ward:
            return("Ward")
        
        if total_pop < 10:
            return("Village")
        elif total_pop < 150:
            return("Village") 
        elif total_pop < 1000:
            return("Town")
        elif total_pop < 7500:
            return("City")
        else:
            return("Metropolis")

class Road(Path):
    """
    Implements the path object for roads
    """
    def __init__(self, start):
        Path.__init__(self, start)

        self.color = ( 196, 196, 196 )
        self.width = 2

        self.quality = 1.50 

        self.z_value = 3

class River(Path):
    """
    Implements `Path`
    """
    def __init__(self, start):
        Path.__init__(self, start)
        self.color = (colors.ocean[0]*0.8, colors.ocean[1]*0.8, colors.ocean[2]*0.8)

        self.width = 1

        # by default, should have none
        self.tributaries = None
        self.tributary_objs = None

        self._max_len = 20
        
        self.z_value = 2

    def join_with( self, other ):
        """
        Joins with the other river! 

        Other river must connect to this one 
        """
        if not isinstance( other, River ):
            raise TypeError("Cannot join with object of type {}".format(type(other)))

        # make sure these rivers are join-able. One river needs to have its end point on the other! 
        if other.end() not in self._vertices:
            # try joining with its tributaries 
            if self.tributaries is not None:
                prior0 = self.tributaries[0].width
                prior1 = self.tributaries[1].width
                error_code = self.tributaries[0].join_with( other )
                if error_code == 0:
                    self.width += self.tributaries[0].width - prior0
                    return(0)
                error_code = self.tributaries[1].join_with( other )
                if error_code == 0:
                    self.width += self.tributaries[1].width - prior1
                    return(0) 
                
                # failed to join other river with itself or its tributaries 
                return( 1 )
            else:
                return( 1)

        # we know they meet somewhere
        # check if they are end-to-end
        if self.end()==other.start():
            self._vertices = self._vertices + other.vertices
            return(0)
        elif other.end()==self.start():
            self._vertices = other.vertices + self.vertices
            return(0)
        elif self.end()==other.end():
            # if they meet end-to-end (weird)... reverse the appened one
            self._vertices = self._vertices + other.vertices[::-1]
            return(0)
        elif self.start()==other.start():
            #take the other, reverse it, append to the start
            self._vertices = other.vertices[::-1] + self._vertices
            return(0)

        # other one ends in this one
        tributary_1 = other
        # going to define a tributary 
        tributary_2 = River( self.start() )

        # Merge part of the self into the new tributary 
        intersect = self.vertices.index( other.end() )
        
        tributary_2._vertices = self.vertices[: (intersect+1)]
        tributary_2.tributaries = self.tributaries 

        self.trim_at( intersect, keep_upper=False )
 
        # modify the self
        self.tributaries = [ tributary_1, tributary_2 ]
        self.tributaries[0].width = other.width
        self.tributaries[1].width = self.width

        self.width = other.width + self.width 

        # success code 
        return(0)


class County(Region, Government):
    """
    Implements the Region class for Counties. 
    """

    def __init__(self, hex_id, parent):
        Region.__init__(self, hex_id, parent)
        Government.__init__(self) 

        self.nation = None

    @property
    def tension(self):
        these_ids = len(self.eIDs)
        if these_ids==0:
            return(0)
        else:
            towns = list(filter( (lambda x:  isinstance(self.parent.main_map.eid_catalogue[x], Town)), these_ids))
            
            avg_ord = self.order/( 1+len(towns))
            avg_war = self.war/( 1+len(towns))
            avg_spi = self_spi/( 1+len(towns))
            
            for town in towns:
                avg_ord += (town.population/self.population)*ward.order/(1+len(towns))
                avg_war += (town.population/self.population)*ward.war/(1+len(towns))
                avg_spi += (town.population/self.population)*ward.spirit/(1+len(towns))

            wip = ( avg_ord - self.order)**2 + (avg_war - self.war)**2 + (avg_spi - self.spirit)**2
            for town in towns:
                (avg_ord - town.order)**2 + (avg_war - town.war)**2 + (avg_spi - town.spirit)**2

            wip = sqrt(wip)
            return(wip)


    @property
    def wealth( self ):
        this_wealth = 0
        for eID in self.eIDs:
            if isinstance( self.parent.eid_catalogue[eID], Settlement ):
                this_wealth += self.parent.eid_catalogue[eID].wealth

        # returns in gp per person 
        return(this_wealth)

    @property
    def eIDs( self ):
        """
        A list of entity IDs contained within this County's borders 
        """
        which = []
        for ID in self.ids:
            if ID in self.parent.eid_map:
                which += self.parent.eid_map[ID]
        return( which )

    @property
    def population( self ):
        pop = 0 
        for eID in self.eIDs:
            if isinstance( self.parent.eid_catalogue[ eID ], Settlement ):
                pop += self.parent.eid_catalogue[eID].population 
        return( pop )

class Nation( Government ):
    """
    A Collection of Counties. One County serves as the seat of the Nation, and that's this one. 
    """
    def __init__(self, parent, rID):
        """
        Must be constructed with a parent Hexmap and the rID of the first constituent County 
        """
        assert( isinstance( rID, int))
        assert( isinstance( parent, Hexmap))
        Government.__init__(self)
        
        self._county_key = 'county'

        if not rID in parent.rid_catalogue[self._county_key]:
            raise ValueError("County must be a registered in Hexmap.")

        self.parent = parent
        self.counties = [rID]
        self.color = self.parent.rid_catalogue[self._county_key][rID].color
        self.parent.rid_catalogue[self._county_key][rID].nation = self
        self.name = "Kingdom of " + self.parent.rid_catalogue[self._county_key][rID].name

    @property
    def tension(self):

        if len(self.counties)==0:
            return(0)
        else:
            # get averages! 
            avg_ord = self.order/(1+len(self.counties))
            avg_war = self.war/(1+len(self.counties))
            avg_spi = self.spirit/(1+len(self.counties))

            for count in self.counties:
                avg_ord += self.parent.rid_catalogue[self._county_key][count].order/(1+len(self.counties))
                avg_war += self.parent.rid_catalogue[self._county_key][count].war/(1+len(self.counties))
                avg_spi += self.parent.rid_catalogue[self._county_key][count].spirit/(1+len(self.counties))

            wip = 0
            for count in self.counties:
                wip += (self.parent.rid_catalogue[self._county_key][count].population/self.subjects)*((avg_ord - self.parent.rid_catalogue[self._county_key][count].order)**2 + (avg_war - self.parent.rid_catalogue[self._county_key][count].war)**2 + (avg_spi - self.parent.rid_catalogue[self._county_key][count].spirit)**2)

            wip = sqrt(wip)
            return( wip )

    @property
    def subjects( self ):
        pop = 0
        for county in self.counties:
            pop += self.parent.rid_catalogue[self._county_key][county].population
        return( pop )
    
    @property
    def total_wealth( self ):
        wea = 0
        for county in self.counties:
            wea += self.parent.rid_catalogue[self._county_key][county].wealth
        return(wea)

    
    def add_county( self, rID ):
        if not isinstance( rID, int):
            raise TypeError("Expected arg of type {}, received {}".format(int, type(rID)))
        if not rID in self.parent.rid_catalogue[self._county_key]:
            raise ValueError("No registered county of rID {}".format(rID))
        
        if rID in self.counties:
            return

        # if it's already part of another Nation, remove it from that nation
        if self.parent.rid_catalogue[self._county_key][rID].nation is not None:
            self.remove_county( rID )

        allowed = False
        for county in self.counties:
            allowed = ( rID in self.parent.get_region_neighbors( county, self._county_key) )
            if allowed:
                break
        if not allowed:
            raise ValueError("Unable to add County {} to Nation. They share no border".format(rID))
        
        self.parent.rid_catalogue[self._county_key][rID].color = self.color 
        self.parent.rid_catalogue[self._county_key][rID].nation = self
        self.counties.append( rID )

    def remove_county( self, rID ):
        if not isinstance( rID , int):
            raise TypeError("Expected arg of type {}, received {}".format(int, type(rID)))
        if rID not in self.counties:
            raise ValueError("County {} not in this Nation".format(rID))

        if rID not in self.counties:
            return

        self.parent.rid_catalogue[self._county_key][rID].set_color( rID )
        self.parent.rid_catalogue[self._county_key][rID].nation = None
        self.counties.pop( self.counties.index(rID) )

class Biome(Region):
    """
    Implementation of the region class for regions of similar geography. 

    Biomes! Like forests, deserts, etc...  
    """
    def __init__(self, hex_id, parent):
        Region.__init__(self, hex_id, parent)




class River_Brush( path_brush ):
    def __init__(self, parent):
        path_brush.__init__(self,parent, True)
        self._creating = River

        self._path_key = "rivers"

        self._qtpath_type = QPainterRiver

    def primary_mouse_released(self, event):
        """
        As usual, call the normal mouse-click function
        But then check for intersections with a new river, and if one is found merge! 
        """
        path_brush.primary_mouse_released( self, event)

        if self._state in [2,3]:
            for pid in self.parent.main_map.path_catalog[self._path_key]:
                result = self.parent.main_map.path_catalog[self._path_key][pid].join_with( self._wip_path )
                if result == 0:
                    self._wip_path = None 
                    if self._wip_path_object is not None:
                        self.parent.scene.removeItem( self._wip_path_object)
                        self._wip_path_object = None 

                    self.prepare(0)
                    self.draw_path( pid )
                    break

    def secondary_mouse_released(self, event):
        path_brush.secondary_mouse_released(self, event)
        self.parent.river_update_list()
        

    def draw_path( self, pID):
        """
        Draw the path using the original implementaitno, then draw the tributaries 
        """
        # before calling the original implementation, we remove the drawn river recursively!
        assert(isinstance( pID, int) or (pID is None))

        if pID in self._drawn_paths:
            self.river_remove_item( self._drawn_paths[pID] )
            del self._drawn_paths[pID]

        path_brush.draw_path(self, pID)

        try:
            this_path = self.parent.main_map.path_catalog[self._path_key][pID]
        except KeyError:
            return

        if this_path.tributaries is not None:
            self._drawn_paths[pID].tribs = self.draw_tribs( this_path )

    def river_remove_item( self, which ):
        """
        Recursively removes a QPainterRiver and its child tributatry items 
        """
        assert( isinstance(which, QGraphicsPathItem))
        self.parent.scene.removeItem( which )

        if which.tribs is not None:
            self.river_remove_item( which.tribs[0] )
            self.river_remove_item( which.tribs[1] )
            

    def draw_tribs(self, river):
        assert( isinstance( river, River))
        
        #if not hasattr(river, "tributary_objs"):
        #    setattr(river, "tributary_objs", None)


        # color, style, already set by original call to the draw function! 

        trib1 = self._qtpath_type()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( river.tributaries[0].vertices  ) )
        trib1.addPolygon(outline)

        trib2 = self._qtpath_type()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( river.tributaries[1].vertices  ) )
        trib2.addPolygon(outline)

        # draw both of the tributaries using the appropriate width, saving the QRiverItem
        self.QPen.setWidth(3 + river.tributaries[0].width)
        first =self.parent.scene.addPath( trib1, pen=self.QPen, brush=self.QBrush)
        self.QPen.setWidth(3 + river.tributaries[1].width)
        second = self.parent.scene.addPath( trib2, pen=self.QPen, brush=self.QBrush)


        tributary_objs = ( first , second )

        # draw tributaties of the tributaries (recursively), assign the newely formed tuples to the QRiverItem
        if river.tributaries[0].tributaries is not None:
            tributary_objs[0].tribs = self.draw_tribs( river.tributaries[0])
        if river.tributaries[1].tributaries is not None:
            tributary_objs[1].tribs = self.draw_tribs( river.tributaries[1])

        # set the z-value of the rivers
        tributary_objs[0].setZValue(river.z_level)
        tributary_objs[1].setZValue(river.z_level)

        # return a tuple of the objects 
        return tributary_objs

    def redraw_rivers( self ):
        """
        all the rivers
        """
        # self._river_drawn


        if 'rivers' in self.parent.main_map.path_catalog:
            for pID in self.parent.main_map.path_catalog['rivers'].keys():
                assert( isinstance( self.parent.main_map.path_catalog['rivers'][pID], River) )
                self.draw_path( pID )
                    

class Biome_Brush( region_brush):
    def __init__(self, parent, civmode = False):
        region_brush.__init__(self, parent, 'biome')


        self.draw_borders = not civmode
        self.small_font = civmode
        self._type = Biome

    def primary_mouse_released(self, event):
        region_brush.primary_mouse_released(self, event)
        self.parent.biome_update_gui()
     


class County_Brush( region_brush ):
    def __init__(self, parent):
        region_brush.__init__(self, parent, 'county')

        self.draw_borders = True
        self.selector_mode = True
        self._type = County

        self.default_name = "County"

        self.in_nation = None

    def secondary_mouse_released(self, event):
        region_brush.secondary_mouse_released( self, event )

        self.parent.county_update_with_selected()

    def primary_mouse_released(self, event):
        if self.selected_rid is not None:
            if self.selector_mode:
                self.selector_mode = False
            else:
                self.selector_mode = True
        else:
            self.selected_rid = None
            self.selector_mode = True

class Nation_Brush( basic_tool ):
    def __init__(self, parent):
        self.parent = parent

        self._county_key = 'county'

        self._state = 0
        self._selected = None
        # 0 - neutral
        # 1 - creating a new nation 
        # 2 - adding to an existing nation
        # 3 - removing some county from its nation 

    @property 
    def selected(self):
        return( self._selected )

    def select(self, nation):
        if nation is not None:
            assert(isinstance( nation, Nation))

        self._selected = nation

    def set_state(self, state):
        assert( isinstance(state, int))
        if state in [0,1,2,3]:
            self._state = state
        else:
            raise NotImplementedError("Unrecognized state {}".format(state))

        self.parent.update_state()

    def primary_mouse_released( self, event ):
        where = Point( event.scenePos().x(), event.scenePos().y() )
        loc_id = self.parent.main_map.get_id_from_point( where )
        try:        
            this_county_rid = self.parent.main_map.id_map[self._county_key][loc_id]
        except KeyError:
            return
            
        if self._county_key not in self.parent.main_map.id_map:
            return

        if self._state == 0:
            # In a waiting state. If we're in state 0, select the nation under the cursor 
            where = Point( event.scenePos().x(), event.scenePos().y() )
            loc_id = self.parent.main_map.get_id_from_point( where )
            try:        
                this_county_rid = self.parent.main_map.id_map[self._county_key][loc_id]
            except KeyError:
                return

            if self.parent.main_map.rid_catalogue[self._county_key][this_county_rid].nation is not None:
                self.select(self.parent.main_map.rid_catalogue[self._county_key][this_county_rid].nation)
                self.parent.nation_update_gui()

        elif self._state == 1:
            # create the new nation with this county as a base

            # no registering needed. A nation exists as a nebulous connection between its counties. Once the last such connection is severed, the nation disappears 
            #   .... and is collected by the Python garbage collector 
            new_nation = Nation(self.parent.main_map, this_county_rid)
            self._state = 0
        elif self._state == 2:
            # adding to selected nation
            if self._selected is None:
                self.set_state( 0 )
                print("nothing was selected")
                return
            else:
                self._selected.add_county( this_county_rid )
                self.parent.nation_update_gui()
                
        elif self._state == 3:
            if self._selected is None:
                self.set_state( 0 )
                print("nothing was selected")
                return
            else:
                self._selected.remove_county( this_county_rid )
                self.parent.nation_update_gui()

        self.parent.county_control.redraw_region(this_county_rid)

    def secondary_mouse_released(self, event):
        if self._state == 0:
            # select the kingdom at the mouse ! 
            pass

        elif self._state==1:
            # cancel 
            self.set_state( 0 )
        elif self._state==2:
            self.set_state( 0 )
        elif self._state ==3:
            self.set_state( 0 )


    def mouse_moved( self, event ):
        pass

    def drop( self ):
        self._state = 0
    def clear(self):
        self._state = 0
        
class Road_Brush( path_brush ):
    def __init__(self, parent):
        path_brush.__init__(self,parent, False)
        self._creating = Road

        self._path_key = "roads"

    def secondary_mouse_released(self, event):
        path_brush.secondary_mouse_released(self, event)
        self.parent.road_update_list()


class OEntity_Brush( entity_brush ):
    def __init__(self, parent):
        entity_brush.__init__(self, parent)
        self._settlement = Town

class OHex_Brush( hex_brush ):
    def __init__(self, parent):
        hex_brush.__init__(self, parent)
        self._brush_type = OHex

        self._skip_params = ["_altitude_base"]

        self._river_drawn = []

    def adjust_hex(self, which):
        """
        OHex brush specific. Land shouldn't be made beneath sea level and ocean shouldn't be above it! 
        """
        hex_brush.adjust_hex(self, which)

        which._is_land = bool(which._is_land)
        if which._is_land:
            if which._altitude_base < 0:
                which._altitude_base = 0.
        else:
            if which._altitude_base > 0:
                which._altitude_base = 0

    # DIE
    def drop(self):
        if self.parent.main_map._outline is not None:
            self.parent.scene.removeItem( self._outline_obj )
            self._outline_obj = None
        self._selected_id = None

 


    
class OHex(Hex):
    """
    Overland Hex implementation

    Adds criteria to define how that hex is! 
    """
    def __init__(self, center=default_p, radius=1.0):
        Hex.__init__(self, center, radius)
        
        self._biodiversity     = 1.0
        self._rainfall_base    = 0.0
        self._altitude_base    = 1.0
        self._temperature_base = 1.0
        self._is_land          = True
        self.biome             = ""
        self.on_road           = None

        # CW downstream , CCW downstream, runs through
        self.river_border = [ False ,False , False]
        
    def rescale_color(self):
        self.fill  = (min( 255, max( 0, self.fill[0]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[1]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[2]*( 1.0 + 0.4*(self._altitude_base) -0.2))))


class hcolor:
    """
    Just a utility used to hold a bunch of colors 
    """
    def __init__(self):
        self.ocean = (100,173,209)
        self.grassland = (149,207,68)
        self.forest = (36, 94, 25)
        self.arctic = (171,224,224)
        self.tundra = (47,105,89)
        self.mountain = (158,140,96)
        self.ridge = (99,88,60)
        self.desert = (230,178,110)
        self.rainforest = (22,77,57)
        self.savanah = (170, 186, 87)
        self.wetlands = (30,110,84)
colors = hcolor()


# Tons of hex templates... 
def Ocean_Hex(center, radius):
    temp = OHex(center, radius)
    temp.fill = colors.ocean
    temp._temperature_base = 0.5
    temp._rainfall_base    = 1.0
    temp._biodiversity     = 1.0
    temp._altitude_base    = 0.0
    temp._is_land          = False
    return(temp) 

def Grassland_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.grassland
    temp._is_land = True
    return(temp)

def Forest_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.forest
    temp._is_land = True
    return(temp)

def Mountain_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.mountain
    temp.genkey = '01000000'
    temp._is_land = True
    return(temp)

def Arctic_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.arctic
    temp._temperature_base = 0.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Desert_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.desert
    temp._temperature_base = 1.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Ridge_Hex(center, radius):
    temp = OHex( center, radius )
    temp.fill = colors.ridge
    temp.genkey = '11000000'
    temp._is_land = True
    return(temp)



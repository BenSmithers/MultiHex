from MultiHex.core import Hex, Point, Region, Path, Hexmap
from MultiHex.core import RegionMergeError, RegionPopError

from MultiHex.objects import Settlement, Government
from MultiHex.tools import hex_brush, entity_brush, path_brush, region_brush, basic_tool, clicker_control

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsPathItem

try:
    from numpy import inf, exp,sqrt
except ImportError:
    from math import inf, exp,sqrt

"""
Implements the overland map type, its brushes, and its hexes.
These are all derived from the "core" and "tools classes 

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
rthree = sqrt(3)

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
    Implements `Path` for rivers, allowing rivers to be joined to make tributaries 
    """
    def __init__(self, start):
        Path.__init__(self, start)
        self.color = (134, 183, 207)

        self.width = 1

        # by default, should have none
        self.tributaries = None
        self.tributary_objs = None

        self._max_len = 20
        
        self.z_value = 2

    def join_with( self, other ):
        """
        Looks and tries to see if the river 'other' merges with the self or one the self's tributaries

        Returns an integer: 0 for successful merge, 1 for no merge 
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
            self.tributaries = other.tributaries
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
    Adds this "tension" property measuring discrepancies between a county's government and its constituent government 
    Also adds ways of accessing total wealth and population
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
    Similar to Counties, adds tension and total wealth+population
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


class Detail_Brush( basic_tool ):
    """
    This tool is used to modify aspects of the hexes in bulk. 
    """
    def __init__(self,parent):
        basic_tool.__init__(self, parent)

        self._hover_circle = None #qt object for seleciton
        self._location = None
        self._radius = 1

        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.brush.setStyle(1)

        self.pen.setColor(QtGui.QColor(183, 114, 194,150))
        self.brush.setColor(QtGui.QColor(183, 114, 194, 50))

        self._magnitude = 0.05

        self._configuring = ""

    @property
    def configuring(self):
        return(self._configuring )

    def set_configuring(self, conf):
        if not isinstance(conf, str):
            raise TypeError("Argument must be {}, got {}".format(str, type(conf)))

        self._configuring = conf
        print("now configuring {}".format(self._configuring))

    def set_magnitude(self, new):
        if not isinstance(new, float):
            raise TypeError("Expected {}, got {}".format(float, type(new)))
        self._magnitude = min(new, 1.0)

        if new>1.0:
            print("Warn! Received illegal magnitude {}, set to 1.0".format(new))
        
    @property
    def magnitude(self):
        return(self._magnitude)

    def set_radius(self, new_val):
        if not isinstance(new_val, int):
            raise TypeError("Expected {}, got {}".format(int, type(new_val)))
        self._radius = new_val

    @property 
    def radius(self):
        return(self._radius)

    def mouse_moved(self, event):
        """
        moved the selection circle to the mouse
        """
        place = Point( event.scenePos().x(), event.scenePos().y() )
        center_id = self.parent.main_map.get_id_from_point(place)
        real_place = self.parent.main_map.get_point_from_id(center_id)

        if center_id!=self._location:
            if self._hover_circle is not None:
                self.parent.scene.removeItem(self._hover_circle)

            eff_rad = self.parent.main_map.drawscale*(max(2*self._radius, 1))
            self._hover_circle = self.parent.scene.addEllipse(real_place.x-eff_rad , real_place.y-eff_rad, 2*eff_rad, 2*eff_rad , pen=self.pen, brush=self.brush)

    def primary_mouse_held(self, event):
        self.primary_mouse_released(event)

    def secondary_mouse_held(self, event):
        self.secondary_mouse_released(event)

    def primary_mouse_released(self, event):
        self.brushy_brushy(event, 1)

    def secondary_mouse_released(self, event):
        self.brushy_brushy(event, -1)

    def brushy_brushy( self, event, sign=1):
        """
        This is used to change temperature, rainfall, altitude, or whatever is underneath the brush
        """
        if self.configuring=="":
            return

        place = Point( event.scenePos().x(), event.scenePos().y() )
        center_id = self.parent.main_map.get_id_from_point(place)

        if center_id in self.parent.main_map.catalogue:
            setattr(self.parent.main_map.catalogue[center_id], self.configuring, getattr(self.parent.main_map.catalogue[center_id], self.configuring) + sign*self.magnitude)
            self.parent.climatizer.apply_climate_to_hex(self.parent.main_map.catalogue[center_id])
            self.parent.main_map.catalogue[center_id].rescale_color()
            self.parent.hex_control.redraw_hex(center_id)

        reduced = self.magnitude
        iter = 1
        while iter <= self.radius:
            reduced *= 2./3
            neighbors = self.parent.main_map.get_hex_neighbors(center_id, iter)
            for each in neighbors:
                if each in self.parent.main_map.catalogue:
                    new_value = max( -1.0, min(1.5, getattr(self.parent.main_map.catalogue[each], self.configuring) + sign*reduced))
                    setattr(self.parent.main_map.catalogue[each], self.configuring, new_value)
                    self.parent.climatizer.apply_climate_to_hex(self.parent.main_map.catalogue[each])
                    self.parent.main_map.catalogue[each].rescale_color()
                    self.parent.hex_control.redraw_hex(each)
            iter+=1

    def drop(self):
        if self._hover_circle is not None:
            self.parent.scene.removeItem(self._hover_circle)
            self._hover_circle = None

        self._location = None


class River_Brush( path_brush ):
    def __init__(self, parent):
        path_brush.__init__(self,parent, True)
        self._creating = River

        self._path_key = "rivers"

        # zeros and ones to select a tributary to a river
        self._sub_selection = ''

        self._qtpath_type = QPainterRiver

        self._extra_states = [5] # adding to a river's tributary's start 
    
    @property
    def sub_selection(self):
        return( self._sub_selection )

    def sub_select(self, sub):
        if not isinstance(sub, str):
            raise TypeError("Sub selection should be {}, not {}".format(str, type(sub)))

        for part in sub:
            if not (part=='0' or part=='1'):
                raise ValueError("Error in sub-selection. Encountered {}".format(part))

        self._sub_selection = sub
        self.draw_path( self.selected_pid )


    def _dive(self,river, key):
        """
        Recursively access the river object according to the selected tributary 
        """
        assert(isinstance(key, str))
        assert(isinstance(river, River))

        if len(key)==1:
            return( river.tributaries[ int(key[0]) ] )
        else:
            return( self._dive( river.tributaries[int(key[0])], key[1:] ))


    def get_sub_selection(self):
        """
        Returns the river object based on the sub-selection
        """
        if self.selected_pid is None:
            return(None)
        if self.sub_selection == '':
            return(self.parent.main_map.path_catalog[self._path_key][self.selected_pid])
        else:
            return( self._dive(self.parent.main_map.path_catalog[self._path_key][self.selected_pid], self.sub_selection) )

    def pop_selected_start(self):
        """
        Pops off the end of the selected tributary or registered river
        """
        if self.sub_selection=='':
            path_brush.pop_selected_start()
        else:
            # get the sub selection
            this_riv = self.get_sub_selection()
            if this_riv is not None:
                this_riv.trim_at(1, False )
                if len(this_riv.vertices)==1:
                    # this river now has no length
                    former = self.sub_selection

                    # get its parent
                    self.sub_select(former[:-1])
                    parent = self.get_sub_selection()

                    # the width will get changed a little bit
                    new_width = parent.width - this_riv.width

                    # get the other tributary 
                    if former[-1]==0:
                        what_to_add = parent.tributaries[1]
                    else:
                        what_to_add = parent.tributaries[0]

                    result = parent.join_with(what_to_add)
                    if result==1:
                        raise Exception("Failed to join rivers when it should've succeded!")
                    parent.width = new_width
                self.draw_path( self.selected_pid )


    def select_pid(self, pID=None):
        path_brush.select_pid( self, pID)
        self.sub_select('')

    def get_alt_from_point(self, event):
        return( self.get_sub_selection().start() )

    def primary_mouse_released(self, event):
        """
        As usual, call the normal mouse-click function
        But then check for intersections with a new river, and if one is found merge! 
        """
        path_brush.primary_mouse_released( self, event)
        if self._state==0 or self._state==1:
            return
        if self._state==2: # see if this WIP river will merge
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
        elif self._state==3: 
            #adding to start
            # try joining the active river with other ones 
            selected_river = self.get_sub_selection()

            
            for pid in self.parent.main_map.path_catalog[self._path_key]:
                if pid==self.selected_pid:
                    continue
                result = self.parent.main_map.path_catalog[self._path_key][pid].join_with( selected_river )
                if result == 0:

                    self.parent.main_map.unregister_path( self.selected_pid, 'rivers')
                    self.prepare(0)
                    self.draw_path(self.selected_pid)
                    self.draw_path(pid)
                    self.select_pid(None)
                    self.sub_select('')
                    self.parent.extra_ui.river_update_gui()
                    return

        elif self._state==4: # adding to end
            return
        elif self._state==5:
            where, from_point = self.where_to_from(event)

            which = self.get_sub_selection()
            which.add_to_start(where)
            self.draw_path(self.selected_pid)

        else:
            raise NotImplementedError("Unexpected state {} encountered".format(self._state))

    def mouse_moved(self, event):
        path_brush.mouse_moved(self, event)
        #print("mouse moved state {}".format(self._state))
        if self._state==5:
            if self._drawn_icon is None:
                self._drawn_icon = self.parent.scene.addPixmap( self._icon )
                self._drawn_icon.setZValue(20)

            self._drawn_icon.setX( event.scenePos().x() )
            self._drawn_icon.setY( event.scenePos().y() )

            where, from_point = self.where_to_from(event)

            if self._step_object is not None:
                self.parent.scene.removeItem( self._step_object )
            
            path = self._qtpath_type()
            path.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw([ from_point, where])) )
            self._step_object = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )

    def secondary_mouse_released(self, event):
        path_brush.secondary_mouse_released(self, event)
        
        if self._state==5:
            self.draw_path( self._selected_pid )
            self.select_pid(None )
            self._state = 0

        self.parent.extra_ui.river_update_list()
        

    def draw_path( self, pID):
        """
        Draw the path using the original implementaitno, then draw the tributaries 
        """
        # before calling the original implementation, we remove the drawn river recursively!
        assert(isinstance( pID, int) or (pID is None))

        # Clear everything out first. This starts from the outermost, works its way in to the delta
        if pID in self._drawn_paths:
            self.river_remove_item( self._drawn_paths[pID] )
            del self._drawn_paths[pID]

        path_brush.draw_path(self, pID, self.sub_selection!='')

        if pID in self.parent.main_map.path_catalog[self._path_key]:
            this_path = self.parent.main_map.path_catalog[self._path_key][pID]
        else:
            return

        if this_path.tributaries is not None:
            if pID in self._drawn_paths:
                self._drawn_paths[pID].tribs = self.draw_tribs( this_path, '', self.selected_pid==pID)



    def river_remove_item( self, which ):
        """
        Recursively removes a QPainterRiver and its child tributatry items 
        """
        assert( isinstance(which, QGraphicsPathItem))
        self.parent.scene.removeItem( which )

        if which.tribs is not None:
            self.river_remove_item( which.tribs[0] )
            self.river_remove_item( which.tribs[1] )
            

    def draw_tribs(self, river, depth, is_selected):
        assert( isinstance( river, River))

        if not self.drawing:
            return

        trib1 = self._qtpath_type()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( river.tributaries[0].vertices  ) )
        trib1.addPolygon(outline)

        
        trib2 = self._qtpath_type()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( river.tributaries[1].vertices  ) )
        trib2.addPolygon(outline)

        # draw both of the tributaries using the appropriate width, saving the QRiverItem
        if is_selected and self.sub_selection==depth+'0':
            self.QPen.setColor(self._selected_color)
        else:
            self.QPen.setColor(QtGui.QColor(river.tributaries[0].color[0],river.tributaries[0].color[1],river.tributaries[0].color[2]  ))
        self.QPen.setWidth(3 + river.tributaries[0].width)
        first =self.parent.scene.addPath( trib1, pen=self.QPen, brush=self.QBrush)

        if is_selected and self.sub_selection==depth+'1':
            self.QPen.setColor(self._selected_color)
        else:
            self.QPen.setColor(QtGui.QColor(river.tributaries[1].color[0],river.tributaries[1].color[1],river.tributaries[1].color[2]  ))

        self.QPen.setWidth(3 + river.tributaries[1].width)
        second = self.parent.scene.addPath( trib2, pen=self.QPen, brush=self.QBrush)


        tributary_objs = ( first , second )

        # set the z-value of the rivers
        tributary_objs[0].setZValue(river.z_level)
        tributary_objs[1].setZValue(river.z_level)

        # color, style, already set by original call to the draw function! 
        # draw tributaties of the tributaries (recursively), assign the newely formed tuples to the QRiverItem
        if river.tributaries[0].tributaries is not None:
            tributary_objs[0].tribs = self.draw_tribs( river.tributaries[0], depth+'0',is_selected)
        if river.tributaries[1].tributaries is not None:
            tributary_objs[1].tribs = self.draw_tribs( river.tributaries[1], depth+'1',is_selected)

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
    def drop(self):
        self.sub_select('')
        path_brush.drop(self)

    def clear(self):
        path_brush.clear(self)
        self.drop()

                    

class Biome_Brush( region_brush):
    def __init__(self, parent, civmode = False):
        region_brush.__init__(self, parent, 'biome')


        self.draw_borders = not civmode
        self.small_font = civmode
        self._type = Biome

    def primary_mouse_released(self, event):
        region_brush.primary_mouse_released(self, event)
        self.parent.extra_ui.biome_update_gui()
     
    def secondary_mouse_released(self, event):
        region_brush.secondary_mouse_released(self, event)
        self.parent.extra_ui.biome_update_gui()

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

    def primary_mouse_released(self, event):
        region_brush.primary_mouse_released(self, event)
        self.parent.extra_ui.county_update_with_selected()

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

        self.parent.extra_ui.update_state()

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
                self.parent.extra_ui.nation_update_gui()
                
        elif self._state == 3:
            if self._selected is None:
                self.set_state( 0 )
                print("nothing was selected")
                return
            else:
                self._selected.remove_county( this_county_rid )
                self.parent.extra_ui.nation_update_gui()

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
        self.parent.extra_ui.road_update_list()


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

    def adjust_hex(self, which, params=None):
        """
        Sets the specified Hex to the specified parameters
        """
        hex_brush.adjust_hex(self, which, params)

        which._is_land = bool(which._is_land)
        if which._is_land:
            if which._altitude_base < 0:
                which._altitude_base = 0.
        else:
            if which._altitude_base > 0:
                which._altitude_base = 0

    def get_color_for_param_overwrite(self,parameter_name, parameter_value):
        if parameter_name=="_altitude_base":
            return(QtGui.QColor( 50, max(0,min(230 - 100*parameter_value,255)), max(0,min(255,(130 + 100*parameter_value)))))
        elif parameter_name=="_rainfall_base":
            return(QtGui.QColor( max(0,min(255,230 - 100*parameter_value)), max(0,min(255,130 + 100*parameter_value)), 50))
        elif parameter_name=="_temperature_base":
            return(QtGui.QColor( max(0,min(255,255 - 155*parameter_value)), 200, max(0,min(255,155 + 100*parameter_value))))
        else:
            # default to red->green
            return(QtGui.QColor(max(0,min(255, 230 - 100*parameter_value)), max(0,min(255,130 + 100*parameter_value)), 50))


 


    
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
        self._temperature_base = 0.0
        self._is_land          = True
        self.biome             = ""
        self.on_road           = None

        # CW downstream , CCW downstream, runs through
        self.river_border = [ False ,False , False]

        self._scale_factor = self.radius*rthree

    def get_cost(self, other):
        """
        Gets the cost of movement between two hexes. Used for routing
        """
        if not isinstance(other, OHex):
            raise TypeError("Can only calculate cost with other {}, got {}".format(OHex, type(other)))

        # xor operator
        # both should be land OR both should be water
        if self._is_land ^ other._is_land:
            water_scale = 10.
        else:
            water_scale = 1.


        # prefer flat ground!
        lateral_dist = (self.center - other.center).magnitude

        alt_dif = exp(2*(other.altitude - self.altitude)) if self._is_land else 0.

        return(water_scale*(lateral_dist + self.radius*rthree*alt_dif))

    def get_heuristic(self, other):
        """
        Estimates the total cost of going from this hex to the other one
        """
        if not isinstance(other, OHex):
            raise TypeError("Can only calculate cost with other {}, got {}".format(OHex, type(other)))

        lateral_dist = (self.center - other.center).magnitude
        alt_dif = exp(2*(other.altitude - self.altitude))
        return(lateral_dist + self.radius*rthree*alt_dif)

    @property
    def biodiversity(self):
        return(self._biodiversity)

    @property
    def rainfall(self):
        return(self._rainfall_base)

    @property
    def altitude(self):
        return(self._altitude_base)

    @property
    def temperature(self):
        return(self._temperature_base)

    def set_biodiversity(self, what):
        if not (isinstance(what,float) or isinstance(what, int)):
            raise TypeError("Expected type {}, got {}".format(float, type(what)))
        self._biodiversity = what

    def set_rainfall_base(self, what):
        if not (isinstance(what,float) or isinstance(what, int)):
            raise TypeError("Expected type {}, got {}".format(float, type(what)))
        self._rainfall_base = what

    def set_altitude(self, what):
        if not (isinstance(what,float) or isinstance(what, int)):
            raise TypeError("Expected type {}, got {}".format(float, type(what)))
        self._altitude_base = what

    def set_temperature(self, what):
        if not (isinstance(what,float) or isinstance(what, int)):
            raise TypeError("Expected type {}, got {}".format(float, type(what)))
        self._temperature_base = what
        
    def rescale_color(self):
        self.fill  = (min( 255, max( 0, self.fill[0]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[1]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[2]*( 1.0 + 0.4*(self._altitude_base) -0.2))))



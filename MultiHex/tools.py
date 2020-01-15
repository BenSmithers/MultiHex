from PyQt5.QtWidgets import QGraphicsScene, QGraphicsDropShadowEffect
from PyQt5 import QtGui, QtCore

from MultiHex.core import Point, Region, RegionMergeError, RegionPopError, Path
from MultiHex.objects import Icons, Entity, Mobile, Settlement
# from MultiHex.map_types.overland import Road, River


import os # used for some of the icons

from math import sqrt
rthree =  sqrt(3)

class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self, parent=None):
        pass
    def primary_mouse_depressed(self,event):
        """
        Called when the right mouse button is depressed 

        @param event 
        """
        pass
    def primary_mouse_released(self, event):
        """
        This is called when the right mouse button is released from a localized click. 

        @param event - location of release
        """
        pass
    def primary_mouse_held(self,event ):
        """
        Called continuously while the right mouse button is moved and depressed 

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def secondary_mouse_released(self, event ):
        """
        Left click released event, used to select something

        @param event - Qt event object. has where the mouse is
        """
        pass
    def mouse_moved(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass
    def drop(self):
        """
        Called when this tool is being replaced. Cleans up anything it has drawn and should get rid of (like, selection circles). This is needed when closing one of the guis 
        """
        pass
    def toggle_mode(self, force=None):
        """
        Toggles the 'mode' of the tool. Optionally passed a 'corce' argument 
        """
        pass

    def clear(self):
        """
        Called when parent window is closing. Clears list of drawn items 
        """
        pass 
    def __str__(self):
        return("BasicTool of type {}".format(type(self)))

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

        self._primary = QtCore.Qt.LeftButton
        self._secondary = QtCore.Qt.RightButton

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
        if event.button()==self._primary:
            event.accept() # accept the event
            self._held = True # say that the mouse is being held 
            self._active.primary_mouse_depressed( event )

    def mouseReleaseEvent( self, event):
        """
        Called when a mouse button is released 
        """
        if event.button()==self._primary:
            # usually a brush event 
            event.accept()
            self._held = False
            self._active.primary_mouse_released(event)

        elif event.button()==self._secondary:
            # usually a selection event
            event.accept()
            self._active.secondary_mouse_released( event )

   #mouseMoveEvent 
    def mouseMoveEvent(self,event):
        """
        called continuously as the mouse is moved within the graphics space. The "held" boolean is used to distinguish between regular moves and click-drags 
        """
        event.accept()
        if self._held:
            self._active.primary_mouse_held( event )
 
        self._active.mouse_moved( event )

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

class path_brush(basic_tool):
    """
    Basic tool implementation for drawing Path objects like rivers and roads
    """
    def __init__(self, parent, river_mode=False):

        self._drawn_rivers = []

        self.parent = parent

        # state variable! 
        # state 0 - not doing anything
        #       1 - preparing to draw a road or river. Showing the river/road icon
        #       2 - currently adding to a road or river. 
        self._state = 0

        self._drawn_icon = None
        self._river_mode = river_mode
        self._creating = Path

        # load in the appropriate icon! 
        self._icon_size = 24
        if self._river_mode:
            self._icon = QtGui.QPixmap( os.path.join(os.path.dirname(__file__), '..', 'Artwork', 'river_icon.svg' )).scaledToWidth( self._icon_size )
        else: # road mode
            self._icon = QtGui.QPixmap( os.path.join(os.path.dirname(__file__), '..', 'Artwork', 'road_cursor.svg' )).scaledToWidth( self._icon_size )

        self._wip_path = None
        self._wip_path_object = None

        self._step_object = None

        # for drawing
        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
        self.QBrush.setStyle(0)
        self.QPen.setStyle(1)

    def prepare(self, setting):
        assert( isinstance(setting, int))

        self._state = setting

    def redraw_rivers(self):
        pass

    def mouse_moved( self, event ):
        if self._state==0:
            # not doing anything. Make sure no icon is there
            if self._drawn_icon is not None:
                self.parent.scene.removeItem( self._drawn_icon )
                self._drawn_icon = None

            if self._step_object is not None:
                self.parent.scene.removeItem( self._step_object )
                self._step_object = None

        elif self._state==1:
            # we are placing a new river/road. If it hasn't been drawn, draw the hex
            if self._drawn_icon is None:
                self._drawn_icon = self.parent.scene.addPixmap( self._icon )
                self._drawn_icon.setZValue(20)

            if self._river_mode:
                where = self.parent.main_map.get_vert_from_point(Point(event.scenePos().x(),event.scenePos().y() ))
                
            else:
                where = self.parent.main_map.get_point_from_id(self.parent.main_map.get_id_from_point( Point(event.scenePos().x(),event.scenePos().y() )))
                

            self._drawn_icon.setX( where.x ) #-(self._icon_size)/2 )
            self._drawn_icon.setY( where.y ) #-(self._icon_size)/2 )
        elif self._state==2:
            if self._drawn_icon is not None:
                self.parent.scene.removeItem( self._drawn_icon )
                self._drawn_icon = None

            if self._river_mode:
                step_size = self.parent.main_map.drawscale
            else:
                step_size = rthree*self.parent.main_map.drawscale

            small_step = Point( event.scenePos().x(), event.scenePos().y()) - self._wip_path.end()
            small_step.normalize()
            small_step = small_step * step_size

            if self._step_object is not None:
                self.parent.scene.removeItem( self._step_object )
            
            self._step_object = None

        else:
            raise NotImplementedError("{} Reached unexpected state {}".format(self, self._state))
    # update the position of the river icon

    def primary_mouse_released(self, event):
        if self._state==0:
            pass
        elif self._state==1:
            # get the location and make a new path


            if self._river_mode:
                where = self.parent.main_map.get_vert_from_point(Point(event.scenePos().x(),event.scenePos().y() ))

            else:
                where = self.parent.main_map.get_point_from_id(self.parent.main_map.get_id_from_point( Point(event.scenePos().x(),event.scenePos().y() )))
            
            self._wip_path = self._creating(where)
            self._state = 2

            self.QPen.setWidth( 2 +  self._wip_path.width)
            self.QPen.setColor( QtGui.QColor( self._wip_path.color[0],self._wip_path.color[1], self._wip_path.color[2]))

        elif self._state==2:
            pass
        else:
            raise NotImplementedError("Reached unexpected state {}".format(self._state))

    def secondary_mouse_released(self, event):
        if self._state==0:
            pass
        elif self._state==1:
            self._state = 0
        elif self._state==2:
            # finish up I guess
            pass
        else:
            raise NotImplementedError("Reached unexpected state {}".format(self._state))

    def draw_path(self):
        pass
        
class QEntityItem(QtGui.QStandardItem):
    """
    Item object to be used with the entity lists in the GUI. These things are the same, but also carry around an eID attribute.
    """
    def __init__(self, value, eID):
        super(QEntityItem, self).__init__( value)
        assert( isinstance(eID, int))
        assert( eID >= 0)
        self._eID = eID

    @property
    def eID(self):
        copy = self._eID
        return(copy)

class entity_brush(basic_tool):
    """
    Basic tool implementaion for adding and editing entities on the map! 
    """
    def __init__(self, parent):
        self.parent = parent

        # list of drawn Qt Items. objects indexed with relevant eID
        self._drawn_entities = {}

        # are we in the process of placing a thingy
        # -1 no
        #  0 yes, entity
        #  1 yes, Town
        self._placing = -1 
        
        # which menu is open
        self._menu = 0
        # 0 - locations
        # 1 - settlements 

        # eID of the selected entity 
        self._selected_eid = None
        
        # HexID of the selected Hex, and its object 
        self._selected_hex = None
        self._selected_hex_outline = None

        # these are used for the ghosted prospective placement icon of a new entity
        self._ghosted_placement = None
        self._icon_size = 32 #int(self.parent.main_map._drawscale*2)

        # whether or not assets have been loaded
        self._loaded = False
        # where the assets are loaded
        self._all_icons = None
        # icon we are writing with
        self._icon = None 

        self._settlement = Settlement
    
    @property
    def selected_hex(self):
        copy = self._selected_hex
        return(copy)

    @property
    def selected(self):
        copy = self._selected_eid
        return(copy)
    def select_entity(self, eID):
        """
        Function exposing the selected eID. Allows it to be set by non-member functions
        """
        assert( isinstance( eID, int ))
        if not eID in self.parent.main_map.eid_catalogue:
            raise ValueError("eID {} not registered, but is being selected?".format(eID))
        self._selected_eid = eID

    def prep_new(self, ent_type = 0):
        """
        Prepares this object to place a new Entity. Optional argument to specify /which/ kind of entity to place. Creates a ghost outline to show where the new Entity will be 
        """
        assert( isinstance(ent_type, int))
        self._placing = ent_type 

        if self._ghosted_placement is not None:
            self.parent.scene.removeItem(self._ghosted_placement)
            self._ghosted_placement = None 

        if ent_type == 0 or ent_type == 1:
            if ent_type==0:
                self._icon = self._all_icons.location
            else:
                self._icon = self._all_icons.village 
            self._ghosted_placement = self.parent.scene.addPixmap( self._icon )
            self._ghosted_placement.setZValue(20)
            
        else:
            pass

    def unprepare_new(self):
        """
        Yeah cancel that
        """
        self._placing = -1
        if self._ghosted_placement is not None:
            self.parent.scene.removeItem(self._ghosted_placement)
            self._ghosted_placement = None 

    def mouse_moved(self, event):
        """
        All this really does is move the ghost around. If it turns out that we aren't placing things then get rid of the ghosts 
        """
        if not self._loaded:
            self.load_assets()

        # this is the case when the user is placing a Location  ( 0 )
        if self._placing in [0, 1]:
            if self._ghosted_placement is None:
                raise Exception("This shouldn't happen")
            else:
                self._ghosted_placement.setX( event.scenePos().x() -(self._icon_size)/2 )
                self._ghosted_placement.setY( event.scenePos().y() -(self._icon_size)/2 )
        else:
            if self._ghosted_placement is not None:
                self.parent.scene.removeItem( self._ghosted_placement )
                self._ghosted_placement = None 

    def deselect_hex(self):
        """
        Called when this is no longer looking at any Hex
        """
        self._selected_hex = None
        self.update_wrt_new_hex()

    def update_wrt_new_hex(self):
        """
        Called when a new hex is selected, OR this hex has changed (like new entities). Updates the GUI based on the hex selected: draws an outline around the selected Hex and updates the list of entities 
        """
        
        self._menu = self.parent.ui.toolBox.currentIndex()

        if self._selected_hex_outline is not None:
            self.parent.scene.removeItem( self._selected_hex_outline )
            self._selected_hex_outline = None

        self._selected_eid = None

        if self._menu == 0:
            # tell the gui to update the proper menu
            self.parent.loc_update_selection( self._selected_hex )
        elif self._menu==1:
            # get eIDs at this hex
            settlement_eid = None

            if self._selected_hex in self.parent.main_map.eid_map:
                eIDs_here = self.parent.main_map.eid_map[ self._selected_hex ]
                for eID in eIDs_here:
                    if isinstance( self.parent.main_map.eid_catalogue[eID] , self._settlement ):
                        settlement_eid = eID
            self._selected_eid = settlement_eid
            self.parent.set_update_selection( settlement_eid )
        else:
            pass


    def update_wrt_new_eid(self):
        """
        Called when a new /entity/ is selected. Chooses and updates the proper menu
        """
        self._menu = self.parent.ui.toolBox.currentIndex()

        if self._menu == 0:
            self.parent.loc_update_name_text( self._selected_eid )
        elif self._menu==1:
            self.parent.set_update_selection( self._selected_eid )

    def primary_mouse_released( self, event ):
        """
        Select the hex that was clicked on. If we're placing, create the Entity and place it. Then update the menus
        """
        place = Point( event.scenePos().x(), event.scenePos().y() ) 
        loc_id = self.parent.main_map.get_id_from_point( place )
        
        if loc_id!=self._selected_hex:
            self._selected_hex = loc_id 
            self.update_wrt_new_hex()



        if self._placing in [ 0, 1 ]:
            # we are going to create 
            if self._ghosted_placement is not None:
                self.parent.scene.removeItem( self._ghosted_placement )
                self._ghosted_placement = None   
            
            if self._placing == 0:
                new_ent = Entity( "temp" , loc_id )
                new_ent.icon = "location"
                self._selected_eid = self.parent.main_map.register_new_entity( new_ent )
                self.parent.main_map.eid_catalogue[self._selected_eid].name = "Entity {}".format(self._selected_eid)
            else: #placing is 1
                new_ent = self._settlement("temp", loc_id )
                new_ent.icon = "village"
                self._selected_eid = self.parent.main_map.register_new_entity( new_ent )
                self.parent.main_map.eid_catalogue[self._selected_eid].name = "Town {}".format(self._selected_eid)
            
            self.update_wrt_new_eid()
            self.redraw_entities_at_hex( loc_id )

            if self._placing == 0:
                self.update_wrt_new_hex()

            self._placing = -1 

        else:
            pass



    def load_assets(self):
        """
        Loads all the artwork into an Icon object held 
        """
        self._all_icons = Icons()
        self._icon = self._all_icons.location
        self._loaded = True
    
    def redraw_entities_at_hex(self, hID):
        """
        Redraws the entities at the hexID provided. This function decides which entity to draw. 
        """

        if hID == -1:
            return
        if hID not in self.parent.main_map.eid_map:
            raise ValueError("HexID {} has no entry in {}".format(hID))

        eIDs = self.parent.main_map.eid_map[hID]
        
        # make sure none of these have been drawn
        for eID in eIDs:
            if eID in self._drawn_entities:
                self.parent.scene.removeItem( self._drawn_entities[eID])
                del self._drawn_entities[eID]
        
        which_eID = None
        for eID in eIDs:
            if which_eID is None:
                which_eID = eID 
                continue
            
            is_mob = isinstance( self.parent.main_map.eid_catalogue[eID], Mobile )
            if is_mob:
                print("Don't know how to draw a mob")
                continue

            is_set = isinstance( self.parent.main_map.eid_catalogue[eID], self._settlement)
            other_is_set = isinstance( self.parent.main_map.eid_catalogue[which_eID], self._settlement )
            
            # if the chosen one is a settlement and this one isn't, skip
            if other_is_set and (not is_set):
                continue
            # otherwise, if this one is a settlement and the other isn't, swap to this one. 
            elif is_set and ( not other_is_set ):
                which_eID = eID
            # if they /both/ are settlements
            elif other_is_set and is_set:
                # choose the one with the higher population
                if self.main_map.eid_catalogue[eID].population > self.main_map.eid_catalogue[which_eID].population:
                    which_eID = eID

        self.draw_entity( which_eID )    

    def draw_entity(self, eID):
        """
        Draws the entity with eID provided. 
        """

        if not self._loaded:
            self.load_assets()

        if (eID not in self.parent.main_map.eid_catalogue) and (eID not in self._drawn_entities):
            raise ValueError("eID {} not registered in catalogue".format(eID))

        # delete old drawing if it exists
        if eID in self._drawn_entities:
            self.parent.scene.removeItem( self._drawn_entities[ eID ] )
            del self._drawn_entities[ eID ]

        if eID in self.parent.main_map.eid_catalogue:
            self._drawn_entities[eID] = self.parent.scene.addPixmap( getattr( self._all_icons, self.parent.main_map.eid_catalogue[ eID ].icon ))
            self._drawn_entities[eID].setZValue(5)
            location = self.parent.main_map.get_point_from_id( self.parent.main_map.eid_catalogue[eID].location)
            self._drawn_entities[eID].setX( location.x - self._all_icons.shift)
            self._drawn_entities[eID].setY( location.y - self._all_icons.shift)


    def drop(self):
        self.deselect_hex()
       
        if self._selected_hex_outline is not None:
            self.parent.scene.removeItem( self._selected_hex_outline )

        if self._ghosted_placement is not None:
            self.parent.scene.removeItem( self._ghosted_placement )

    def clear(self):
        self.drop() 
        self._drawn_entities = {}

class hex_brush(basic_tool):
    """
    Another tool with clicker-control interfacing used to paint hexes on a hexmap. 

    Keeps track of all the canvas objects that it has drawn. Theres are **not** actual Hex's (TM), but just boring ass hexagons. 
    """
    def __init__(self, parent):
        self.writing = True
        self._brush_type = None
        self._brush_size = 1

        self.pen_style = 0
        self.pen_size = 2

        self.parent = parent

        self.drawn_hexes = {}
        self._outline_obj = None

        self._selected_id = None
        self._selected_out = None 

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()

    def primary_mouse_released(self, event):
        if self.writing:
            self.write(event)
        else:
            self.erase(event)
    def primary_mouse_held(self, event):
        self.primary_mouse_released(event)
    
    def mouse_moved(self, event):
        """
        While moving it continuously removes and redraws the outline
        """
        # get center, 
        place = Point( event.scenePos().x(), event.scenePos().y())
        center_id = self.parent.main_map.get_id_from_point( place )
        self.QPen.setWidth(5)
        self.QPen.setStyle(1)

        if self.parent.main_map._outline == center_id:
            # the mouse hasn't moved, skip this
            pass
        else:
            # new center! 
            self.parent.main_map._outline = center_id

            # get the outline
            outline = self.parent.main_map.get_neighbor_outline( center_id , self._brush_size)

            # if we're writing draw green, if erasing draw red 
            if self.writing:
                t_color = self._brush_type(Point(0,0), 1.0).fill
                self.QPen.setColor(QtGui.QColor(t_color[0], t_color[1], t_color[2]))
                self.QBrush.setStyle(1)
                self.QBrush.setColor(QtGui.QColor(t_color[0], t_color[1], t_color[2], 160))
            else:
                self.QBrush.setStyle(0)
                self.QPen.setColor(QtGui.QColor(255,15,15))

            # remove previous outline object
            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
            # redraw the selection outline


            self._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )
            self._outline_obj.setZValue(10)
    
    def erase(self, event):
        """
        First, it tries removing the picture on the canvas, and then unregistering that point's ID from the hex catalog
                obviously there may not be a hex at that ID. So just ignore when that happens 
        
        Then if relevant it does that again to all the neighboring points 
        """
        place = Point(event.scenePos().x(),event.scenePos().y() )
        loc_id = self.parent.main_map.get_id_from_point( place )
        try:
            self.parent.scene.removeItem( self.drawn_hexes[ loc_id ] ) 
            del self.drawn_hexes[loc_id]
            self.parent.main_map.remove_hex(loc_id)
        except KeyError:
            pass 

        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors(loc_id)
            for neighbor in neighbors:
                try:
                    self.parent.scene.removeItem( self.drawn_hexes[neighbor])
                    del self.drawn_hexes[neighbor]
                    self.parent.main_map.remove_hex( neighbor )
                except KeyError:
                    pass

    def write(self, event):
        """
        Like the eraser, but for writing. Gets the ID for the point under the cursor, builds a hex there, and tries registering it. If successfull, it then draws the hex. 

        Same story for larger brush size. Try building and registering hexes for all the IDs neighboring the central ID 

        """
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )

        # calculate the center of a hex that would have that id
        new_hex_center = self.parent.main_map.get_point_from_id( loc_id )
        # create a hex at that point, with a radius given by the current drawscale 
        new_hex= self._brush_type( new_hex_center, self.parent.main_map._drawscale )
        
        
        # register that hex in the hexmap 
        try:
            self.parent.main_map.register_hex( new_hex, loc_id )
            self.redraw_hex( loc_id )
        except NameError: # error registering hex. Das ok 
            pass
        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = self.parent.main_map.get_point_from_id( neighbor )
                new_hex = self._brush_type( new_hex_center, self.parent.main_map._drawscale)
                try:
                    self.parent.main_map.register_hex( new_hex, neighbor )            
                    self.redraw_hex( neighbor )
                except NameError:
                    pass
    def redraw_hex(self, hex_id):
        try:
            # if this hex has been drawn, redraw it! 
            if hex_id in self.drawn_hexes:
                self.parent.scene.removeItem( self.drawn_hexes[hex_id] )

            # get the pen ready (does the outlines)
            # may raise key error 
            this_hex = self.parent.main_map.catalogue[ hex_id ]
            self.QPen.setColor(QtGui.QColor( this_hex.outline[0], this_hex.outline[1], this_hex.outline[2] ))
            self.QBrush.setStyle(1)
 
            self.QPen.setWidth(self.pen_size)
            self.QPen.setStyle(self.pen_style)

            self.QBrush.setColor( QtGui.QColor( this_hex.fill[0], this_hex.fill[1], this_hex.fill[2] ))
            self.drawn_hexes[hex_id] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( this_hex._vertices )), pen=self.QPen, brush=self.QBrush) 
            self.drawn_hexes[hex_id].setZValue(-1)

        except KeyError: #happens if told to redraw a hex that isn't there 
            #print("key error")
            pass

               
            

    def secondary_mouse_released(self,event):
        self.QBrush.setStyle(0)
        self.QPen.setColor(QtGui.QColor(75,75,245))
        self.QPen.setWidth(4)

        here = Point( event.scenePos().x(), event.scenePos().y())
        this_id = self.parent.main_map.get_id_from_point( here )

        # only bother doing things if this is a new hex we're clicking on
        if self._selected_id != this_id:
            if self._selected_out is not None:
                # so, if there already is an outline (there should be), let's erase it. We're going to draw a new hex
                self.parent.scene.removeItem( self._selected_out )
            
            # okay, now verify that we're clicking on a registered hex 
            if this_id in self.parent.main_map.catalogue:
                # draw a new hex, and select its id 
                self._selected_out = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( self.parent.main_map.catalogue[this_id]._vertices)), pen = self.QPen, brush=self.QBrush )
                self._selected_out.setZValue(10)
                self._selected_id = this_id
                

                
            else:
                # the outline object needs to be purged, otherwise it will later try erasing it again
                # we also undo our selection 
                self._selected_out = None
                self._selected_id = None


    
    def toggle_brush_size(self):
        """
        Only here to support the outdated ridge gui 
        """
        if self._brush_size == 2:
            self._brush_size = 1
        else:
            self._brush_size = 2

    def set_brush_size(self, size):
        if type(size)!=int:
            raise TypeError("Invalid size type {}".format(size))

        if (size>0) and (size<3):
            self._brush_size = size
        else:
            raise ValueError("Cannot set brush size to {}".format(size))

    def toggle_mode(self, force= None):
        if (force is not None) and (type(force)==bool):
            self.writing = force
        else:
            if self.writing:
                self.writing = False # erasing 
            else:
                self.writing = True

    # DIE
    def drop(self):
        if self.parent.main_map._outline is not None:
            self.parent.scene.removeItem( self._outline_obj )
            self._outline_obj = None
        if self._selected_out is not None:
            self.parent.scene.removeItem( self._selected_out )
            self._selected_out = None
        self._selected_id = None
    
    def clear(self):
        self.drawn_hexes = {}
        self._outline_obj = {}
        


class region_brush(basic_tool):
    """
    basic_tool implementation used to draw and register regions on a canvas/hexmap 
    """

    def __init__(self, parent, layer):
        """
        @ param parent - the gui object that will hold this 
        """
        self.start = Point(0.0, 0.0)
        self.selected_rid = None

        # parent should be a pointer to the gui object that has this brush 
        self.parent = parent
        self._writing = True
        self._brush_size = 1

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
        self.QBrush.setStyle(6)
        self.QPen.setWidth(3)


        self.r_layer = layer

        self._outline_obj = None
        self._drawn_regions = {} # map from rid to drawn region
        self._drawn_names = {}

    def _set_color(self, color):
        """
        Sets the brush and pen to a specified color. The brush is only partially opaque 

        @param color    - the specified color. Needs to be an length-3 indexable with integer entries >0 and < 255
        """
        if len(color)<3:
            raise ValueError("")
        for entry in color:
            if type(entry)!=int:
                raise TypeError("For {} in {}, expected type {} but got {}".format(entry, color, int, type(entry)))

            if entry<0 or entry>255:
                raise ValueError("Entry {} in {} should be valued between 0 and 255".format(entry, color))

        self.QBrush.setColor(QtGui.QColor( color[0], color[1], color[2], 60))
        self.QPen.setColor( QtGui.QColor(color[0], color[1], color[2])) 
    def set_brush_size( self, size ):
        if not type(size)==int: 
            raise TypeError("Can't set brush size to type {}, expected {}".format(type(size), int))
        # not actually doing anything...
    
        if size==1:
            self._brush_size = 1
        elif size==2:
            self._brush_size= 2
        else:
            raise ValueError("Can't set brush size to {}".format(size))

    def secondary_mouse_released(self, event):
        """
        Selects the region under the cursor. If no region is there, deselect whatever region is active 
        """
        here = Point( event.scenePos().x(), event.scenePos().y())        
        this_id = self.parent.main_map.get_id_from_point( here )
        
        if this_id not in self.parent.main_map.id_map[self.r_layer]:
            self.selected_rid = None
            self.parent.ui.RegEdit.setText("")
        else:
            if self.parent.main_map.id_map[self.r_layer][this_id]!=self.selected_rid:

                self.selected_rid = self.parent.main_map.id_map[self.r_layer][this_id]
                self.parent.ui.RegEdit.setText(self.parent.main_map.rid_catalogue[self.r_layer][self.selected_rid].name)

    def primary_mouse_held(self, event):
        self.primary_mouse_released( event )

    def primary_mouse_released(self, event):
        """
        Right click 
        """
        if self._writing:
            self.reg_add(event)
        else:
            self.reg_remove(event)
    def toggle_mode(self, force=None):
        """
        Switches brush sizes, the region remover only works with brush size 1, so... force the brush size back to 1. 
        """
        if (force is not None) and (type(force)==bool):
            self._writing = force
            if force==False:
                self._brush_size = 1
        else:
            if self._writing:
                self._writing = False
                self._brush_size = 1
            else:
                self._writing = True
    def mouse_moved(self, event):
        """
        While moving it continuously removes and redraws the outline - reimplimentation of the 'move' function in the hex brush
        """
        # get center, 
        place = Point( event.scenePos().x(), event.scenePos().y())
        center_id = self.parent.main_map.get_id_from_point( place )
        
        self.QPen.setWidth(5)
        self.QPen.setStyle(1)

#        self._brush_size = 1

        if self.parent.main_map._outline == center_id:
            # the mouse hasn't moved, skip this
            pass
        else:
            # new center! 
            self.parent.main_map._outline = center_id

            # get the outline
            outline = self.parent.main_map.get_neighbor_outline( center_id , self._brush_size)

            # if we're writing draw green, if erasing draw red 
            if self._writing:
                self.QBrush.setStyle(6)
                if self.selected_rid is not None:
                    self._set_color( self.parent.main_map.rid_catalogue[self.r_layer][ self.selected_rid ].color)
                else:
                    self.QPen.setColor(QtGui.QColor(114,218,232))
            else:
                self.QPen.setColor(QtGui.QColor(220,20,20))
                self.QBrush.setColor(QtGui.QColor(220,20,20,170))
                self.QBrush.setStyle( 14 )


            # remove previous outline object
            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
            # redraw the selection outline

            self.QBrush.setStyle(0)
            self._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )
            self._outline_obj.setZValue( 10 )

    def reg_add(self, event):
        """
        Add to a region. If the brush size is 1, it just tries to add that hex to the active region. If there's no active region, it creates a region there. If the brush size is 2 it makes a temporary region around the cursor and merges the surrounding hexes with the temp region. Then it merges the temp region and active region together. 
        """
        # set up the pen and brush to draw a region
        
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )
        
        if loc_id not in self.parent.main_map.catalogue:
            return


        if self.selected_rid is None:
            # if the hex here is not mapped to a registered region, 
            if (loc_id not in self.parent.main_map.id_map[self.r_layer]):
                # make a new region here, set it to the active region, and draw it
                new_reg = Region( loc_id, self.parent.main_map )
                                
                # get the newely created rid, set it to active 
                self.selected_rid = self.parent.main_map.register_new_region( new_reg, self.r_layer )
                
                # self.parent.main_map.id_map( loc_id )
                
                if self._brush_size == 2:
                    # build a new region around this one
                    for ID in self.parent.main_map.get_hex_neighbors( loc_id ):
                        self.parent.main_map.add_to_region( self.selected_rid, ID, self.r_layer )

                self.redraw_region( self.selected_rid )
            else:
                # no active region, but the hex here belongs to a region. 
                # set this hexes' region to the active one 
                self.selected_rid = self.parent.main_map.id_map[self.r_layer][ loc_id ]
        else:
            if self._brush_size==1:
                try:
                    # try adding it
                    # if it can't, it raises a RegionMergeError exception
                    other_rid = self.parent.main_map.add_to_region(self.selected_rid, loc_id, self.r_layer )
                    
                    if (other_rid!=-1) and (other_rid is not None): 
                        # add_to_region returns an rid if it removes a hex from another region.
                        # it returns -1, it didn't remove anything from anywhere 
                        self.redraw_region( other_rid )
                    self.redraw_region( self.selected_rid )
                except RegionMergeError:
                    pass
                except RegionPopError:
                    pass
            elif self._brush_size==2:
                # This seems to cause some instability...
                # ...
                if loc_id not in self.parent.main_map.id_map[self.r_layer]:
                    # create and register a region
                    temp_region = Region( loc_id , self.parent.main_map )
                    new_rid = self.parent.main_map.register_new_region( temp_region, self.r_layer )

                    for ID in self.parent.main_map.get_hex_neighbors( loc_id ):
                        try:
                            self.parent.main_map.add_to_region( new_rid, ID , self.r_layer )
                        except (RegionMergeError, RegionPopError):
                            pass

                    # now merge the regions
                    try: 
                        self.parent.main_map.merge_regions( self.selected_rid, new_rid , self.r_layer)
                        self.redraw_region( self.selected_rid )
                    except RegionMergeError:
                        # delete that region, remove it
                        self.parent.main_map.remove_region( new_rid , self.r_layer )

                    #for ID in temp_region.ids:
                    #    print("Failed here")
                    #    self.parent.main_map.remove_from_region( ID )

    def reg_remove(self, event):
        """
        Tries to remove the hex under the cursor from its region.
        """
        place   = Point( event.scenePos().x(), event.scenePos().y() )
        loc_id  = self.parent.main_map.get_id_from_point( place )
        if loc_id not in self.parent.main_map.catalogue:
            return

        if loc_id not in self.parent.main_map.id_map[self.r_layer]:
            # nothing to pop
            return
        else:
            # get this hexes's region id 
            this_rid = self.parent.main_map.id_map[self.r_layer][ loc_id ]
            # remvoe this hex from that region
            try:
                self.parent.main_map.remove_from_region( loc_id, self.r_layer )
                # redraw that region
                self.redraw_region( this_rid )
            except RegionPopError:
                pass

    def redraw_region(self, reg_id ):
        """
        Redraws the region with the provided region ID.

        @ param reg_id  - region id if region to redraw.
        """

        self.redraw_region_text( reg_id )
        return()

        #self.QBrush.setStyle(6)
        self.QBrush.setStyle(1)
        self.QPen.setWidth(3)
        

        if reg_id in self._drawn_regions:
            self.parent.scene.removeItem( self._drawn_regions[ reg_id ] )
        
        try:
            reg_obj = self.parent.main_map.rid_catalogue[self.r_layer][ reg_id ]
        except KeyError:
            return

        self._set_color( reg_obj.color )

        path = QtGui.QPainterPath()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( reg_obj.perimeter + [reg_obj.perimeter[0]] ) )
        path.addPolygon( outline )

        for enclave in reg_obj.enclaves:
            enc_path = QtGui.QPainterPath()
            enc_outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw(enclave+[enclave[0]])) 
            enc_path.addPolygon( enc_outline )
            path = path.subtracted( enc_path )
        
        self._drawn_regions[reg_id] = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush)
        self._drawn_regions[reg_id].setZValue(9)


    def redraw_region_text( self, rid ):
        """
        Redraws the name of the region with the provided region id

        @param rid  - region id of region whose name should be redrawn
        """
        reg_obj = self.parent.main_map.rid_catalogue[self.r_layer][ rid ]

        if reg_obj.name=="":
            return

        dname = reg_obj.name.split(" ")
        mult_factor = 1
        if len(dname)>=6:
            split = int(len(dname)/2)
            mult_factor = 2
            dname = " ".join(dname[0:split])+"\n"+ " ".join(dname[split:])
        else:
            dname = " ".join(dname)

        if rid in self._drawn_names:
            self.parent.scene.removeItem( self._drawn_names[ rid ] )
        
        drop = QGraphicsDropShadowEffect()
        drop.setOffset(1)
        center, extent = reg_obj.get_center_size()
        font = QtGui.QFont("Fantasy")
        font_size = mult_factor*max( 12, int(extent.magnitude / len(reg_obj.name)))
        font.setPointSize( font_size )

        self._drawn_names[rid] = self.parent.scene.addText( dname, font )
        self._drawn_names[rid].setPos( center.x - 0.5*extent.x, center.y )
        #new_color = QtGui.QColor( 0.5*(255+reg_obj.color[0]), 0.5*(255+reg_obj.color[1]), 0.5*(255+reg_obj.color[0]))
        new_color= QtGui.QColor( 250, 250, 250)
        self._drawn_names[rid].setDefaultTextColor( new_color )
        self._drawn_names[rid].setGraphicsEffect( drop )
        self._drawn_names[rid].setZValue(15)
    
    def drop(self):
        """
        Removes the selection outline for the tool. Called while switching to another tool. 
        """
        if self._outline_obj is not None:
            self.parent.scene.removeItem( self._outline_obj )

    def clear(self):
        self._drawn_names = {}
        self._drawn_regions = {}
        self._outline_obj = None


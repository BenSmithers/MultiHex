from PyQt5.QtWidgets import QGraphicsScene, QGraphicsDropShadowEffect
from PyQt5 import QtGui, QtCore

from MultiHex.core import Point, Region, RegionMergeError, RegionPopError
from MultiHex.objects import Icons, Entity 

import os # used for some of the icons


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

class path_brush(basic_tool):
    """
    Basic tool implementation for drawing Path objects like rivers and roads
    """
    def __init__(self, parent):
        self._drawing = False
        self._active_path = None

        self._drawn_rivers = []

    def redraw_rivers(self):
        pass

    def move( self, event ):
        pass
    # update the position of the river icon
        

class entity_brush(basic_tool):
    """
    Basic tool implementaion for adding and editing entities on the map! 
    """
    def __init__(self, parent):
        self.parent = parent

        self._drawn_entities = {}

        # are we in the process of placing a thingy
        self._placing = False
        self._placing_type = 0

        # eID of the selected entity 
        self._selected = None
        
        # icon size should be derived from the map's drawscale.
        # fixing this will require a better and more dedicated map drawing function 
        self._drawn_icon = None
        self._icon_size = 32 #int(self.parent.main_map._drawscale*2)
        self._icon = None 
        self._all_icons = None

    def prep_new(self, ent_type = 0):
        assert( isinstance(ent_type, int))
        self._placing = True
        self._placing_type = ent_type 

    def move(self, event):
        if self._icon is None:
            self._all_icons = Icons()
            self._icon = self._all_icons.location

        # meaning we want to 
        if self._placing:
            if self._drawn_icon is None:
                self._drawn_icon = self.parent.scene.addPixmap( self._icon )
                self._drawn_icon.setZValue(20)
            else:
                self._drawn_icon.setX( event.scenePos().x() -(self._icon_size)/2 )
                self._drawn_icon.setY( event.scenePos().y() -(self._icon_size)/2 )
        else:
            if self._drawn_icon is not None:
                self.parent.scene.removeItem( self._drawn_icon )
                self._drawn_icon = None 

            
    def activate( self, event ):
        if self._placing:
            # we are going to create 
            if self._drawn_icon is not None:
                self.parent.scene.removeItem( self._drawn_icon )
                self._drawn_icon = None   
            
            place = Point( event.scenePos().x(), event.scenePos().y() ) 
            loc_id = self.parent.main_map.get_id_from_point( place )

            new_ent = Entity( "temp" , loc_id )
            new_ent.icon = self._icon
            #QtGui.QPixmap( os.path.join('..','Artwork','location.svg')).scaledToWidth(32)

            self._selected = self.parent.main_map.register_new_entity( new_ent )
            self.parent.main_map.eid_catalogue[self._selected].name = "Entity {}".format(self._selected)
            self.configure_toolbox_loc()
            self.redraw_entity( self._selected )

            print("New entity, number {}, at {}".format( self._selected, loc_id ))

            self._placing = False

    def configure_toolbox_loc(self):
        self.parent.ui.loc_name_edit.setText( self.parent.main_map.eid_catalogue[ self._selected ].name)
        self.parent.ui.loc_desc_edit.setText( self.parent.main_map.eid_catalogue[ self._selected].description)

    def redraw_entity(self, eID):
        if eID not in self.parent.main_map.eid_catalogue:
            raise ValueError("eID {} not registered in catalogue".format(eID))

        # delete old drawing if it exists
        if eID in self._drawn_entities:
            self.parent.scene.removeItem( self._drawn_entities[ eID ] )
            del self._drawn_entities[ eID ]
        
        self._drawn_entities[eID] = self.parent.scene.addPixmap( self.parent.main_map.eid_catalogue[ eID ].icon )
        self._drawn_entities[eID].setZValue(2)
        location = self.parent.main_map.get_point_from_id( self.parent.main_map.eid_catalogue[eID].location)
        self._drawn_entities[eID].setX( location.x - self.parent.main_map.eid_catalogue[eID].icon.width()/2 )
        self._drawn_entities[eID].setY( location.y - self.parent.main_map.eid_catalogue[eID].icon.height()/2)


    def drop(self):
        if self._drawn_icon is not None:
            self.parent.scene.removeItem( self._drawn_icon )

    def clear(self):
        self.drop()

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

    def activate(self, event):
        if self.writing:
            self.write(event)
        else:
            self.erase(event)
    def hold(self, event):
        self.activate(event)
    
    def move(self, event):
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
            self.drawn_hexes[hex_id].setZValue(1)

        except KeyError: #happens if told to redraw a hex that isn't there 
            #print("key error")
            pass

               
            

    def select(self,event):
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
                self._selected_out.setZValue(4)
                self._selected_id = this_id
                
                self.update_selection()

                
            else:
                # the outline object needs to be purged, otherwise it will later try erasing it again
                # we also undo our selection 
                self._selected_out = None
                self._selected_id = None

    def update_selection(self):
        pass

    
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

    def select(self, event):
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

    def hold(self, event):
        self.activate( event )

    def activate(self, event):
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
    def move(self, event):
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
        self._drawn_regions[reg_id].setZValue(5)


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


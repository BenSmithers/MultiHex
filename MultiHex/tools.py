from MultiHex.point import Point
from MultiHex.special_hexes import *

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene

class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self, parent=None):
        pass
    def press(self,event):
        """
        Called when the mouse is pressed

        @param event 
        """
        pass
    def activate(self, event):
        """
        This is called when the mouse is released from a localized click. 

        @param event - location of release
        """
        pass
    def hold(self,event, step):
        """
        Called continuously while the mouse is held

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def move(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass

class selector(basic_tool):
    """
    Tool with clicker_control interfacing used to select and spot-edit hexes
    """
    def __init__(self, parent):
        self.start = Point(0.0,0.0)
        self.selected_id  = None
        self.selected_out = None
      
        self.parent = parent

        # configure brush and pen for showing selected hex 
        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
        self.QBrush.setStyle(0)
        self.QPen.setColor(QtGui.QColor(75,75,245))
        self.QPen.setWidth(4)

    def press(self, place):
        """
        clicking isn't what's important, it's releasing 
        """
        pass
    def activate(self, place):
        """
        Mouse released. 
        """
        here = Point( place.scenePos().x(), place.scenePos().y())
        this_id = self.parent.main_map.get_id_from_point( here )

        # only bother doing things if this is a new hex we're clicking on
        if self.selected_id != this_id:
            if self.selected_out is not None:
                # so, if there already is an outline (there should be), let's erase it. We're going to draw a new hex
                self.parent.scene.removeItem( self.selected_out )
            
            # okay, now verify that we're clicking on a registered hex 
            if this_id in self.parent.main_map.catalogue:
                # draw a new hex, and select its id 
                self.selected_out = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( self.parent.main_map.catalogue[this_id]._vertices)), pen = self.QPen, brush=self.QBrush )
                self.selected_id = this_id

                # set the sliders 
                self.parent.ui.rainfall.setValue(    max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._rainfall_base*100    )))) 
                self.parent.ui.temperature.setValue( max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._temperature_base*100 ))))
                self.parent.ui.biodiversity.setValue(max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._biodiversity*100     ))))
            else:
                # the outline object needs to be purged, otherwise it will later try erasing it again
                # we also undo our selection 
                self.selected_out = None
                self.selected_id = None
            
    # these functions will be called to scale a selected hexes' properties using the sliders 
    def rainfall(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self.selected_id]._rainfall_base = float(value)/100.
    def temperature(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self.selected_id]._temperature_base = float(value)/100.
    def biodiversity(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self.selected_id]._biodiversity_base = float(value)/100.
        
    # clean yoself up 
    def drop_selector(self):
        if self.selected_out is not None:
            self.parent.scene.removeItem( self.selected_out )
            self.selected_out = None
            self.parent.ui.rainfall.setValue( 0 )
            self.parent.ui.temperature.setValue( 0 )
            self.parent.ui.biodiversity.setValue( 0 )
        self.selected_id = None


class hex_brush(basic_tool):
    """
    Another tool with clicker-control interfacing used to paint hexes on a hexmap. 

    Keeps track of all the canvas objects that it has drawn. Theres are **not** actual Hex's (TM), but just boring ass hexagons. 
    """
    def __init__(self, parent):
        self.writing = True
        self._brush_type = Grassland_Hex
        self._brush_size = 2

        self.pen_style = 0
        self.pen_size = 2

        self.parent = parent

        self.drawn_hexes = {}
        self._outline_obj = None

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
    def drop_brush(self):
        if self.parent.main_map._outline is not None:
            self.parent.scene.removeItem( self._outline_obj )
            self._outline_obj = None

    # so clicked or held, it's getting activated! 
    def activate(self, event):
        if self.writing:
            self.write(event)
        else:
            self.erase(event)
    def hold(self, event, step):
        self.move(event)
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
                self.QPen.setColor(QtGui.QColor(15,255,15))
            else:
                self.QPen.setColor(QtGui.QColor(255,15,15))


            # remove previous outline object
            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
            # redraw the selection outline

            self.QBrush.setStyle(0)
            self._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )

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
        self.QPen.setWidth(self.pen_size)
        self.QPen.setStyle(self.pen_style)
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )

        # calculate the center of a hex that would have that id
        new_hex_center = self.parent.main_map.get_point_from_id( loc_id )
        # create a hex at that point, with a radius given by the current drawscale 
        new_hex= self._brush_type( new_hex_center, self.parent.main_map._drawscale )
        
        # get the pen ready (does the outlines)
        self.QPen.setColor(QtGui.QColor( new_hex.outline[0], new_hex.outline[1], new_hex.outline[2] ))
        self.QBrush.setStyle(1)

        # register that hex in the hexmap 
        try:
            self.parent.main_map.register_hex( new_hex, loc_id )
            self.QBrush.setColor( QtGui.QColor( new_hex.fill[0], new_hex.fill[1], new_hex.fill[2] ))
            self.drawn_hexes[loc_id] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( new_hex._vertices )), pen=self.QPen, brush=self.QBrush) 
        except NameError:
            pass
        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = self.parent.main_map.get_point_from_id( neighbor )
                new_hex = self._brush_type( new_hex_center, self.parent.main_map._drawscale)
                try:
                    self.parent.main_map.register_hex( new_hex, neighbor )            
                    self.QBrush.setColor( QtGui.QColor( new_hex.fill[0], new_hex.fill[1], new_hex.fill[2]))
                    self.drawn_hexes[neighbor] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( new_hex._vertices )), pen=self.QPen, brush=self.QBrush)
                except NameError:
                    pass

    def toggle_brush_size(self):
        if self._brush_size==1:
            self._brush_size = 2 # hex and friends 
        else: 
            self._brush_size = 1 # lonely hex 

    def toggle_write(self):
        if self.writing:
            self.writing = False # erasing 
        else:
            self.writing = True

    # What kind of template to use when drawing 
    def switch_forest(self):
        self._brush_type = Forest_Hex
    def switch_grass(self):
        self._brush_type = Grassland_Hex
    def switch_mountain(self):
        self._brush_type = Mountain_Hex
    def switch_desert(self):
        self._brush_type = Desert_Hex
    def switch_ocean(self):
        self._brush_type = Ocean_Hex
    def switch_arctic(self):
        self._brush_type = Arctic_Hex

class clicker_control(QGraphicsScene):
    """
    Manages the mouse interface for to the canvas.
    """
    def __init__(self, parent=None, master=None):
        QGraphicsScene.__init__(self, parent)


        self.start = Point(0.0, 0.0)
        self.step = Point(0.0, 0.0)
        self.end   = Point(0.0, 0.0)

        self._active = None
        self._held = False
        
        self.master = master

    def mousePressEvent(self, event):
        """
        Called whenever the mouse is pressed within its bounds (The drawspace)
        """
        event.accept() # accept the event
        self._held = True # say that the mouse is being held 
        self.step =  Point( event.scenePos().x(), event.scenePos().y())
        self.start = Point( event.scenePos().x(), event.scenePos().y())
        # temp to stop break break
        self._active.press( event )

    def mouseReleaseEvent( self, event):
        """
        Called when the mouse is released 
        """
        event.accept()
        self._held = False
        self.end = Point(event.scenePos().x(), event.scenePos().y())
        diff = self.start - self.end
    #    if diff.magnitude <=5.0:
        self._active.activate(event)
            #event.widget.create_line(self.start.x, self.start.y, self.end.x, self.end.y)
            #main_map.draw_relative_to = self.end - self.start
            # self._active.hold(self.end, self.step)
 
   #mouseMoveEvent 
    def mouseMoveEvent(self,event):
        """
        called continuously as the mouse is moved within the graphics space. The "held" boolean is used to distinguish between regular moves and click-drags 
        """
        event.accept()
        if self._held:
            self._active.hold( event, self.start )
            self.step = Point( event.scenePos().x(), event.scenePos().y() )

        #    self.mouseHeld( event )
        
        self._active.move( event )

    def to_brush(self):
        """
        We need to switch over to calling the writer control, and have the selector clean itself up. These two cleaners are used to git rid of any drawn selection outlines 
        """
        self._active = self.master.writer_control
        self.master.selector_control.drop_selector()
    def to_select(self):
        """
        same for the above, but opposite 
        """
        self._active = self.master.selector_control
        self.master.writer_control.drop_brush()

 

from HexMap.point import Point
from HexMap.special_hexes import *

from PyQt4 import QtGui


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
        pass
    def activate(self, place):
        here = Point( place.scenePos().x(), place.scenePos().y())
        this_id = self.parent.main_map.get_id_from_point( here )

        if self.selected_id != this_id:
            if self.selected_out is not None:
                self.parent.scene.removeItem( self.selected_out )

            if this_id in self.parent.main_map.catalogue:
                self.selected_out = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( self.parent.main_map.catalogue[this_id]._vertices)), pen = self.QPen, brush=self.QBrush )
                self.selected_id = this_id

                self.parent.ui.rainfall.setValue(    max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._rainfall_base*100    )))) 
                self.parent.ui.temperature.setValue( max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._temperature_base*100 ))))
                self.parent.ui.biodiversity.setValue(max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._biodiversity*100     ))))
            else:
                self.selected_out = None
                self.selected_id = None
            
    def rainfall(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self.selected_id]._rainfall_base = float(value)/100.
    def temperature(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self.selected_id]._temperature_base = float(value)/100.
    def biodiversity(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self.selected_id]._biodiversity_base = float(value)/100.
        
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
    Writes hexes.
    """
    def __init__(self, parent):
        self.writing = True
        self._brush_type = Grassland_Hex
        self._brush_size = 2

        self.parent = parent

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
    def drop_brush(self):
        if self.parent.main_map._outline is not None:
            self.parent.scene.removeItem( self.parent.main_map._outline_obj )
            self.parent.main_map._outline_obj = None

    def activate(self, event):
        if self.writing:
            self.write(event)
        else:
            self.erase(event)
    def hold(self, event, step):
        
        self.move(event)
        self.activate(event)
    
    def move(self, event):
        # get center, 
        place = Point( event.scenePos().x(), event.scenePos().y())
        center_id = self.parent.main_map.get_id_from_point( place )
        self.QPen.setWidth(5)
        
        if self.parent.main_map._outline == center_id:
            # the mouse hasn't moved, skip this
            pass
        else:
            # new center! 
            self.parent.main_map._outline = center_id

            # get the outline
            outline = self.parent.main_map.get_neighbor_outline( center_id , self._brush_size)

            if self.writing:
                self.QPen.setColor(QtGui.QColor(15,255,15))
            else:
                self.QPen.setColor(QtGui.QColor(255,15,15))


            # remove previous outline object
            if self.parent.main_map._outline_obj is not None:
                self.parent.scene.removeItem( self.parent.main_map._outline_obj )
            # redraw the selection outline

            self.QBrush.setStyle(0)
            self.parent.main_map._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )

    def erase(self, event):
        place = Point(event.scenePos().x(),event.scenePos().y() )
        loc_id = self.parent.main_map.get_id_from_point( place )
        try:
            self.parent.scene.removeItem( self.parent.main_map.drawn_hexes[ loc_id ] ) 
            del self.parent.main_map.drawn_hexes[loc_id]
            self.parent.main_map.remove_hex(loc_id)
        except KeyError:
            pass 

        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors(loc_id)
            for neighbor in neighbors:
                try:
                    self.parent.scene.removeItem( self.parent.main_map.drawn_hexes[neighbor])
                    del self.parent.main_map.drawn_hexes[neighbor]
                    self.parent.main_map.remove_hex( neighbor )
                except KeyError:
                    pass



    def write(self, event):
        self.QPen.setWidth(1)
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
            self.parent.main_map.drawn_hexes[loc_id] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( new_hex._vertices )), pen=self.QPen, brush=self.QBrush) 

            #self.parent.main_map.draw_one_hex( event.widget, loc_id )
        except NameError:
            # don't actually want this
            # self.parent.main_map.set_active_hex( loc_id )
            # if there is already a hex there, just set that hex as the active one
            pass
        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = self.parent.main_map.get_point_from_id( neighbor )
                new_hex = self._brush_type( new_hex_center, self.parent.main_map._drawscale)
                try:
                    self.parent.main_map.register_hex( new_hex, neighbor )            
                    self.QBrush.setColor( QtGui.QColor( new_hex.fill[0], new_hex.fill[1], new_hex.fill[2]))
                    self.parent.main_map.drawn_hexes[neighbor] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( new_hex._vertices )), pen=self.QPen, brush=self.QBrush)
        
                except NameError:
                    pass

    def toggle_brush_size(self):
        if self._brush_size==1:
            self._brush_size = 2 
        else: 
            self._brush_size = 1

    def toggle_write(self):
        if self.writing:
            self.writing = False
        else:
            self.writing = True

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



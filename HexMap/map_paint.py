## #!/usr/bin/python3.6m

from HexMap.point import Point
from HexMap.hex import Hex
from HexMap.hexmap import Hexmap
from HexMap.hexmap import save_map, load_map
from HexMap.special_hexes import *
from HexMap.tools import *
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui

from HexMap.guis.editor import Ui_MainWindow

import sys # basic command line interface 
import os  # basic file-checking, detecting os


screen_ratio = 0.8

# loaded maps need to be drawn
#need_to_draw = False
#if len(sys.argv) > 1:
#    in_file = sys.argv[1]
#    if in_file.split(".")[-1]=="hexmap":
#        if os.path.exists( in_file ):
#            print("Loading "+in_file)
#            main_map = load_map( in_file )
#            need_to_draw = True
#        else:
#            main_map = Hexmap() 
#    else:
#        main_map = Hexmap() 
#else:
#    main_map = Hexmap() 

# open the gui



class clicker_control(QtGui.QGraphicsScene):
    """
    Manages the mouse interface for to the canvas 
    """
    def __init__(self, parent=None, master=None):
        QtGui.QGraphicsScene.__init__(self, parent)


        self.start = Point(0.0, 0.0)
        self.step = Point(0.0, 0.0)
        self.end   = Point(0.0, 0.0)

        self._active = None
        self._held = False
        
        self.master = master

    def mousePressEvent(self, event):
        event.accept()
        self._held = True
        self.step =  Point( event.scenePos().x(), event.scenePos().y())
        self.start = Point( event.scenePos().x(), event.scenePos().y())
        # temp to stop break break
        self._active.press( event )

    def mouseReleaseEvent( self, event):
        event.accept()
        self._held = False
        self.end = Point(event.scenePos().x(), event.scenePos().y())
        diff = self.start - self.end
    #    if diff.magnitude <=5.0:
        self._active.activate(event)
            #event.widget.create_line(self.start.x, self.start.y, self.end.x, self.end.y)
            #main_map.draw_relative_to = self.end - self.start
            # self._active.hold(self.end, self.step)

    def scroll(self, event):
        #print("change: {}".format(event.delta))
        
        main_map.draw_relative_to += (main_map.origin_shift - Point(event.scenePos().x(),event.scenePos().y()) )*(1./main_map._zoom)
        main_map.origin_shift = Point(event.scenePos().x(), event.scenePos().y())
        main_map._zoom += (event.delta/120.)*0.05
        main_map.draw( event.widget )

   #mouseMoveEvent 
    def mouseMoveEvent(self,event):
        event.accept()
        if self._held:
            self._active.hold( event, self.start )
            self.step = Point( event.scenePos().x(), event.scenePos().y() )

        #    self.mouseHeld( event )
        
        self._active.move( event )

    def to_brush(self):
        self._active = self.master.writer_control
        self.master.selector_control.drop_selector()
    def to_select(self):
        self._active = self.master.selector_control
        self.master.writer_control.drop_brush()

  


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


class editor_gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.writer_control = hex_brush(self)
        self.selector_control = selector(self)

        self.scene = clicker_control( self.ui.graphicsView, self )

        #def open_map( target = '' ):
        #    global main_map    
        #    global editor_instance
        #    global scene
        #    global applicaiton

        self.scene._active = self.writer_control
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )


        self.ui.brush.clicked.connect( self.scene.to_brush )
        self.ui.hand.clicked.connect( self.scene.to_select )


        self.ui.pushButton_7.clicked.connect( self.writer_control.switch_desert )
        self.ui.pushButton_8.clicked.connect( self.writer_control.switch_arctic )
        self.ui.pushButton_9.clicked.connect( self.writer_control.switch_mountain )
        self.ui.Forest.clicked.connect( self.writer_control.switch_forest )
        self.ui.Ocean.clicked.connect( self.writer_control.switch_ocean )
        self.ui.Grassland.clicked.connect( self.writer_control.switch_grass )
        self.ui.brushTottle.clicked.connect( self.writer_control.toggle_brush_size )
        self.ui.write_erase.clicked.connect( self.writer_control.toggle_write )
        QtCore.QObject.connect( self.ui.rainfall, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.rainfall)
        QtCore.QObject.connect( self.ui.temperature, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.temperature)
        QtCore.QObject.connect( self.ui.biodiversity, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.biodiversity)
        #self.ui.rainfall.clicked.connect(selector_control.rainfall)
        #toggle_write

        self.ui.brush.setChecked(True)
    
        self.main_map = Hexmap()

    def prep_map(self, file_name ):
        self.main_map = load_map( file_name )
        
        newpen = QtGui.QPen()
        newbrush=QtGui.QBrush()
        newbrush.setStyle(1)
        for ID in self.main_map.catalogue:
            dahex = self.main_map.catalogue[ID]
            newpen.setColor(QtGui.QColor( dahex.outline[0], dahex.outline[1], dahex.outline[2]))
            newbrush.setColor(QtGui.QColor( dahex.fill[0], dahex.fill[1], dahex.fill[2] ))
            newpen.setWidth(1)
            self.main_map.drawn_hexes[ID] = self.scene.addPolygon( QtGui.QPolygonF(self.main_map.points_to_draw(dahex._vertices )), pen = newpen, brush= newbrush )


#application = QtGui.QApplication(sys.argv)
#editor_instance = gui()

#thing = open_map()
#thing.show()
#sys.exit( applicaiton.exec_() )
    #    return( editor_instance )

#if __name__=="__main__":
#    
#    editor_instance.show()
#    sys.exit(application.exec_())



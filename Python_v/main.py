## #!/usr/bin/python3.6m

from point import Point
from hex import Hex
from hexmap import Hexmap
from hexmap import save_map, load_map
from special_hexes import *
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui

#from PyQt4.QtWidgets import QGraphicsScene
from display import Ui_MainWindow

import sys # basic command line interface 
import os  # basic file-checking, detecting os

screen_ratio = 0.8

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# loaded maps need to be drawn
need_to_draw = False
if len(sys.argv) > 1:
    in_file = sys.argv[1]
    if in_file.split(".")[-1]=="hexmap":
        if os.path.exists( in_file ):
            print("Loading "+in_file)
            main_map = load_map( in_file )
            need_to_draw = True
        else:
            main_map = Hexmap() 
    else:
        main_map = Hexmap() 
else:
    main_map = Hexmap() 

# open the gui
class gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QtGui.QApplication(sys.argv)
app_instance = gui()


def savesave():
    save_map(main_map, "saves/test.hexmap")

class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self):
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


class clicker_control(QtGui.QGraphicsScene):
    """
    Manages the mouse interface for to the canvas 
    """
    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)


        self.start = Point(0.0, 0.0)
        self.step = Point(0.0, 0.0)
        self.end   = Point(0.0, 0.0)

        self._active = None
        self._held = False
        

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
        writer_control.set_brush_small()
        self._active = writer_control
  #      app_instance.ui.hand.setChecked(False)
    def to_select(self):

        self._active = selector_control
 #       app_instance.ui.brush.setChecked(True)

  
#    def setMouseTracking(self, flag):
#        def recursive_set(parent):
#            for child in parent.findChildren(QtCore.QObject):
#                try:
#                    child.setMouseTracking(flag)
#                except:
#                    pass
#                recursive_set(child)
#        QtGui.QWidget.setMouseTracking(self, flag)
#        recursive_set(self)

#controlle = clicker_control()

#scene = clicker_control( app_instance.ui.centralwidget )

scene = clicker_control( app_instance.ui.graphicsView )

class selector(basic_tool):
    def __init__(self):
        self.start = Point(0.0,0.0)
        self.selection = None

    def press(self, place):
        pass
    def activate(self, place):
        pass


class hex_brush(basic_tool):
    """
    Writes hexes.
    """
    def __init__(self):
        self.writing = True
        self._brush_type = Grassland_Hex
        self._brush_size = 2

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()

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
        center_id = main_map.get_id_from_point( place )
        self.QPen.setWidth(5)
        
        if main_map._outline == center_id:
            # the mouse hasn't moved, skip this
            pass
        else:
            # new center! 
            main_map._outline = center_id

            # get the outline
            outline = main_map.get_neighbor_outline( center_id , self._brush_size)

            if self.writing:
                self.QPen.setColor(QtGui.QColor(15,255,15))
            else:
                self.QPen.setColor(QtGui.QColor(255,15,15))


            # remove previous outline object
            if main_map._outline_obj is not None:
                scene.removeItem( main_map._outline_obj )
            # redraw the selection outline

            self.QBrush.setStyle(0)
            main_map._outline_obj = scene.addPolygon( QtGui.QPolygonF( main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )

    def erase(self, event):
        place = Point(event.scenePos().x(),event.scenePos().y() )
        loc_id = main_map.get_id_from_point( place )
        try:
            scene.removeItem( main_map.drawn_hexes[ loc_id ] ) 
            del main_map.drawn_hexes[loc_id]
            main_map.remove_hex(loc_id)
        except KeyError:
            pass 

        if self._brush_size ==2:
            neighbors = main_map.get_hex_neighbors(loc_id)
            for neighbor in neighbors:
                try:
                    scene.removeItem( main_map.drawn_hexes[neighbor])
                    del main_map.drawn_hexes[neighbor]
                    main_map.remove_hex( neighbor )
                except KeyError:
                    pass



    def write(self, event):
        self.QPen.setWidth(2)
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = main_map.get_id_from_point( place )

        # calculate the center of a hex that would have that id
        new_hex_center = main_map.get_point_from_id( loc_id )
        # create a hex at that point, with a radius given by the current drawscale 
        new_hex= self._brush_type( new_hex_center, main_map._drawscale )
        
        # get the pen ready (does the outlines)
        self.QPen.setColor(QtGui.QColor( new_hex.outline[0], new_hex.outline[1], new_hex.outline[2] ))
        self.QBrush.setStyle(1)

        # register that hex in the hexmap 
        try:
            main_map.register_hex( new_hex, loc_id )

            self.QBrush.setColor( QtGui.QColor( new_hex.fill[0], new_hex.fill[1], new_hex.fill[2] ))
            main_map.drawn_hexes[loc_id] = scene.addPolygon( QtGui.QPolygonF( main_map.points_to_draw( new_hex._vertices )), pen=self.QPen, brush=self.QBrush) 

            #main_map.draw_one_hex( event.widget, loc_id )
        except NameError:
            # don't actually want this
            # main_map.set_active_hex( loc_id )
            # if there is already a hex there, just set that hex as the active one
            pass
        if self._brush_size ==2:
            neighbors = main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = main_map.get_point_from_id( neighbor )
                new_hex = self._brush_type( new_hex_center, main_map._drawscale)
                try:
                    main_map.register_hex( new_hex, neighbor )            
                    self.QBrush.setColor( QtGui.QColor( new_hex.fill[0], new_hex.fill[1], new_hex.fill[2]))
                    main_map.drawn_hexes[neighbor] = scene.addPolygon( QtGui.QPolygonF( main_map.points_to_draw( new_hex._vertices )), pen=self.QPen, brush=self.QBrush)
        
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


writer_control = hex_brush()
selector_control = selector()

scene._active = writer_control
app_instance.ui.graphicsView.setMouseTracking(True)
#app_instance.ui.graphicsView.setTransformationAnchor( 0 )
#app_instance.ui.graphicsView.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
#app_instance.ui.graphicsView.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
#app_instance.ui.graphicsView.horizontalScrollBar().disconnect()
#app_instance.ui.graphicsView.verticalScrollBar().disconnect()


#app_instance.ui.graphicsView = clicker_control( app_instance.ui.centralwidget )
#app_instance.ui.graphicsView.setObjectName(_fromUtf8("graphicsView"))

app_instance.ui.graphicsView.setScene( scene )


app_instance.ui.brush.clicked.connect( scene.to_brush )
app_instance.ui.hand.clicked.connect( scene.to_select )


app_instance.ui.pushButton_7.clicked.connect( writer_control.switch_desert )
app_instance.ui.pushButton_8.clicked.connect( writer_control.switch_arctic )
app_instance.ui.pushButton_9.clicked.connect( writer_control.switch_mountain )
app_instance.ui.Forest.clicked.connect( writer_control.switch_forest )
app_instance.ui.Ocean.clicked.connect( writer_control.switch_ocean )
app_instance.ui.Grassland.clicked.connect( writer_control.switch_grass )
app_instance.ui.brushTottle.clicked.connect( writer_control.toggle_brush_size )
app_instance.ui.write_erase.clicked.connect( writer_control.toggle_write )
#toggle_write

if need_to_draw:
    newpen = QtGui.QPen()
    newbrush=QtGui.QBrush()
    newbrush.setStyle(1)
    for ID in main_map.catalogue:
        dahex = main_map.catalogue[ID]
        newpen.setColor(QtGui.QColor( dahex.outline[0], dahex.outline[1], dahex.outline[2]))
        newbrush.setColor(QtGui.QColor( dahex.fill[0], dahex.fill[1], dahex.fill[2] ))
        main_map.drawn_hexes[ID] = scene.addPolygon( QtGui.QPolygonF(main_map.points_to_draw(dahex._vertices )), pen = newpen, brush= newbrush )


#update again
if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())

# frame.destroy()

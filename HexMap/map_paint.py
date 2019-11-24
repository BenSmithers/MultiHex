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

  

class editor_gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.paent = parent
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

        self.ui.pushButton_5.clicked.connect( self.go_away )
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
    def go_away(self):
        self.main_map = None
        self.parent().show()
        self.hide()

    def prep_map(self, file_name ):
        self.scene.clear()
        self.ui.graphicsView.update
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



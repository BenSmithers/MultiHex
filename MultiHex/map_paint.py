## #!/usr/bin/python3.6m

from MultiHex.point import Point
from MultiHex.hex import Hex
from MultiHex.hexmap import Hexmap
from MultiHex.hexmap import save_map, load_map
from MultiHex.special_hexes import *

# need these to define all the interfaces between the canvas and the user
from MultiHex.tools import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget

from MultiHex.guis.editor import Ui_MainWindow

import sys # basic command line interface 
import os  # basic file-checking, detecting os


screen_ratio = 0.8

  

class editor_gui(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # writes hexes on the screen
        self.writer_control = hex_brush(self)
        self.selector_control = selector(self)

        # manages the writer and selector controls. This catches clicky-events on the graphicsView
        self.scene = clicker_control( self.ui.graphicsView, self )

        #def open_map( target = '' ):
        #    global main_map    
        #    global editor_instance
        #    global scene
        #    global applicaiton

        # start with the hex as the currently used tool
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
        
        # need to fix the sliders
        #QtCore.QObject.connect( self.ui.rainfall, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.rainfall)
        #QtCore.QObject.connect( self.ui.temperature, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.temperature)
        #QtCore.QObject.connect( self.ui.biodiversity, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.biodiversity)
        
        
        #self.ui.rainfall.clicked.connect(selector_control.rainfall)
        #toggle_write
        self.ui.pushButton_5.clicked.connect( self.go_away )
        self.ui.pushButton_4.clicked.connect( self.save_map )
        self.ui.pushButton_6.clicked.connect( self.save_as )
        self.ui.brush.setChecked(True)
        
        
        self.file_name = ''
        self.main_map = Hexmap()

    def go_away(self):
        # show the main menu and disappear 
        self.parent().show()
        # need to clear the canvas too!
        self.hide()
        
        self.selector_control.selected_id = None
        self.selector_control.selected_out = None
        self.writer_control.drawn_hexes = {}
        self.writer_control._outline_obj = None
        self.scene._held = None

    def save_map(self):
        save_map( self.main_map, self.file_name)
        self.ui.label_2.setText("Saved!")

    def save_as(self):
        self.file_name = QtGui.QFileDialog.getSaveFileName(None, 'Save HexMap', './saves', 'HexMaps (*.hexmap)')
        self.save_map()



    def prep_map(self, file_name ):
        self.scene.clear()
            
        self.ui.graphicsView.update()
        self.main_map = load_map( file_name )
        self.file_name = file_name 

        newpen = QtGui.QPen()
        newbrush=QtGui.QBrush()
        newbrush.setStyle(1)
        newpen.setWidth( self.writer_control.pen_size )
        newpen.setStyle( self.writer_control.pen_style )

        for ID in self.main_map.catalogue:
            dahex = self.main_map.catalogue[ID]
            newpen.setColor(QtGui.QColor( dahex.outline[0], dahex.outline[1], dahex.outline[2]))
            newbrush.setColor(QtGui.QColor( dahex.fill[0], dahex.fill[1], dahex.fill[2] ))
            self.writer_control.drawn_hexes[ID] = self.scene.addPolygon( QtGui.QPolygonF(self.main_map.points_to_draw(dahex._vertices )), pen = newpen, brush= newbrush )


# this stuff is commented out since this script is not meant to be called directly! 

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



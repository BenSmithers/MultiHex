from HexMap.point import Point
from HexMap.hex import Hex
from HexMap.hexmap import Hexmap
from HexMap.hexmap import save_map
from HexMap.special_hexes import Mountain_Hex

from HexMap.tools import *

from PyQt4 import QtCore, QtGui
from HexMap.guis.ridge_editor_gui import ridge_gui_window

from HexMap.generator.full_chain import ridge_onward

import sys

class ridge_gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = ridge_gui_window()
        self.ui.setupUi(self)

        self.main_map = Hexmap()
        
        # give this a hex brush and make it paint Mountains
        self.writer_control = hex_brush(self)
        self.writer_control._brush_type = Mountain_Hex

        self.scene = clicker_control( self.ui.graphicsView, self )

        self.scene._active = self.writer_control

        self.ui.graphicsView.setMouseTracking( True )
        self.ui.graphicsView.setScene( self.scene )

        self.ui.pushButton_2.clicked.connect( self.writer_control.toggle_brush_size ) 
        self.ui.pushButton.clicked.connect( self.writer_control.toggle_write) 
        self.ui.pushButton_4.clicked.connect( self.save_continue ) 
        self.ui.pushButton_3.clicked.connect( self.go_away ) #quit


        self.save_name = "./saves/generated.hexmap"

    def save_continue(self):
        dupl = self.main_map
        save_map( dupl , self.save_name )
        self.main_map = None
        self.hide()
        ridge_onward('cont',self.save_name)
        self.parent().show()
        self.parent().load_int()


    def go_away(self):
        pass
        #self.main_map = None


#appy = QtGui.QApplication(sys.argv)
#thign = ridge_gui()

#thign.show()
#sys.exit( appy.exec_())

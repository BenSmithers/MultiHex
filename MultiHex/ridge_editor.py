from MultiHex.point import Point
from MultiHex.hex import Hex
from MultiHex.hexmap import Hexmap
from MultiHex.hexmap import save_map
from MultiHex.special_hexes import Mountain_Hex

from MultiHex.tools import *

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget

from MultiHex.guis.ridge_editor_gui import ridge_gui_window
from MultiHex.generator.full_chain import ridge_onward

import os
import sys

class ridge_gui(QMainWindow):
    """
    Basically just a shitty version of the main map editor... 

    just has fewer buttons. yay
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = ridge_gui_window()
        self.ui.setupUi(self)

        self.main_map = Hexmap()
        
        # give this a hex brush and make it paint Mountains
        self.writer_control = hex_brush(self)
        self.writer_control._brush_type = Ridge_Hex

        self.scene = clicker_control( self.ui.graphicsView, self )

        self.scene._active = self.writer_control

        self.ui.graphicsView.setMouseTracking( True )
        self.ui.graphicsView.setScene( self.scene )

        self.ui.pushButton_2.clicked.connect( self.writer_control.toggle_brush_size ) 
        self.ui.pushButton.clicked.connect( self.writer_control.toggle_mode) 
        self.ui.pushButton_4.clicked.connect( self.save_continue ) 
        self.ui.pushButton_3.clicked.connect( self.go_away ) #quit


        self.save_name = os.path.join(os.path.dirname(__file__),"saves","generated.hexmap")

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

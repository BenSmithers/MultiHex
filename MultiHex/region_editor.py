from MultiHex.point import Point
from MultiHex.hex import Hex
from MultiHex.hexmap import Hexmap
from MultiHex.hexmap import save_map, load_map
from MultiHex.special_hexes import Mountain_Hex
from MultiHex.tools import *

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget

from MultiHex.guis.region_editor_gui import region_gui_window

import os
import sys

class region_gui(QMainWindow):
    """
    Basically just a shitty version of the main map editor... 

    just has fewer buttons. yay
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = region_gui_window()
        self.ui.setupUi(self)

        self.main_map = Hexmap()
        self.writer_control = hex_brush(self) 
        self.region_control = region_brush(self)

        self.scene = clicker_control( self.ui.graphicsView, self )

        self.scene._active = self.region_control 

        self.ui.graphicsView.setMouseTracking( True )
        self.ui.graphicsView.setScene( self.scene )


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
    
    def prep_map(self, file_name ):
        """
        Needs to be alled when the map is first loaded. This actually has Qt draw all the hexes in the map's hexmap
        """
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


#appy = QtGui.QApplication(sys.argv)
#thign = ridge_gui()

#thign.show()
#sys.exit( appy.exec_())

## #!/usr/bin/python3.6m

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import clicker_control
from MultiHex.map_types.overland import OHex_Brush, Biome_Brush

# need these to define all the interfaces between the canvas and the user
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog

from MultiHex.guis.terrain_editor_gui import editor_gui_window

import sys # basic command line interface 
import os  # basic file-checking, detecting os


screen_ratio = 0.8

  

class editor_gui(QMainWindow):
    """
    This class creates the gui for the main world editor.
    It imports the gui definitions from the guis folder and plugs buttons, switches, and sliders  in to various functions 

    Some important TOOLS used are 
        clicker control
        hex brush
        selector
    All are defined in the tools folder 

    It also needs a  
        Hexmap
    object which defines the hexmap it shows and edits. 

    """

    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = editor_gui_window()
        self.ui.setupUi(self)
        
        # writes hexes on the screen

        # manages the writer and selector controls. This catches clicky-events on the graphicsView
        self.scene = clicker_control( self.ui.graphicsView, self )
        # start with the hex as the currently used tool
        self.writer_control = OHex_Brush(self)
        self.region_control = Biome_Brush(self)
       
        
        self.scene._active = self.writer_control

        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        self.ui.hexBrush.clicked.connect( self.scene.to_hex )
        self.ui.radioButton.clicked.connect( self.scene.to_region)

        #button doesn't exist anymore
#        self.ui.hand.clicked.connect( self.scene.to_select )

        # connect all the buttons to the writer, selector, and some ui functions
        self.ui.pushButton_5.clicked.connect( self.go_away )
        self.ui.pushButton_7.clicked.connect( self.writer_control.switch_desert )
        self.ui.pushButton_8.clicked.connect( self.writer_control.switch_arctic )
        self.ui.pushButton_9.clicked.connect( self.writer_control.switch_mountain )
        self.ui.Ridge.clicked.connect( self.writer_control.switch_ridge)
        self.ui.Forest.clicked.connect( self.writer_control.switch_forest )
        self.ui.Ocean.clicked.connect( self.writer_control.switch_ocean )
        self.ui.Grassland.clicked.connect( self.writer_control.switch_grass )
        self.ui.brushToggle.clicked.connect( self.brushToggle_clicked)
        #self.ui.write_erase.clicked.connect( self.writer_control.toggle_write )
        
        # TODO fix the sliders
        #QtCore.QObject.connect( self.ui.rainfall, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.rainfall)
        #QtCore.QObject.connect( self.ui.temperature, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.temperature)
        #QtCore.QObject.connect( self.ui.biodiversity, QtCore.SIGNAL('valueChanged(int)'), self.selector_control.biodiversity)
        
        self.ui.hexBrush.setChecked(True)
        self.ui.brushSize.valueChanged.connect( self.brushSizeChanged )
        self.ui.RegButton.clicked.connect( self.set_region_name ) 
        self.ui.pushButton_5.clicked.connect( self.go_away )
        self.ui.pushButton_4.clicked.connect( self.save_map )
        self.ui.pushButton_6.clicked.connect( self.save_as )
        self.ui.brushToggle.setChecked(True)
         
        
        self.file_name = ''
        self.main_map = Hexmap()

    def go_away(self):
        # show the main menu and disappear 
        self.parent().show()
        # need to clear the canvas too!
        self.hide()
        
        self.region_control.clear()
        self.selected_rid = None

        self.writer_control.clear()
        self.scene._held = None

    def set_region_name(self):
        # this needs to be fixed!
        if self.region_control.selected_rid is None:
            return
        else:
            self.main_map.rid_catalogue['biome'][self.region_control.selected_rid].name = self.ui.RegEdit.text()
            print("Setting Region Name to {}".format(self.ui.RegEdit.text()))

        self.region_control.redraw_region_text( self.region_control.selected_rid )

    def brushSizeChanged( self ):
        # new val is self.ui.brushSize.value()
        self.writer_control.set_brush_size( self.ui.brushSize.value() )
        self.region_control.set_brush_size( self.ui.brushSize.value() )

    def brushToggle_clicked(self, state):
        self.writer_control.toggle_mode( state )
        self.region_control.toggle_mode( state )

    def save_map(self):
        save_map( self.main_map, self.file_name)
        self.ui.label_2.setText("Saved!")

    def save_as(self):
        """
        Opens a dialog to accept a filename from the user, then calls the save_map function
        """
        self.file_name = QFileDialog.getSaveFileName(None, 'Save HexMap', './saves', 'HexMaps (*.hexmap)')
        self.save_map()



    def prep_map(self, file_name ):
        """
        Needs to be alled when the map is first loaded. This actually has Qt draw all the hexes in the map's hexmap
        """
        self.scene.clear()
            
        self.ui.graphicsView.update()
        self.main_map = load_map( file_name )
        self.file_name = file_name 
        
        print("Drawing hexes... ", end='')
        for ID in self.main_map.catalogue: 
            self.writer_control.redraw_hex( ID )
            
        print("done")
        print("Drawing biomes... ", end='')
        if self.region_control.r_layer in self.main_map.rid_catalogue :
            for rid in self.main_map.rid_catalogue[self.region_control.r_layer]:
                self.region_control.redraw_region( rid )
        print("done")
        print("Drawing rivers... ", end='')
        self.writer_control.redraw_rivers()
        print("done")
        



## #!/usr/bin/python3.6m

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import clicker_control
from MultiHex.map_types.overland import OHex_Brush, Biome_Brush

# need these to define all the interfaces between the canvas and the user
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QDialog

from MultiHex.guis.terrain_editor_gui import editor_gui_window
from MultiHex.about_class import about_dialog

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
         
        self.file_name = ''
        self.main_map = Hexmap()

        # toolbar buttons
        self.ui.tool_hex_select.clicked.connect( self.tb_hex_select )
        self.ui.tool_hex_brush.clicked.connect( self.tb_hex_brush )
        self.ui.tool_detail.clicked.connect( self.tb_detailer )
        self.ui.tool_riv_but.clicked.connect( self.tb_new_river )
        self.ui.tool_biome_but.clicked.connect( self.tb_new_biome )

        # Detailer toolbox connections
        self.ui.det_noise_combo.currentIndexChanged.connect( self.det_comboBox_select )
        self.ui.det_but_noise.clicked.connect( self.det_inject_button )
        self.ui.det_but_color.clicked.connect( self.det_color_button )
        self.ui.det_apply_button.clicked.connect( self.det_apply_button )

        # Hexbar toolbox connections
        self.ui.hex_type_combo.currentIndexChanged.connect( self.det_comboBox_select )
        self.ui.hex_list_entry = QtGui.QStandardItemModel() 
        self.ui.hex_sub_list.setModel( self.ui.hex_list_entry )
        self.ui.hex_sub_list.clicked[QtCore.QModelIndex].connect( self.hex_subtype_clicked )
        self.ui.hex_brush_disp.valueChanged.connect( self.hex_brush_change )

        # river toolbox connections
        #   first all the list stuff
        self.ui.river_list_entry = QtGui.QStandardItemModel()
        self.ui.tributary_list_entry = QtGui.QStandardItemModel()
        self.ui.river_list.setModel( self.ui.river_list_entry )
        self.ui.river_trib_list.setModel( self.ui.tributary_list_entry )
        self.ui.river_list.clicked[QtCore.QModelIndex].connect( self.river_list_click )
        self.ui.river_trib_list.clicked[QtCore.QModelIndex].connect( self.river_trib_click )
        # now all the buttons
        self.ui.riv_but_pstart.clicked.connect( self.river_ps )
        self.ui.riv_but_pend.clicked.connect( self.river_pe )
        self.ui.riv_but_astart.clicked.connect( self.river_as )
        self.ui.riv_but_aend.clicked.connect( self.river_ae )
        self.ui.riv_but_delete.clicked.connect( self.river_delete )

        #biome painter buttons
        self.ui.bio_name_but_gen.clicked.connect( self.biome_name_gen )
        self.ui.biome_but_apply.clicked.connect( self.biome_apply )

        # drop-down menu buttons
        self.ui.actionSave.triggered.connect( self.save_map )
        self.ui.actionSave_As.triggered.connect( self.save_as )
        self.ui.actionQuit.triggered.connect( self.go_away )
        self.ui.actionAbout_MultiHex.triggered.connect( self.menu_help )
        self.ui.actionTemperature.triggered.connect( self.menu_heatmap_temperature )
        self.ui.actionAltitude.triggered.connect( self.menu_heatmap_altitude )
        self.ui.actionRainfall.triggered.connect( self.menu_heatmap_rainfall )
        self.ui.actionBiome_Names.triggered.connect( self.menu_view_biome_name )
        self.ui.actionBiome_Borders.triggered.connect( self.menu_view_biome_border )
        self.ui.actionRivers.triggered.connect( self.menu_view_rivers )

    def tb_hex_select(self):
        pass

    def tb_detailer(self):
        pass

    def tb_hex_brush(self):
        pass

    def tb_new_river(self):
        pass

    def tb_new_biome(self):
        pass

    def det_comboBox_select(self):
        pass

    def det_inject_button(self):
        pass

    def det_color_button(self):
        pass

    def det_apply_button(self):
        pass

    def hex_comboBox_select(self):
        pass

    def hex_subtype_clicked(self, index=None):
        pass

    def hex_brush_change(self):
        pass

    def river_list_click(self, index=None):
        pass

    def river_trib_click(self, index=None):
        pass

    def river_ps(self):
        pass

    def river_pe(self):
        pass

    def river_as(self):
        pass

    def river_ae(self):
        pass

    def river_delete(self):
        pass

    def biome_name_gen(self):
        pass

    def biome_apply(self):
        pass

    def menu_open(self):
        pass

    def menu_view_biome_name(self):
        pass

    def menu_view_biome_border(self):
        pass

    def menu_view_rivers(self):
        pass

    def menu_heatmap_altitude(self):
        pass

    def menu_heatmap_temperature(self):
        pass

    def menu_heatmap_rainfall(self):
        pass

    def menu_help(self):
        dialog = about_dialog(self)
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()

    def go_away(self):
        # show the main menu and disappear 
        self.parent().show()
        # need to clear the canvas too!
        self.hide()
        
        self.region_control.clear()
        self.selected_rid = None

        self.writer_control.clear()
        self.scene._held = None


    def save_map(self):
        save_map( self.main_map, self.file_name)

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
        


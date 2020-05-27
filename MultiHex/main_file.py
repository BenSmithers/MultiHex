from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QApplication, QWidget

import os
import sys 
import json

# standard GUI
from MultiHex.guis.main_gui import main_gui

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import basic_tool
from MultiHex.objects import Icons
from MultiHex.map_types.overland import OEntity_Brush, OHex_Brush, Road_Brush, County_Brush, Nation_Brush, Nation, Biome_Brush, River_Brush, ol_clicker_control, Detail_Brush
from MultiHex.about_class import about_dialog
from MultiHex.generator.util import get_tileset_params, create_name, Climatizer

# import other guis! 
from MultiHex.guis.terrain_editor_gui import terrain_ui
from MultiHex.guis.civ_gui import civ_ui
from MultiHex.guis.new_load_gui import new_load_gui

class main_window(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        # standard boiler-plate gui initialization
        # we instantiate the default GUI before anything else 
        self.ui = main_gui()
        self.ui.setupUi(self) 

        # now we need to set up the default tools 
        self.hex_control = OHex_Brush(self)
        self.entity_control = OEntity_Brush(self)
        self.path_control = Road_Brush(self)
        self.river_control = River_Brush(self)
        self.biome_control = Biome_Brush(self) #we'll need to remember to change this when switching between CIV and Terrain modes
        self.county_control = County_Brush( self )
        self.county_control.small_font = False
        self.nation_control = Nation_Brush(self)
        self.detail_control = Detail_Brush(self)
        self.climatizer = Climatizer( "standard" )

        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.scene = ol_clicker_control( self.ui.graphicsView, self )
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        # start off with a nothing tool.
        # any mouse commands will just be thrown in the trash 
        self.scene._active = basic_tool(self)
        
        # set up the action bar! 
        self.ui.actionQuit.triggered.connect( self.quit )
        self.ui.actionSave.triggered.connect( self.save_map )
        self.ui.actionSave_As.triggered.connect( self.save_as)
        self.ui.actionOpen.triggered.connect( self.open )
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionTerrainEditor.triggered.connect(self.switch_to_terrain)
        self.ui.actionCivEditor.triggered.connect(self.switch_to_civilization)

        self._ui_clear_function = None
        self.extra_ui = None

        loc = os.path.join(os.path.dirname(__file__),'resources', 'tilesets.json')
        file_object = open( loc, 'r')
        self.config = json.load( file_object )
        file_object.close()
        self.params = []

        self.icons = Icons()

    def smart_ui_chooser(self):
        self.switch_to_terrain()

    def switch_to_terrain(self):
        self.scene.drop()
        if self._ui_clear_function is not None:
            self._ui_clear_function(self.ui)
        self.extra_ui = terrain_ui(self)
        self.ui.actionCivEditor.setChecked(False)
        self.ui.actionTerrainEditor.setChecked(True)
        self._ui_clear_function = self.extra_ui.clear_ui


    def switch_to_civilization(self):
        self.scene.drop()
        if self._ui_clear_function is not None:
            self._ui_clear_function(self.ui)

        self.extra_ui = civ_ui(self)
        self.ui.actionCivEditor.setChecked(True)
        self.ui.actionTerrainEditor.setChecked(False)
        self._ui_clear_function = self.extra_ui.clear_ui

    def show(self):
        QMainWindow.show(self)
        # this either has MH load a map or make a new map 
        self.main_map = None
        while self.main_map is None:
            dialog = new_load_dialog(self)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def new(self):
        pass

    def open(self):
        pass

    def load(self):
        """
        Called when we want to load a new map
        """
        self.filename = QFileDialog.getOpenFileName(None, 'Open HexMap', os.path.join(os.path.dirname(__file__), "saves"), 'HexMaps (*.hexmap)')[0]
        if self.filename is None:
            return
        elif not os.path.exists(self.filename): 
            # either the user chose something that doesn't exist, or they canceled 
            return

        self.ui.graphicsView.update()
        self.main_map = load_map( self.filename )
        self.smart_ui_chooser()
        self.params = get_tileset_params( self.main_map.tileset )

        print("Drawing hexes... ", end='')
        self._redraw_hexes()
        print("done")
        print("Drawing biomes... ", end='')
        self._redraw_biomes()
        print("done")
        print("Drawing rivers... ", end='')
        self.river_control.redraw_rivers()
        print("done")
        print("Drawing everything else...",end='')
        self._redraw_entities()
        self._redraw_roads()
        self._redraw_counties()
        print("done")
        

    def _redraw_hexes(self):
        for ID in self.main_map.catalogue: 
            self.hex_control.redraw_hex( ID )
    def _redraw_biomes(self):
        if 'biome' in self.main_map.rid_catalogue :
            for rid in self.main_map.rid_catalogue['biome']:
                self.biome_control.redraw_region( rid )
    def _redraw_entities(self):
        for hexID in self.main_map.eid_map:
            self.entity_control.redraw_entities_at_hex( hexID )
    def _redraw_roads(self):
        if self.path_control._path_key in self.main_map.path_catalog:
            for pID in self.main_map.path_catalog[self.path_control._path_key]:
                self.path_control.draw_path( pID )
    def _redraw_counties(self):
        if 'county' in self.main_map.rid_catalogue :
            for rid in self.main_map.rid_catalogue['county']:
                self.county_control.redraw_region( rid )

    def quit(self):
        """
        Exits MultiHex
        """
        sys.exit()

    def save_as(self):
        """
        Opens a dialog to accept a filename from the user, then calls the save_map function
        """
        self.file_name = QFileDialog.getSaveFileName(None, 'Save HexMap', './saves', 'HexMaps (*.hexmap)')
        self.save_map()

    def save_map(self):
        """
        Saves the map that is saved
        """
        if self.main_map is None:
            return
        else:
            save_map( self.main_map, self.file_name)
    
class new_load_dialog(QDialog):
    def __init__(self, parent):
        super(new_load_dialog, self).__init__(parent)
        self.ui = new_load_gui()
        self.ui.setupUi(self)

        self.ui.new_map_button.clicked.connect(self.button_new)
        self.ui.load_map_button.clicked.connect(self.button_load)
        self.ui.quit_button.clicked.connect(self.button_quit)
        self.parent = parent

    def button_new(self):
        """
        Tells the parent Window to try making a new map. This will launch the New Map Interface
        """
        self.parent.new()
        self.accept()

    def button_load(self):
        """
        This tells the parent window to load a map. Opens the open file dialog! 
        """
        self.parent.load()
        self.accept()

    def button_quit(self):
        sys.exit()

app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    # make sure the base saves folder exists 
    try:
        os.mkdir(os.path.join( os.path.dirname(__file__), "saves" ))
    except FileExistsError:
        pass
    app_instance.show()
    sys.exit(app.exec_())

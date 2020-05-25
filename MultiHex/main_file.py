from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QApplication, QWidget

import os
import sys 

# standard GUI
from MultiHex.guis.main_gui import main_gui

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import basic_tool
from MultiHex.map_types.overland import OEntity_Brush, OHex_Brush, Road_Brush, County_Brush, Nation_Brush, Nation, Biome_Brush, River_Brush, ol_clicker_control
from MultiHex.about_class import about_dialog
from MultiHex.load_new import new_load_dialog
from MultiHex.generator.util import get_tileset_params

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

        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.scene = ol_clicker_control( self.ui.graphicsView, self )
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        # start off with a nothing tool.
        # any mouse commands will just be thrown in the trash 
        self.scene._active = basic_tool(self)
        

        # set up the action bar! 
        """
        self.ui.actionQuit.triggered.connect( self.quit )
        self.ui.actionSave.triggered.connect( self.save_map )
        self.ui.actionSave_As.triggered.connect( self.save_as)
        self.ui.actionBiome_Borders.triggered.connect( self.action_biome_bord )
        self.ui.actionCounty_Borders.triggered.connect(self.action_county_bord )
        self.ui.actionBiome_Names.triggered.connect( self.action_biome_names )
        self.ui.actionCounty_Names.triggered.connect( self.action_county_names )
        self.ui.actionTowns.triggered.connect( self.action_towns )
        self.ui.actionLocations.triggered.connect( self.action_locations )
        self.ui.actionAbout_MultiHex.triggered.connect( self.actionAbout )
        """

    def show(self):
        QMainWindow.show(self)
        # this either has MH load a map or make a new map 
        self.main_map = None
        dialog = new_load_dialog(self)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    def new(self):
        pass

    def load(self):
        """
        Called when we want to load a new map
        """
        filename = QFileDialog.getOpenFileName(None, 'Open HexMap', os.path.join(os.path.dirname(__file__), "saves"), 'HexMaps (*.hexmap)')[0]
        self.ui.graphicsView.update()
        self.main_map = load_map( filename )
        self.file_name = filename 
        
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

    def save_map(self):
        """
        Saves the map that is saved
        """
        if self.main_map is None:
            return
        else:
            save_map( self.main_map, self.file_name)
    
    def actionAbout(self):
        """
        Pops open the about dialog
        """
        dialog = about_dialog( self )
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()

    def save_as(self):
        """
        Opens a dialog to accept a filename from the user, then calls the save_map function
        """
        self.file_name = QFileDialog.getSaveFileName(None, 'Save HexMap', './saves', 'HexMaps (*.hexmap)')
        self.save_map()

    def action_biome_names(self):
        """
        Toggles the drawing of biome names
        """
        state = self.ui.actionBiome_Names.isChecked()
        self.biome_control.draw_names = state
        self._redraw_biomes()

    def action_biome_bord(self):
        """
        Toggles the drawing of Biome borders
        """
        state = self.ui.actionBiome_Borders.isChecked()
        self.biome_control.draw_borders = state
        self._redraw_biomes()

    def action_county_bord(self):
        """
        Toggles the drawing of county borders
        """
        state = self.ui.actionCounty_Borders.isChecked()
        self.county_control.draw_borders = state
        self._redraw_counties()
        
    def action_county_names(self):
        """
        Toggles the drawing of county Names
        """
        state = self.ui.actionCounty_Names.isChecked()
        self.county_control.draw_names = state
        self._redraw_counties()

    def action_towns(self):
        """
        Toggles the drawing of settlements on the map
        """
        state = self.ui.actionTowns.isChecked()
        self.entity_control.draw_settlements = state
        self._redraw_entities()

    def action_locations(self):
        """
        Toggles the drawing of entities/locations on the map
        """
        state = self.ui.actionLocations.isChecked()
        self.entity_control.draw_entities = state
        self._redraw_entities()

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

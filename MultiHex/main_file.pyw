from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QApplication, QWidget

import os
import sys 
import json

# standard GUI
from MultiHex.guis.main_gui import main_gui

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import basic_tool, Map_Use_Tool
from MultiHex.objects import Icons
from MultiHex.map_types.overland import OEntity_Brush, OHex_Brush, Road_Brush, County_Brush, Nation_Brush, Nation, Biome_Brush, River_Brush, ol_clicker_control, Detail_Brush
from MultiHex.about_class import about_dialog
from MultiHex.generator.util import get_tileset_params, create_name, Climatizer

# import other guis! 
from MultiHex.guis.terrain_editor_gui import terrain_ui
from MultiHex.guis.civ_gui import civ_ui
from MultiHex.guis.new_load_gui import new_load_gui
from MultiHex.guis.map_use_gui import map_use_ui

#import some dialogs
from MultiHex.new_map import basicMapDialog

class main_window(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        # standard boiler-plate gui initialization
        # we instantiate the default GUI before anything else 
        self.ui = main_gui()
        self.ui.setupUi(self) 
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'Artwork','wiki_images','multihex_small_logo.svg')))

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
        self.map_use_control = Map_Use_Tool(self)

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
        self.ui.export_image.triggered.connect(self.export_image)
        self.ui.actionOpen.triggered.connect( self.open )
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionTerrainEditor.triggered.connect(self.switch_to_terrain)
        self.ui.actionCivEditor.triggered.connect(self.switch_to_civilization)
        self.ui.actionMapUse.triggered.connect(self.switch_to_map_use)

        self._ui_clear_function = None
        self.extra_ui = None

        loc = os.path.join(os.path.dirname(__file__),'resources', 'tilesets.json')
        file_object = open( loc, 'r')
        self.config = json.load( file_object )
        file_object.close()
        self.params = []

        self.icons = Icons()

        self.gen_params = []

        self.unsaved_changes = False

        # set up the save directory
        if sys.platform=='linux':
            basedir = os.path.join(os.path.expandvars('$HOME'),'.local','MultiHex')
        elif sys.platform=='darwin': #macOS
            basedir = os.path.join(os.path.expandvars('$HOME'),'MultiHex')
        elif sys.platform=='win32' or sys.platform=='cygwin': # Windows and/or cygwin. Not actually sure if this works on cygwin
            basedir = os.path.join(os.path.expandvars('%AppData%'),'MultiHex')
        else:
            raise NotImplementedError("{} is not a supported OS".format(sys.platform))
        if not os.path.exists(basedir):
            os.mkdir(basedir)
        self.savedir = os.path.join(basedir, 'saves')
        if not os.path.exists(self.savedir):
            os.mkdir(self.savedir)

    def export_image(self):
        """
        Function is called when the 'export image' action is chosen. Exports a PNG of the map at the location of the user's choice
        """
        temp= QFileDialog.getSaveFileName(None, 'Exoport Image', self.savedir, 'PNGs (*.png)')[0]
        if temp is None:
            return
        elif temp=='':
            return

        #self.main_map.dimensions
        size   = QtCore.QSize(self.main_map.dimensions[0], self.main_map.dimensions[1])
        image  = QtGui.QImage(size,QtGui.QImage.Format_ARGB32_Premultiplied)
        painter= QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(temp)

    def smart_ui_chooser(self):
        self.switch_to_terrain()

    def switch_to_terrain(self):
        self.scene.drop()
        if self._ui_clear_function is not None:
            self._ui_clear_function(self.ui)
        self.extra_ui = terrain_ui(self)
        self.ui.actionCivEditor.setChecked(False)
        self.ui.actionTerrainEditor.setChecked(True)
        self.ui.actionMapUse.setChecked(False)
        self._ui_clear_function = self.extra_ui.clear_ui

        self.county_control.draw_borders = False
        self.county_control.small_font = True
        self.biome_control.draw_borders=True 
        self.biome_control.small_font=False
        self._redraw_counties()
        self._redraw_biomes()

    def switch_to_civilization(self):
        self.scene.drop()
        if self._ui_clear_function is not None:
            self._ui_clear_function(self.ui)
        self.extra_ui = civ_ui(self)
        self.ui.actionCivEditor.setChecked(True)
        self.ui.actionTerrainEditor.setChecked(False)
        self.ui.actionMapUse.setChecked(False)
        self._ui_clear_function = self.extra_ui.clear_ui

        self.county_control.draw_borders = True
        self.county_control.small_font = False
        self.biome_control.draw_borders=False 
        self.biome_control.small_font=True
        self._redraw_counties()
        self._redraw_biomes()

    def switch_to_map_use(self):
        self.scene.drop()
        if self._ui_clear_function is not None:
            self._ui_clear_function(self.ui)
        self.extra_ui = map_use_ui(self)
        self.ui.actionCivEditor.setChecked(False)
        self.ui.actionTerrainEditor.setChecked(False)
        self.ui.actionMapUse.setChecked(True)
        self._ui_clear_function = self.extra_ui.clear_ui

        self.county_control.draw_borders = True
        self.county_control.small_font = False
        self.biome_control.draw_borders=False 
        self.biome_control.small_font=True
        self._redraw_counties()
        self._redraw_biomes()
        self.scene.select(self.map_use_control) # temporary until more buttons are here

    def show(self):
        QMainWindow.show(self)
        # this either has MH load a map or make a new map 
        self.main_map = None
        while self.main_map is None:
            dialog = new_load_dialog(self)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def new(self):
        """
        This is called in order to generate a new map
        """
        new_dialog = basicMapDialog(self)
        new_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        new_dialog.exec_()

        if self.gen_params==[]:
            return
        else:
            genBar = WorldGenLoadingBar(self, self.gen_params[0], self.gen_params[1])
            genBar.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            genBar.exec_()
            self.load(self.gen_params[1]) #load the new map!
            self.gen_params = []

    def _gen_finished(self):
        pass


    def open(self):
        pass

    def load(self, filename=None):
        """
        Called when we want to load a new map
        """
        if filename is None:
            self.filename = QFileDialog.getOpenFileName(None, 'Open HexMap', self.savedir, 'HexMaps (*.hexmap)')[0]
            if self.filename is None or self.filename=='':
                return
        else:
            self.filename=filename
        
        if not os.path.exists(self.filename): 
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
        for ID in self.main_map.catalog: 
            self.hex_control.redraw_hex( ID )
    def _redraw_biomes(self):
        if 'biome' in self.main_map.rid_catalog :
            for rid in self.main_map.rid_catalog['biome']:
                self.biome_control.redraw_region( rid )
    def _redraw_entities(self):
        for hexID in self.main_map.eid_map:
            self.entity_control.redraw_entities_at_hex( hexID )
    def _redraw_roads(self):
        if self.path_control._path_key in self.main_map.path_catalog:
            for pID in self.main_map.path_catalog[self.path_control._path_key]:
                self.path_control.draw_path( pID )
    def _redraw_counties(self):
        if 'county' in self.main_map.rid_catalog :
            for rid in self.main_map.rid_catalog['county']:
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
        temp= QFileDialog.getSaveFileName(None, 'Save HexMap', self.savedir, 'HexMaps (*.hexmap)')[0]
        print(temp)
        if temp is not None:
            if temp!='':
                self.filename=temp
                self.save_map()
                self.unsaved_changes = False

    def save_map(self):
        """
        Saves the map that is saved
        """
        if self.main_map is None:
            return
        else:
            save_map( self.main_map, self.filename)
            self.unsaved_changes = False
    
class LoadingBarGui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Loading")
        self.vbox = QtWidgets.QVBoxLayout(Dialog)
        self.progress = QtWidgets.QProgressBar(Dialog)
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        self.vbox.addWidget(self.progress)

class WorldGenLoadingBar(QDialog):
    def __init__(self,parent, gen_type, filename):
        QDialog.__init__(self,parent)
        # QtCore.Qt.WindowStaysOnTopHint
        self.ui=LoadingBarGui()
        self.ui.setupUi(self)
        self.parent = parent
        self.setWindowTitle("Generating Map...")

        self.gen_type = gen_type
        self.filename = filename

        self.threadpool = QtCore.QThreadPool()
        self.run()

    def run(self):
        worldGen = WorldGenerationThread(self.gen_type, self.filename)
        worldGen.signals.signal.connect(self.finished)
        self.threadpool.start(worldGen)

    def finished(self,other=None):
        self.close()

class Signaler(QtCore.QObject):
    signal = QtCore.pyqtSignal()

class WorldGenerationThread(QtCore.QRunnable):
    def __init__(self, gen_type, filename):
        super(WorldGenerationThread,self).__init__()
        self.gen_type = gen_type
        self.filename = filename
        self.setAutoDelete(True)

        self.signals = Signaler()

    @QtCore.pyqtSlot()
    def run(self):
        from MultiHex.generator.full_chain import full_sim
        self.test = full_sim(self.gen_type,self.filename)
        self.signals.signal.emit()


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
    app_instance.show()
    sys.exit(app.exec_())

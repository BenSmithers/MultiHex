## #!/usr/bin/python3.6m

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import clicker_control, QEntityItem
from MultiHex.map_types.overland import OHex_Brush, Biome_Brush, River_Brush, ol_clicker_control
from MultiHex.generator.util import get_tileset_params, create_name

# need these to define all the interfaces between the canvas and the user
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QDialog, QColorDialog

from MultiHex.guis.terrain_editor_gui import editor_gui_window
from MultiHex.about_class import about_dialog

import sys # basic command line interface 
import os  # basic file-checking, detecting os
import json # used to handle tileses 

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
        self.scene = ol_clicker_control( self.ui.graphicsView, self )
        # start with the hex as the currently used tool
        self.writer_control = OHex_Brush(self)
        self.region_control = Biome_Brush(self)
        self.river_writer = River_Brush(self)
        
        
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
        self.ui.tool_biome_sel.clicked.connect( self.tb_sel_biome )

        # Detailer toolbox connections
        self.ui.det_noise_combo.currentIndexChanged.connect( self.det_comboBox_select )
        self.ui.det_but_noise.clicked.connect( self.det_inject_button )
        self.ui.det_but_color.clicked.connect( self.det_color_button )
        self.ui.det_apply_button.clicked.connect( self.det_apply_button )

        # Hexbar toolbox connections
        self.ui.hex_type_combo.currentIndexChanged.connect( self.hex_comboBox_select )
        self.ui.hex_list_entry = QtGui.QStandardItemModel() 
        self.ui.hex_sub_list.setModel( self.ui.hex_list_entry )
        self.ui.hex_sub_list.clicked[QtCore.QModelIndex].connect( self.hex_subtype_clicked )
        self.ui.hex_brush_disp.valueChanged.connect( self.hex_brush_change )

        loc = os.path.join(os.path.dirname(__file__),'resources', 'tilesets.json')
        file_object = open( loc, 'r')
        self.config = json.load( file_object )
        file_object.close()
        self.params = []

        self.hex_fill_supertypes()


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
        self.ui.bio_color_combo.clicked.connect(self.biome_color_button)
        self.ui.biome_but_delete.clicked.connect( self.biome_delete )

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


    def _update_with_hex_id(self, id = None):
        if id is not None:
            if not isinstance(id, int):
                raise TypeError("Expected {}, got {}".format(int, type(id)))

            self.ui.hex_select_disp.setText(str(id))
            self.ui.det_hexid_disp.setText( str(id) )
            #.setText( str(id) )
        else:
            self.ui.hex_select_disp.setText("")
            self.ui.det_hexid_disp.setText( "")

    def det_show_selected(self, id = None):
        """
        Function called when a new hex is selected 
        """
        if id is not None:
            if not isinstance(id, int):
                raise TypeError("Expected {}, got {}".format(int, type(id)))

            self.ui.det_alt_slide.setValue( self.main_map.catalogue[id]._altitude_base*100 )
            self.ui.det_temp_slide.setValue( self.main_map.catalogue[id]._temperature_base*100)
            self.ui.det_rain_slide.setValue( self.main_map.catalogue[id]._rainfall_base*100)

        self._update_with_hex_id( id )




    def tb_hex_select(self):
        self.scene._active.drop()
        self.scene._active = self.writer_control
        self.writer_control.set_state(0)

        self.ui.toolBox.setCurrentIndex(0)

    def tb_detailer(self):
        self.scene._active.drop()

        self.ui.toolBox.setCurrentIndex(0)

    def tb_hex_brush(self):
        self.scene._active.drop()
        self.scene._active = self.writer_control
        self.writer_control.set_state(1)

        self.ui.toolBox.setCurrentIndex(1)

    def tb_new_river(self):
        self.scene._active.drop()
        self.ui.toolBox.setCurrentIndex(2)
        self.scene._active = self.river_writer

        self.river_writer.prepare(1)

    def tb_new_biome(self):
        self.scene._active.drop()
        self.ui.toolBox.setCurrentIndex(3)
        self.scene._active = self.region_control 
        self.region_control.set_state( 1 )

    def tb_sel_biome(self):
        self.ui.toolBox.setCurrentIndex(3)
        self.scene._active.drop()
        self.scene._active = self.region_control
        self.region_control.set_state( 0 )

    def det_comboBox_select(self):
        pass

    def det_inject_button(self):
        pass

    def det_color_button(self):
        pass

    def det_apply_button(self):
        # build the dictionary to adjut the hex
        params = {
                    "_altitude_base": self.ui.det_alt_slide.value()/100., 
                    "_rainfall_base": self.ui.det_rain_slide.value()/100.,
                    "_temperature_base": self.ui.det_temp_slide.value()/100.
            }
        self.writer_control( self.main_map.catalogue[self.writer_control.selected] , params )

    def hex_comboBox_select(self):
        """
        Called when you choose a new entry in the drop-down menu
        """
        self.ui.hex_list_entry.clear()
        this_sub = self.ui.hex_type_combo.currentText()

        for entry in self.config[self.main_map.tileset]["types"][this_sub]:
            this = QtGui.QStandardItem(entry)
            color =  self.config[self.main_map.tileset]["types"][this_sub][entry]["color"]
            this.setBackground( QtGui.QColor(color[0], color[1], color[2] ))
            self.ui.hex_list_entry.appendRow(this)


    def hex_subtype_clicked(self, index=None):
        """
        Called when you click on a subtype 
        """
        # get ready to draw
        self.tb_hex_brush()

        sub_type = index.data()
        this_type = self.ui.hex_type_combo.currentText()

        new_param = {}
        for key in self.params:
            new_param[key] = self.config[self.main_map.tileset]["types"][this_type][sub_type][key]
        
        self.writer_control.set_color(self.config[self.main_map.tileset]["types"][this_type][sub_type]["color"])
        self.writer_control.set_params( new_param )

    def hex_brush_change(self):
        """
        Called when the brush size changes. Tells the writer_control to switch to the new size
        """
        value = self.ui.hex_brush_disp.value()
        self.writer_control.set_brush_size( value )


    def hex_fill_supertypes(self):
        # hex_type_combo
        where = self.main_map.tileset
        for super_type in self.config[self.main_map.tileset]["types"]:
            self.ui.hex_type_combo.addItem(super_type)

        self.ui.hex_type_combo.setCurrentIndex(0)

    def river_list_click(self, index=None):
        # river_list_entry
        item = self.ui.river_list_entry.itemFromIndex(index)
        pID = item.eID

        if pID is not None:
            self.river_writer.select_pid(pID)


    def river_trib_click(self, index=None):
        item = self.ui.tributary_list_entry.itemFromIndex(index)

    def river_update_list(self):
        self.ui.river_list_entry.clear()

        if not ('rivers' in self.main_map.path_catalog):
            return
        for pID in self.main_map.path_catalog['rivers']:
            self.ui.river_list_entry.appendRow( QEntityItem("River {}".format(pID), pID))

    def river_ps(self):
        self.river_writer.pop_selected_start()

    def river_pe(self):
        self.river_writer.pop_selected_end()

    def river_as(self):
        self.river_writer.prepare( 4 )

    def river_ae(self):
        self.river_writer.prepare( 3)

    def river_delete(self):
        self.river_writer.delete_selected()
        self.river_update_list()

    def biome_name_gen(self):
        if self.region_control.selected_rid is None:
            return

        first = self.main_map.rid_catalogue[self.region_control.r_layer][self.region_control.selected_rid].ids[0]

        new_one = create_name( self.main_map.catalogue[first].biome )
        self.ui.bio_name_edit.setText( new_one )

    def biome_apply(self):
        if self.region_control.selected_rid is None:
            pass
        else:
            self.main_map.rid_catalogue[self.region_control.r_layer][self.region_control.selected_rid].name = self.ui.bio_name_edit.text()
            self.region_control.redraw_region_text( self.region_control.selected_rid)

    def biome_update_gui(self):
        if self.region_control.selected_rid is None:
            self.ui.bio_name_edit.setText("")
            self.ui.bio_color_combo.setEnabled(False)
        else:
            self.ui.bio_name_edit.setText(self.main_map.rid_catalogue[self.region_control.r_layer][self.region_control.selected_rid].name)
            self.ui.bio_color_combo.setEnabled(True)

    def biome_color_button(self):
        if self.region_control.selected_rid is None:
            pass
        else:
            old_one = self.main_map.rid_catalogue[self.region_control.r_layer][self.region_control.selected_rid].color
            qt_old_one = QtGui.QColor(old_one[0], old_one[1], old_one[2])
            new_color = QColorDialog.getColor(initial = qt_old_one, parent=self)

            if new_color.isValid():
                self.main_map.rid_catalogue[self.region_control.r_layer][self.region_control.selected_rid].color = (new_color.red(), new_color.green(), new_color.blue())
                self.region_control.redraw_region(self.region_control.selected_rid)
            else:
                print("pass")
    
    def biome_delete(self):
        if self.region_control.selected_rid is None:
            pass
        else:
            self.main_map.remove_region( self.region_control.selected_rid, self.region_control.r_layer)

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
        #self.writer_control.redraw_rivers()
        self.river_writer.redraw_rivers()
        print("done")
        self.river_update_list()

        self.params = get_tileset_params( self.main_map.tileset )
        


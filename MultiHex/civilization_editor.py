## #!/usr/bin/python3.6m

# civilization gui
from MultiHex.guis.civ_gui import editor_gui_window

# MultiHex objects
from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.map_types.overland import OHex_Brush
from MultiHex.tools import clicker_control, basic_tool, entity_brush, region_brush, QEntityItem

# need these to define all the interfaces between the canvas and the user
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QDialog

# ward dialog gui
from MultiHex.guis.ward_dialog import Ui_Dialog as ward_ui

import sys # basic command line interface 
import os  # basic file-checking, detecting os


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
        self.entity_control = entity_brush(self)
        self.writer_control = OHex_Brush(self)
        self.biome_control = region_brush(self, 'biome')

        self.scene._active = self.entity_control

        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        # drop-down menu buttons 
        self.ui.actionQuit.triggered.connect( self.go_away )
        self.ui.actionSave.triggered.connect( self.save_map )
        self.ui.actionSave_As.triggered.connect( self.save_as)
        
        #toolbar buttons
        self.ui.loc_button_1.clicked.connect( self.new_location_button_toolbar)
        self.ui.setl_button_2.clicked.connect( self.new_settlement_button_toolbar )
        self.ui.road_button_3.clicked.connect( self.new_road_button_toolbar )
        self.ui.count_button_4.clicked.connect( self.new_county_button_toolbar )

        # location tab buttons and things
        self.ui.loc_list_entry = QtGui.QStandardItemModel()
        self.ui.loc_list_view.setModel( self.ui.loc_list_entry )
        self.ui.loc_save.clicked.connect( self.loc_save_entity )
        self.ui.loc_delete.clicked.connect( self.loc_delete )
        self.ui.loc_deselect.clicked.connect( self.entity_control.deselect_hex )
        self.ui.loc_list_view.clicked[QtCore.QModelIndex].connect(self.loc_list_item_clicked)
        
        # settlement tab buttons and things
        self.ui.set_ward_dd.currentIndexChanged.connect( self.set_dropdown_activate )

        # page number can be accessed from
        # ui.toolBox.currentIndex() -> number
        # and set from
        # ui.toolBox.setCurrentIndex( number )

        self.file_name = ''
        self.main_map = Hexmap()
    
        self.ward_accept = False

    def set_dropdown_activate(self, index):
        print("Wow! Index {} of {}".format(index, self.ui.set_ward_dd.count()))

    def set_update_selection(self, eID=None):
        """
        Updates the settlement menu gui with the proper information about it
        """

        if eID is not None:
            assert( isinstance( eID , int ))
            if not isinstance( self.main_map.eid_catalogue[eID], Settlement):
                raise TypeError("Something terribly wrong has happened. Trying to update Entity {} as if it were {}, but it is {}".format(eID), Settlement, type( self.main_map.eid_catalogue[eID]) )

            self.ui.set_name_edit.setText( self.main_map.eid_catalogue[ eID ].name)
            self.ui.set_desc_edit.setText( self.main_map.eid_catalogue[ eID ].description )
    
    def set_ward_edit_button( self ):
        """
        brings up the ward buton
        """
        if self.entity_brush.selected is None:
            return
        if not isinstance( self.entity_brush.selected, Settlement):
            return
        self.ward_accept = False

        setting = self.ui.set_ward_dd.currentIndex()
        # 0 is whole city
        # 1 is city center
        # last is for a new ward
        if (setting+1)==self.ui.set_ward_dd.count():
            setting = -1
            new_ward = Settlement("New Ward", is_ward=True)
            dialog = ward_dialog( self, new_ward, setting )
        else:
            dialog = ward_dialog( self, self.main_map.eid_catalogue[ self.entity_brush.selected ], setting )
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()


    def set_update_ward_info(self, eID, ward = None):
        """
        For the settlement page. Updates the ward section in the GUI with the specified ward.
        """
        assert( isinstance( eID, int))
        assert( isinstance( ward, int))
        
        this_city = self.main_map.eid_catalogue[eID]

        if ward is None:
            self.ui.set_name_view.setText( this_city.name )
            self.ui.set_pop_disp.setText( this_city.population )
            self.ui.set_weal.disp.setText( this_city.wealth)


    def set_clear_ward_info(self):
        self.ui.set_name_view.setText("")
        self.ui.set_pop_disp.setText("")
        self.ui.set_weal.disp.setText("")
        self.ui.set_demo_view.setText("")




    def loc_update_name_text(self, eID):
        self.ui.loc_name_edit.setText( self.main_map.eid_catalogue[ eID ].name)
        self.ui.loc_desc_edit.setText( self.main_map.eid_catalogue[ eID ].description)

    def loc_update_selection(self, HexID=None):
        """
        Updates the location menu gui with the proper information for the specified Hex 
        """
        self.ui.status_label.setText("...")
        self.ui.loc_name_edit.setText( "" )
        self.ui.loc_desc_edit.setText( "" )

        # clear out the list no matter what
        self.ui.loc_list_entry.clear()
        if HexID is not None:
            # write out a list of all the entities at the selected Hex
            try:
                for eID in self.main_map.eid_map[ HexID ]:
                    self.ui.loc_list_entry.appendRow( QEntityItem(self.main_map.eid_catalogue[eID].name , eID))
            except KeyError:
                # there are no entities here
                pass


    def loc_delete(self):
        if self.entity_control.selected is not None:
            loc_id = self.main_map.eid_catalogue[ self.entity_control.selected ].location
            self.main_map.remove_entity( self.entity_control.selected )
            
            # this deletes the old drawing 
            try:
                self.entity_control.draw_entity( self.entity_control.selected )
            except ValueError:
                # this means that the entity was never drawn. That's okay. Just pass it...
                pass 

            # redraw the entities here in case we now have a more prominent thing to draw  
            self.entity_control.redraw_entities_at_hex( loc_id )
            self.entity_control.update_wrt_new_hex()
            self.ui.status_label.setText("deleted")
    
    def loc_save_entity(self):
        if self.entity_control.selected is not None:
            self.main_map.eid_catalogue[ self.entity_control.selected ].name = self.ui.loc_name_edit.text()
            self.main_map.eid_catalogue[ self.entity_control.selected ].description = self.ui.loc_desc_edit.toPlainText()
            self.entity_control.update_wrt_new_hex()
            self.ui.status_label.setText("saved")
        

    def loc_list_item_clicked( self , index):
        item = self.ui.loc_list_entry.itemFromIndex(index)
        
        # select the new entity and update the name/description
        self.entity_control.select_entity( item.eID )
        self.ui.loc_name_edit.setText( self.main_map.eid_catalogue[ item.eID ].name )
        self.ui.loc_desc_edit.setText( self.main_map.eid_catalogue[ item.eID ].description )


    def new_location_button_toolbar(self):
        self.ui.toolBox.setCurrentIndex( 0 )
        self.scene._active = self.entity_control 
        self.entity_control.prep_new(0)
    def new_settlement_button_toolbar(self):
        self.ui.toolBox.setCurrentIndex( 1 )
        self.scene._active = self.entity_control 
        self.entity_control.prep_new(1)
    def new_road_button_toolbar(self):
        self.ui.toolBox.setCurrentIndex( 2 )
    def new_county_button_toolbar(self):
        self.ui.toolBox.setCurrentIndex( 3 )
    

    def go_away(self):
        # show the main menu and disappear 
        self.parent().show()
        # need to clear the canvas too!
        self.hide()
        self.entity_control.clear()
        self.writer_control.clear()
        self.biome_control.clear()

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
        
        print("redrawing")
        for ID in self.main_map.catalogue: 
            self.writer_control.redraw_hex( ID )

        if 'biome' in self.main_map.rid_catalogue :
            for rid in self.main_map.rid_catalogue['biome']:
                self.biome_control.redraw_region( rid )
            
        self.writer_control.redraw_rivers()
        
        for hexID in self.main_map.eid_map:
            self.entity_control.redraw_entities_at_hex( hexID )

class ward_dialog(QDialog):
    def __init__(self,parent, which, setting):
        """
        which - which ward is being edited
        setting - specifies what exactly is being done. 
                     -1 add new ward
                     0 whole city
                     1 city center 
                   
        """
        ## TODO
        ## this part needs to be fixed so the 'whole city' and 'city center' parts actually only add to those specific parts


        super(ward_dialog, self).__init__(parent)
        self.ui = ward_ui()
        self.ui.setupUi(self)
        self.ui.accept_reject.accepted.connect( self.accept )
        self.ui.accept_reject.rejected.connect( self.reject )
        self.setting = setting

        if setting==0 or setting==-1:
            self.editing_ward = which
        else:            
            self.editing_ward = which.wards[ setting -2 ]

        if setting==1:
            self.ui.name_edit.setText( "City Center" )
            self.ui.pop_value.setText( str( self.editing_ward.partial_population ))
            self.ui.pop_edit.setText( str(self.editing_ward.partial_population ))
            self.ui.wealth_value.setText( str( self.editing_ward.partial_wealth ))
            self.ui.wealth_edit.setText(str( self.editing_ward.partial_wealth ))
        else:
            self.ui.name_edit.setText( self.editing_ward.name )
            self.ui.pop_value.setText( str( self.editing_ward.population ))
            self.ui.pop_edit.setText( str(self.editing_ward.population ))
            self.ui.wealth_value.setText( str( self.editing_ward.wealth ))
            self.ui.wealth_edit.setText(str( self.editing_ward.wealth ))

        #currentIndexChanged.conect
        self.ui.pop_dropdown.currentIndexChanged.connect( self.set_population )
        self.ui.wealth_dropdown.currentIndexChanged.connect( self.set_wealth )

        if setting==0:
            # restrict some parts that can't be edited for the whole
            self.ui.checkBox.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
            self.ui.demo_edit.setEnabled(False)

    def set_wealth(self, index):
        # writes the wealth after changing the dropdown menu
        if index==0 or index==1:
            if self.setting==1:
                self.ui.pop_edit.setText( str(self.editing_ward.partial_population) )
            else:
                self.ui.pop_edit.setText( str(self.editing_ward.population) )
        else:
            self.ui.pop_edit.setText( "0" )
            
    def set_poulation(self, index):
        # writes the population after changing the dropdown menu
        if index==0 or index==1:
            if self.setting==1:
                self.ui.wealth_edit.setText( str(self.editing_ward.partial_wealth ))
            else:
                self.ui.wealth_edit.setText( str( self.editing_ward.wealth ))
        else:
            self.ui.wealth_edit.setText("0")

    def accept(self):
        self.parent.accept = True
        which.name = self.ui.name_edit.text()
        #which.walled = walled_chck.state()  <-- not sure about this syntax
        
        if True: # should check the "allow to change" box!! 
            

        if self.ui.pop_dropdown.currentIndex()==0:
            pass
        elif self.ui.pop_dropdown.currentIndex()==1:
            # set to
            pass
        else:
            # add
            pass



        super( ward_dialog, self).accept()

    def reject(self):
        self.parent.accept = False
        super(ward_dialog, self).reject()

def parse_demographic( text ):
    """
    This parses the text in the demographic box. It ignores lines with a comment character: #. 
    
    It builds a dictionary assuming that the user prepares the data like 
        key : value
    and it ignores whitespace. If it fails, it raises a ValueError 
    """
    
    lines = []
    line = ""
    ignore = False
    for char in text:
        # at an end of line character we append what we have and start reading again
        if char == '\n':
            stripped = "".join( line.split(" ") )
            if stripped!="":
                lines.append( stripped )
                line = ""
            ignore = False
            continue

        # if we hit a comment character, ignore the rest of the line 
        if char =="#":
            ignore = True
            continue

        if ignore:
            continue

        line = line + char 
    
    # parse the lines intoa dictionary 
    new_dict = {}
    key = ""
    for line in lines:
        if line[0]=='+':
            # new key
            key = line[1:]
            if key not in new_dict:
                new_dict[key] = {}
            continue
        else:
            if key=="":
                raise ValueError("Bad Formatting.")

            split = line.split(":")
            if len(split)!=2:
                # this means there aren't the right number of ":" in the line
                raise ValueError("Bad formatting")
            # make it lower case to avoid case-sensitivity 
            subkey = split[0].lower()
            # will raise ValueError if this is not a number 
            value = float(split[1])

            new_dict[key][subkey]=value
    
    # normalize the built dictionary
    for key in new_dict:
        total = 0
        for subkey in new_dict:
            total += new_dict[key][subkey
        # divide each value by the sum of the values
        for subkey in new_dict:
            new_dict[key][subkey]/= float(total)

    return( new_dict )

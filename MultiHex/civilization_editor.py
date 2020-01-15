## #!/usr/bin/python3.6m

# civilization gui
from MultiHex.guis.civ_gui import editor_gui_window

# MultiHex objects
from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.tools import clicker_control, basic_tool, region_brush, QEntityItem, path_brush
from MultiHex.map_types.overland import Town, OEntity_Brush, OHex_Brush

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
        self.entity_control = OEntity_Brush(self)
        self.writer_control = OHex_Brush(self)
        self.path_control = path_brush(self, river_mode=False)
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
        self.ui.ent_select_button_0.clicked.connect(  self.entity_selector_toolbar)
        self.ui.count_sel_button_1.clicked.connect( self.county_selector_toolbar )
        self.ui.hand_button_2.clicked.connect( self.hand_button_toolbar )

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
        self.ui.set_button_apply.clicked.connect( self.set_button_apply )
        self.ui.set_edit_button.clicked.connect( self.set_ward_edit_button )

        # page number can be accessed from
        # ui.toolBox.currentIndex() -> number
        # and set from
        # ui.toolBox.setCurrentIndex( number )

        self.file_name = ''
        self.main_map = Hexmap()
    
        self.ward_accept = False


    def set_button_apply(self):

        which = self.entity_control.selected

        # skip this if nothing is selected
        if not isinstance(which, int):
            return

        # ensure that the selected eID is actually an entity
        if not isinstance( self.main_map.eid_catalogue[which], Town ):
            raise TypeError("A {} type object is selected instead of a town. How did this happen?".format(type(self.main_map.eid_catalogue[which])))

        # apply the changes
        self.main_map.eid_catalogue[which].name = self.ui.set_name_edit.text()
        self.main_map.eid_catalogue[which].description = self.ui.set_desc_edit.toPlainText()

    def set_dropdown_activate(self, index):
        """
        Called when an entry is selected in the drop down menu in the settlement tab
         0 - city as a whole
         1 - city center
         ... - wards
         -1 - new ward
        """
        which = self.entity_control.selected
        if not isinstance( which, int):
            return #none is selec ted
        if not isinstance( self.main_map.eid_catalogue[which], Town ):
            raise TypeError("A {} type object is selected instead of a town. How did this happen?".format(type(self.main_map.eid_catalogue[which])))

        if index==(self.ui.set_ward_dd.count() - 1):
            # add new ward
            pass
        elif index==0:
            # all city
            self.set_update_ward_info( which )
        else:
            # take the index, subtract 1. This gives the ward number! 
            self.set_update_ward_info( which, index - 1)

    def set_update_selection(self, eID=None):
        """
        Updates the settlement menu gui with the proper information about it
        """
        # set dropdown menu to default setup 
        while self.ui.set_ward_dd.count()>3:
            self.ui.set_ward_dd.removeItem( self.ui.set_ward_dd.count() -2 )

        if eID is not None:
            assert( isinstance( eID , int ))
            if not isinstance( self.main_map.eid_catalogue[eID], Town):
                raise TypeError("Something terribly wrong has happened. Trying to update Entity {} as if it were {}, but it is {}".format(eID, Town, type( self.main_map.eid_catalogue[eID]) ))

            self.ui.set_name_edit.setText( self.main_map.eid_catalogue[ eID ].name)
            self.ui.set_desc_edit.setText( self.main_map.eid_catalogue[ eID ].description )

            self.ui.set_ward_dd.setCurrentIndex(0)
            self.set_update_ward_info(eID)

            for ward in self.main_map.eid_catalogue[eID].wards:
                self.ui.set_ward_dd.insertItem(self.ui.set_ward_dd.count()-1, ward.name)

        else:
            # eID is None-type. So let's clear 
            self.ui.set_name_edit.setText( "" )
            self.ui.set_desc_edit.setText( "" )
            self.set_clear_ward_info()
            pass
    
    def set_ward_edit_button( self ):
        """
        Called when the 'ward edit' button is clicked 
        """
        if self.entity_control.selected is None:
            print("nothing selected")
            return
        if not isinstance( self.main_map.eid_catalogue[self.entity_control.selected], Town):
            print("got entity type {}, expected {}".format(type(self.main_map.eid_catalogue[self.entity_control.selected]), Town) )
            return
        self.ward_accept = False

        setting = self.ui.set_ward_dd.currentIndex()
        # 0 is whole city
        # 1 is city center
        # last is for a new ward
        if (setting+1)==self.ui.set_ward_dd.count():
            setting = -1
            new_ward = Town("New Ward", is_ward=True)
            dialog = ward_dialog( self, new_ward, setting )
        else:
            dialog = ward_dialog( self, self.main_map.eid_catalogue[ self.entity_control.selected ], setting )
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()

        if setting==-1 and (new_ward is not None):
            self.main_map.eid_catalogue[self.entity_control.selected].add_ward( new_ward )

        #update! 
        self.set_update_selection( self.entity_control.selected )

        # redraw the hex ( the icon may have changed )
        self.entity_control.redraw_entities_at_hex( self.entity_control.selected_hex ) 

    def set_update_ward_info(self, eID, ward = None):
        """
        For the settlement page. Updates the ward section in the GUI with the specified ward.
        """
        assert( isinstance( eID, int))
        
        this_city = self.main_map.eid_catalogue[eID]

        # if no ward is specified, update the ward info with the town's overall values 
        if ward is None:
            self.ui.set_name_view.setText( this_city.name )
            self.ui.set_pop_disp.setText( str(this_city.population))
            self.ui.set_weal_disp.setText( str(this_city.wealth) )
            self.ui.set_demo_view.setPlainText("A City")
        else:
            assert( isinstance( ward, int))
            # 0 - city center
            # > 0 - some ward...
            if ward==0:
                self.ui.set_name_view.setText( "City Center")
                self.ui.set_pop_disp.setText( str(this_city.partial_population ))
                self.ui.set_weal_disp.setText( str(this_city.partial_wealth))
                self.ui.set_demo_view.setPlainText( this_city.get_demographics_as_str() )
            else:
                self.ui.set_name_view.setText( this_city.wards[ward-1].name )
                self.ui.set_pop_disp.setText( str(this_city.wards[ward-1].population ))
                self.ui.set_weal_disp.setText( str(this_city.wards[ward-1].wealth))
                self.ui.set_demo_view.setPlainText( this_city.wards[ward-1].get_demographics_as_str() )



    def set_clear_ward_info(self):
        self.ui.set_name_view.setText("")
        self.ui.set_pop_disp.setText("")
        self.ui.set_weal_disp.setText("")
        self.ui.set_demo_view.setText("")




    def loc_update_name_text(self, eID):
        """
        Should be called when a new location is selected. Writes the name and description
        """
        self.ui.loc_name_edit.setText( self.main_map.eid_catalogue[ eID ].name)
        self.ui.loc_desc_edit.setText( self.main_map.eid_catalogue[ eID ].description)

    def loc_update_selection(self, HexID=None):
        """
        Updates the location menu gui with the proper information for the specified Hex. Adds the list of entities there
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
        """
        Called when the delete button is pressed in the locations tab
        """
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
        if isinstance( self.main_map.eid_catalogue[ item.eID ], Town):
            self.ui.toolBox.setCurrentIndex( 1 )
            self.set_update_selection( item.eID )
        else:
            self.ui.loc_name_edit.setText( self.main_map.eid_catalogue[ item.eID ].name )
            self.ui.loc_desc_edit.setText( self.main_map.eid_catalogue[ item.eID ].description )


    def new_location_button_toolbar(self):
        """
        Called by a GUI button. Drops any active tool, swaps to the entity control, changes to the proper toolBox page, and prepares to create a new Location
        """
        self.scene._active.drop()
        self.ui.toolBox.setCurrentIndex( 0 )
        self.scene._active = self.entity_control 
        self.entity_control.prep_new(0)
    def new_settlement_button_toolbar(self):
        """
        Called by a GUI button. Drops any active tool, swaps to the entity control, changes to the Settlement page, and prepares to create a new town. 
        """
        self.scene._active.drop()
        self.ui.toolBox.setCurrentIndex( 1 )
        self.scene._active = self.entity_control 
        self.entity_control.prep_new(1)
    def new_road_button_toolbar(self):
        self.ui.toolBox.setCurrentIndex( 2 )
        self.scene._active.drop()
        self.scene._active = self.path_control
        self.path_control.prepare(1)

    def new_county_button_toolbar(self):
        self.ui.toolBox.setCurrentIndex( 3 )
    
    def entity_selector_toolbar(self):
        """
        Ensures that the entity brush is active. Drops whatever brush used to be selected and selects this one! 
        """

        self.ui.toolBox.setCurrentIndex( 0 )
        self.scene._active.drop()
        self.scene._active = self.entity_control

    def county_selector_toolbar(self):
        print("county sel click")
    def hand_button_toolbar(self):
        print("hand click")

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
                     -1 the new town-like object 
                     0 whole city
                     1 city center 
                     higher numbers for wards
                   
        """

        #for some reason, the accept function is called twice.... 
        self._done = False

        super(ward_dialog, self).__init__(parent)
        self.ui = ward_ui()
        self.ui.setupUi(self)
        self.ui.accept_reject.accepted.connect( self.accept )
        self.ui.accept_reject.rejected.connect( self.reject )
        self.setting = setting

        if setting==0 or setting==-1 or setting==1:
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

        self.ui.walled_chck.setChecked( self.editing_ward.walled ) 
        self.ui.order_slider.setValue(100*self.editing_ward.order)
        self.ui.spirit_slider.setValue(100*self.editing_ward.spirit)
        self.ui.war_slider.setValue(100*self.editing_ward.war)

        #currentIndexChanged.conect
        self.ui.pop_dropdown.currentIndexChanged.connect( self.set_population )
        self.ui.wealth_dropdown.currentIndexChanged.connect( self.set_wealth )
        # 2 - order; 3 - war; 4 - spirit

        if setting==0:
            # restrict some parts that can't be edited for the whole
            #self.ui.checkBox.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
            self.ui.demo_edit.setEnabled(False)
            self.ui.order_slider.setEnabled(False)
            self.ui.war_slider.setEnabled(False)
            self.ui.spirit_slider.setEnabled(False)
            self.ui.walled_chck.setEnabled(False)
        else:
            # set the things
            new_text = "# Use \"+\" to start a new category\n# And write entries as \"<type>:<value>\"\n #Categories will be auto-normalized\n\n"+ self.editing_ward.get_demographics_as_str()
            self.ui.demo_edit.setPlainText(new_text)

        self.ui.wealth_edit.setEnabled(False)
        self.ui.pop_edit.setEnabled(False)


    def set_wealth(self, index):
        # writes the wealth after changing the dropdown menu
        #  0 is keep at, 1 is set to, 2 is add to
        if index==0:
            self.ui.wealth_edit.setText("")
            self.ui.wealth_edit.setEnabled(False)
        elif index==1:
            self.ui.wealth_edit.setEnabled(True)
            if self.setting==1:
                self.ui.wealth_edit.setText( str(self.editing_ward.partial_wealth) )
            else:
                self.ui.wealth_edit.setText( str(self.editing_ward.wealth) )
        else:
            self.ui.wealth_edit.setEnabled(True)
            self.ui.wealth_edit.setText( "0" )
            
    def set_population(self, index):
        # writes the population after changing the dropdown menu
        #  0 is keep at, 1 is set to, 2 is add to
        if index==0:
            self.ui.pop_edit.setText("")
            self.ui.pop_edit.setEnabled(False)
        elif index==1:
            self.ui.pop_edit.setEnabled(True)
            if self.setting==1:
                self.ui.pop_edit.setText( str(self.editing_ward.partial_population ))
            else:
                self.ui.pop_edit.setText( str( self.editing_ward.population ))
        else:
            self.ui.pop_edit.setEnabled(True)
            self.ui.pop_edit.setText("0")

    def accept(self):
        """
        Called when the 'okay' option is selected. For some reason it gets called twice though... 
        """

        if self._done:
            return
        else:
            self._done = True

        #which.walled = walled_chck.state()  <-- not sure about this syntax
        self.editing_ward.walled = self.ui.walled_chck.isChecked()
        if not self.setting==1:
            self.editing_ward.name = self.ui.name_edit.text()
       
        if self.setting!=0:
            self.editing_ward.set_war( self.ui.war_slider.value()/100. )
            self.editing_ward.set_order( self.ui.order_slider.value()/100. )
            self.editing_ward.set_spirit( self.ui.spirit_slider.value()/100. )


        if self.setting==0: 
            passed_demo = None
        else:
            try:
                if self.ui.demo_edit.toPlainText()=="":
                    passed_demo = None
                else:
                    self.ui.demo_edit.update()
                    passed_demo = parse_demographic( self.ui.demo_edit.toPlainText() )
            except ValueError:
                print("Error parsing demographic text block")
                self.reject()

        if self.setting==0:
            which_ward = None
        elif self.setting ==  -1:
            which_ward = None
        else:
            which_ward = self.setting - 1

        # how to change the population
        if self.ui.pop_dropdown.currentIndex() == 0: # keep 
            pass
        elif self.ui.pop_dropdown.currentIndex() == 1:
            self.editing_ward.set_population(int( self.ui.pop_edit.text() ), which_ward = which_ward)
        else:
            self.editing_ward.add_population(int( self.ui.pop_edit.text() ), which_ward = which_ward, demographics=passed_demo)
        
        if self.ui.wealth_dropdown.currentIndex() == 0:
            pass
        elif self.ui.wealth_dropdown.currentIndex() == 1:
            self.editing_ward.set_wealth( int( self.ui.wealth_edit.text()), which_ward = which_ward)
        else: 
            self.editing_ward.add_wealth( int( self.ui.wealth_edit.text()), which_ward = which_ward)

        if (self.ui.comboBox.currentIndex()==0) and (passed_demo is not None):
            self.editing_ward.set_demographics( passed_demo )

        self.editing_ward.update_icon()
        super( ward_dialog, self).accept()

    def reject(self):
        if self.setting==-1:
            which = None
        super(ward_dialog, self).reject()

def parse_demographic( text ):
    """
    This parses the text in the demographic box. It ignores lines with a comment character: #. 
    
    It builds a dictionary assuming that the user prepares the data like 
        key : value
    and it ignores whitespace. If it fails, it raises a ValueError 
    """

    # add an EOL character at the end
    text = text + '\n'

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
        for subkey in new_dict[key]:
            total += new_dict[key][subkey]
        # divide each value by the sum of the values
        for subkey in new_dict[key]:
            new_dict[key][subkey]/= float(total)

    return( new_dict )
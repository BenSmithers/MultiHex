from MultiHex.guis.advanced_map_generation import advanced_map_dialog
from MultiHex.guis.basic_map_generation import basic_map_dialog
from MultiHex.generator.full_chain import full_sim

import os
import json #open the configuration stuff

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

"""
This file defines the classes for the two dialogs used in map generation
"""

class basicMapDialog(QDialog):
    def __init__(self,parent=None,default_name="generated.hexmap"):
        QDialog.__init__(self,parent)
        self.ui=basic_map_dialog()
        self.ui.setupUi(self)
        self.parent=parent

        # connects the buttons
        self.ui.cancel_button.clicked.connect(self.button_quit)
        self.ui.generate_button.clicked.connect(self.button_generate)
        self.ui.advanced_gen_button.clicked.connect(self.button_advanced)

        # sets the default filename
        self.ui.fileNameEntry.setText(os.path.join(os.path.dirname(__file__), "saves", default_name))

        self.ui.map_type_combo.currentIndexChanged.connect(self.new_map_type)

        self.tileset_loc = os.path.join(os.path.dirname(__file__), "resources", "tilesets.json")
        self.config_loc = os.path.join(os.path.dirname(__file__),"generator","config.json")

        self.new_map_type()

    def button_advanced(self):
        """
        Calls when the user selects the advanced generation button. Opens the advanced generation dialog window. 
        """
        adv_dialog = advancedMapDialog(self)
        adv_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        adv_dialog.exec_()

    def button_generate(self, custom=False):
        """
        Calls when the generate button is clicked. Starts the generation process.
        """
        if custom:
            full_sim('custom', self.ui.fileNameEntry.text())
        else:
            full_sim(self.ui.gen_preset_combo.currentText(), self.ui.fileNameEntry.text())

    def button_quit(self):
        """
        Called when the user decides against creating a new map
        """
        self.close()

    def choose_filename(self):
        """
        Called when the user wants to choose a new map type
        """
        pass

    def new_map_type(self):
        """
        Called when the user choose a new map type
        """
        
        # Update the list of tilesets
        f = open(self.tileset_loc, 'r')
        data = json.load(f)
        f.close()

        self.ui.tileset_combo.clear()
        for key in data:
            if str(key)=="custom":
                continue
            nice = str(key).lower()
            nice = nice[0].upper() + nice[1:]
            self.ui.tileset_combo.addItem(nice)
        data = None

        # update the list of map generation presets
        f = open(self.config_loc,'r')
        data = json.load(f)
        f.close()
        
        self.ui.gen_preset_combo.clear()
        for key in data:
            nice = str(key).lower()
            nice = nice[0].upper() + nice[1:]
            self.ui.gen_preset_combo.addItem(nice)



class advancedMapDialog(QDialog):
    def __init__(self,parent=None,baseline="continental"):
        QDialog.__init__(self,parent)
        self.ui=advanced_map_dialog()
        self.ui.setupUi(self)
        self.parent=parent
        self.baseline = baseline

        # load it in!
        self.config_loc = os.path.join(os.path.dirname(__file__),"generator","config.json")
        f = open(self.config_loc,'r')
        self.config = json.load(f)
        f.close()

        self.custom_key = "custom"
        self.load_baseline_into_custom()

        self.ui.param_combo.clear()

        self.added_items = {}
        self.row_number = 0

        if baseline not in self.config:
            self.close()
        

        for key in self.config[baseline]:
            nice = str(key).lower()
            nice = nice[0].upper() + nice[1:]
            self.ui.param_combo.addItem(nice)
        
        self.ui.pushButton.clicked.connect(self.continue_button)
        self.ui.param_combo.currentIndexChanged.connect(self.new_dropdown_selected)
        self.new_dropdown_selected()

    def load_baseline_into_custom(self):
        """
        Copies whatever the basline is into the custom key in the generation 'config' json file
        """
        self.config[self.custom_key] = self.config[self.baseline]

    def write_config_file(self):
        """
        This dumps the current configuration into the generation config file
        """
        f = open(self.config_loc,'w')
        json.dump(self.config,f,ensure_ascii=True,indent=2)
        f.close()

    def new_dropdown_selected(self):
        get_key = self.ui.param_combo.currentText().lower()
        # now we add some buttons

        for key in self.added_items:
            self.ui.formLayout.removeWidget( self.added_items[key] )
            self.added_items[key].deleteLater()
        self.added_items = {}

        self.row_number = 0
        for key in self.config[self.custom_key][get_key]["values"]:
            self.add_entry(key, isinstance(self.config[self.custom_key][get_key]["values"][key], int))

        if self.ui.param_combo.currentIndex() == (self.ui.param_combo.count()-1):
            self.ui.pushButton.setText("Generate")
        else:
            self.ui.pushButton.setText("Save and Continue")

    def add_entry(self, key, type_int):
        name = str(key).lower()
        name = name[0].upper() + name[1:]
        subkey = self.ui.param_combo.currentText().lower()
        
        # add in the label
        self.added_items[name+"l"] = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        self.added_items[name+"l"].setObjectName(name)
        self.added_items[name+"l"].setText(name)
        self.ui.formLayout.setWidget(self.row_number, QtWidgets.QFormLayout.LabelRole, self.added_items[name+"l"])

        # add the value
        if type_int:
            self.added_items[name] = QtWidgets.QSpinBox(self.ui.scrollAreaWidgetContents)
            self.added_items[name].setMaximum(8000)
            self.added_items[name].setMinimum(0)
            self.added_items[name].setValue(self.config[self.custom_key][subkey]["values"][key])
        else:
            self.added_items[name] = QtWidgets.QDoubleSpinBox(self.ui.scrollAreaWidgetContents)
            self.added_items[name].setDecimals(3)
            self.added_items[name].setSingleStep(0.01)
            self.added_items[name].setMinimum(0)
            self.added_items[name].setValue(self.config[self.custom_key][subkey]["values"][key])
        self.added_items[name].setObjectName(name+"spin")
        
        self.ui.formLayout.setWidget(self.row_number, QtWidgets.QFormLayout.FieldRole, self.added_items[name])

        self.row_number+=1

        # add the description 
        self.added_items[name+"2"] = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        self.added_items[name+"2"].setObjectName(name+"... desc")
        self.added_items[name+"2"].setText(self.config[self.custom_key][subkey]["desc"][key])
        self.ui.formLayout.setWidget(self.row_number, QtWidgets.QFormLayout.FieldRole, self.added_items[name+"2"])

        self.row_number+=1

    def continue_button(self):
        if self.ui.param_combo.currentIndex() == (self.ui.param_combo.count()-1):
            self.write_config_file()
            self.parent.button_generate(True)
            self.close()
        else:
            # update the config stuff
            subkey = self.ui.param_combo.currentText().lower()
            for key in self.config[self.custom_key][subkey]["values"]:
                name = str(key).lower()
                name = name[0].upper() + name[1:]
                self.config[self.custom_key][subkey]["values"][key] = self.added_items[name].value()

            self.ui.param_combo.setCurrentIndex(self.ui.param_combo.currentIndex()+1)

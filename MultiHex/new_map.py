from MultiHex.guis.advanced_map_generation import advanced_map_dialog
from MultiHex.guis.basic_map_generation import basic_map_dialog

import os
import json #open the configuration stuff

from PyQt5 import QtCore
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

    def button_generate(self):
        """
        Calls when the generate button is clicked. Starts the generation process.
        """
        pass

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
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.ui=advanced_map_dialog()
        self.ui.setupUi(self)

    def add_new_
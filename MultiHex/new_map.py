from MultiHex.guis.advanced_map_generation import advanced_map_dialog, new_preset_dialog
from MultiHex.guis.basic_map_generation import basic_map_dialog
from MultiHex.guis.new_load_gui import new_load_gui


from logger import Logger

import sys
import os
import json #open the configuration stuff
import copy

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

"""
This file defines the classes for the two dialogs used in map generation. 
"""


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
    """
    This here is the main menu. We have three buttons: Load Map, New Map, and Quit

    Should probably add an "About" button
    #TODO set up a way to customize tilesets, 
    """
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

class basicMapDialog(QDialog):
    """
    The basic map dialog allows us the user to choose a "map type", a "generation type", and a "generation preset"
        map type - overall type of map we're making. Like, an overland map, a city map, a space map, etc
        generation type - which generation algorithm we use (specific to map types)
        generation preset - which arrangement of settings to send to the generator (specific to generation type)
    """
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
        self.ui.fileNameEntry.setText(os.path.join(parent.savedir, default_name))

        self.ui.map_type_combo.currentIndexChanged.connect(self.new_map_type)

        self.tileset_loc = os.path.join(os.path.dirname(__file__), "resources", "tilesets.json")
        self.config_loc = os.path.join(os.path.dirname(__file__),"generator","config.json")

        self.new_map_type()

    def button_advanced(self):
        """
        Calls when the user selects the advanced generation button. Opens the advanced generation dialog window. 
        """
        # use the appropriate 
        adv_dialog = advancedMapDialog(self, baseline=self.ui.gen_preset_combo.currentText().lower())
        adv_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        adv_dialog.exec_()

    def button_generate(self, custom=False):
        """
        Calls when the generate button is clicked. Starts the generation process
        """
        # we check if we're using a custom (advanced) generation set
        arg = 'custom' if custom else self.ui.gen_preset_combo.currentText().lower()
        self.parent.gen_params = [arg.lower(), self.ui.fileNameEntry.text()]
        self.close()

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
            if str(key).lower()=="custom":
                continue
            nice = str(key).lower()
            nice = nice[0].upper() + nice[1:]
            self.ui.gen_preset_combo.addItem(nice)



class advancedMapDialog(QDialog):
    """
    Here, the user has specified they want to configure a preset with more detail

    So we copy the preset over into a "custom" category, and edit that one directly 
    We go tab by tab configuring groups of presets - these groups are used individually by different steps in the generation procedure
    """
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

        self.new_preset = ''
        self.new_preset_button = None

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
        # if we don't use the copy thing then we just edit the baseline parameters too :grimace: 
        self.config[self.custom_key] = copy.deepcopy(self.config[self.baseline])

    def write_config_file(self,new_name=None):
        """
        This dumps the current configuration into the generation config file
        """
        f = open(self.config_loc,'w')
        if new_name is not None:
            if not isinstance(new_name,str):
                raise TypeError("New config name must be {}, got {}".format(str, type(new_name)))
            self.config[new_name] = self.config[self.custom_key]
        json.dump(self.config,f,ensure_ascii=True,indent=2)
        f.close()

    def new_dropdown_selected(self):
        get_key = self.ui.param_combo.currentText().lower()
        # now we add some buttons

        for key in self.added_items:
            self.ui.formLayout.removeWidget( self.added_items[key] )
            self.added_items[key].deleteLater()
        self.added_items = {}

        if self.new_preset_button is not None:
            self.ui.horizontalLayout.removeWidget(self.new_preset_button)
            self.new_preset_button.deleteLater()
            self.new_preset_button=None

        self.row_number = 0
        for key in self.config[self.custom_key][get_key]["values"]:
            self.add_entry(key, isinstance(self.config[self.custom_key][get_key]["values"][key], int))

        if self.ui.param_combo.currentIndex() == (self.ui.param_combo.count()-1):
            self.new_preset_button = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
            self.new_preset_button.setObjectName("new_preset_button")
            self.new_preset_button.setText("Save As New Preset")
            self.ui.horizontalLayout.insertWidget(0,self.new_preset_button)
            self.new_preset_button.clicked.connect(self.save_config)

            self.ui.pushButton.setText("Generate")
        else:
            
            self.ui.pushButton.setText("Save and Continue")

    def save_config(self):
        config_dialog = newPresetDialog(self)
        config_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        config_dialog.exec_()

    def add_entry(self, key, type_int):
        """
        For this group of entries we add a bunch of spinboxes to edit each parameter needed by the configuration thingy 
        """
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
        """
        Load up the next group or generate. If the later, write the config file (which has the curtom tab) and run the generator. 
        If the later, we add in all the spin boxes
        """
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


class newPresetDialog(QDialog):
    def __init__(self,parent):
        QDialog.__init__(self,parent)
        self.ui=new_preset_dialog()
        self.ui.setupUi(self)
        self.parent=parent

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def accept(self):
        print("accept")
        new_preset_name = str(self.ui.line.text()) 
        forbid = ["continental", "islands", "custom"]
        if new_preset_name in forbid:
            # TODO show a dialog warning that this is invalid 
            Logger.Warn("Invalid name for preset")
        self.parent.write_config_file(new_preset_name)
        QDialog.accept(self)

    def reject(self):
        print("reject")
        QDialog.reject(self)

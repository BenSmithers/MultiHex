#!/usr/bin/python3.6

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QApplication, QWidget

from MultiHex.guis.main_menu import Ui_MainWindow as main_menu
from MultiHex.terrain_editor import editor_gui
from MultiHex.civilization_editor import editor_gui as civ_gui
from MultiHex.guis.new_map_dialogue import Ui_Dialog as nmd

from MultiHex.ridge_editor import ridge_gui
from MultiHex import generator

import os
import sys
import time


# open the gui
class main_gui(QMainWindow):
    """"
    Main Menu Gui creator! 
    """
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = main_menu()
        self.ui.setupUi(self)

        # it always has these two editors (and soon more!) loaded and ready to go.
        # because of that it's important that these two clean themselves up when told to hide 
        self.editor_ui = editor_gui(self)
        self.ridge_ui  = ridge_gui(self)
        self.civ_ui    = civ_gui(self)

        # connecting buttons 
        self.ui.pushButton_2.clicked.connect( QtCore.QCoreApplication.instance().quit )
        self.ui.pushButton.clicked.connect( self.load_int )
        self.ui.pushButton_3.clicked.connect( self.new )
        self.ui.pushButton_4.clicked.connect( self.editor )
        self.ui.civEdit.clicked.connect(self.civ_edit)
        #self.ui.civEdit.setEnabled(False)
        self.ui.pushButton.setEnabled(False)

        self.new_name   = os.path.join(os.path.dirname(__file__), "saves", "generated.hexmap")
        self.setting    = -1

    def load_int(self, filename=''):
        """
        This will be the stepping off point for interfacing with the map in an interactive way. Hence the 'ing' suffix 
        """
        if filename=='':
            filename = QFileDialog.getOpenFileName(None, 'Open HexMap', os.path.join(os.path.dirname(__file__), "saves"), 'HexMaps (*.hexmap)')[0]

        if filename=='':
            return()
        else:
            print("Loading {}".format(filename))
            print("The main program hasn't been implemented yet")
    def civ_edit(self):
        """
        Will be a stepping off point for editing and viewing the civilizations in the world. 
        """
        filename = QFileDialog.getOpenFileName( None, 'Edit Regions', os.path.join(os.path.dirname(__file__), "saves"), 'HexMaps (*.hexmap)')[0]
        if filename!='':
            self.hide()
            print("Loading {}".format(filename))
        else:
            return()
        self.civ_ui.prep_map(filename)
        self.civ_ui.show()

    def editor(self):
        """
        Opens the world editor 
        """
        filename = QFileDialog.getOpenFileName(None, 'Edit HexMap', os.path.join(os.path.dirname(__file__), "saves"), 'HexMaps (*.hexmap)')[0]

        if filename!='':
            self.hide()        
            print("Loading {}".format(filename))
        else:
            return()
        self.editor_ui.prep_map(filename)
        self.editor_ui.show()

    def new(self):
        """
        Brings up the "new map" dialog
        """
        dialog = mod_accept(self)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()
        if self.setting<0: # indicates a cancel response. Do nothing 
            pass
        else:
            if self.setting==0:
                print("new blank map of name {}".format(self.new_name))
            elif self.setting==1:
                print("Opening ridge maker, name {}".format(self.new_name))
                print(type(self.new_name))
                self.ridge_ui.save_name = self.new_name
                self.hide()
                self.ridge_ui.show()
            else:
                print("Generating from scratch, name {}".format(self.new_name))
                self.hide()
                generator.full_chain.full_sim('cont', self.new_name )
                self.show()

class mod_accept(QDialog):
    """
    This defines the way the new map dialog interfaces with the main menu
    """
    def __init__(self, parent=None):
        super(mod_accept, self).__init__(parent)
        self.ui=nmd()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
    
        self.ui.blank.clicked.connect(self.blank_map)
        self.ui.ridgeline.clicked.connect(self.from_ridge)
        self.ui.full.clicked.connect(self.full_gen)

    def accept(self):
        self.parent().new_name = os.path.join(os.path.dirname(__file__),"saves", self.ui.lineEdit.text())
        super(mod_accept, self).accept()
    def reject(self):
        self.parent().setting = -1
        super(mod_accept, self).reject()

    def blank_map(self):
        self.parent().setting = 0
    def from_ridge(self):
        self.parent().setting = 1
    def full_gen(self):
        self.parent().setting = 2


app = QApplication(sys.argv)
app_instance = main_gui()


# quit button
if __name__=="__main__":
    # make sure the base saves folder exists 
    try:
        os.mkdir(os.path.join( os.path.dirname(__file__), "saves" ))
    except FileExistsError:
        pass
    app_instance.show()
    sys.exit(app.exec_())


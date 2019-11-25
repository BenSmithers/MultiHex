#!/usr/bin/python3.6
from PyQt4 import QtCore, QtGui
from MultiHex.guis.main_menu import Ui_MainWindow as main_menu
from MultiHex.map_paint import editor_gui
from MultiHex.guis.new_map_dialogue import Ui_Dialog as nmd
from MultiHex.ridge_editor import ridge_gui
from MultiHex.generator import full_chain

import sys
import time

# open the gui
class main_gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = main_menu()
        self.ui.setupUi(self)

        self.editor_ui = editor_gui(self)
        self.ridge_ui  = ridge_gui(self)

        self.ui.pushButton_2.clicked.connect( QtCore.QCoreApplication.instance().quit )
        self.ui.pushButton.clicked.connect( self.load_int )
        self.ui.pushButton_3.clicked.connect( self.new )
        self.ui.pushButton_4.clicked.connect( self.editor )
        self.ui.civEdit.clicked.connect(self.civ_edit)

        self.new_name   = "./saves/generated.hexmap"
        self.setting    = -1

    def load_int(self, filename=''):
        if filename=='':
            filename = QtGui.QFileDialog.getOpenFileName(None, 'Open HexMap', './saves', 'HexMaps (*.hexmap)')

        if filename=='':
            return()
        else:
            print("Loading {}".format(filename))
            print("The main program hasn't been implemented yet")
    def civ_edit(self):
        pass

    def editor(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Edit HexMap', './saves', 'HexMaps (*.hexmap)')
        self.hide()        
        if filename!='':
            print("Loading {}".format(filename))
        else:
            self.show()
            return()
        self.editor_ui.prep_map(filename)
        self.editor_ui.show()

    def new(self):
        dialog = mod_accept(self)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()
        if self.setting<0:
            pass
        else:
            if self.setting==0:
                print("new blank map of name {}".format(self.new_name))
            elif self.setting==1:
                print("Opening ridgeemaker, name {}".format(self.new_name))
                print(type(self.new_name))
                self.ridge_ui.save_name = self.new_name
                self.hide()
                self.ridge_ui.show()
            else:
                print("Generating from scratch, name {}".format(self.new_name))
                self.hide()
                full_chain.full_sim('cont', self.new_name )
                self.show()

class mod_accept(QtGui.QDialog):
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
        self.parent().new_name = "./saves/"+self.ui.lineEdit.text()
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


app = QtGui.QApplication(sys.argv)
app_instance = main_gui()


# quit button
if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())



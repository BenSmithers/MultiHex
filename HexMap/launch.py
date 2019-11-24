#!/usr/bin/python3.6
from PyQt4 import QtCore, QtGui
from HexMap.guis.main_menu import Ui_MainWindow as main_menu
from HexMap.map_paint import editor_gui

import sys
import time

# open the gui
class main_gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = main_menu()
        self.ui.setupUi(self)

        self.editor_ui = editor_gui(self)
        
        self.ui.pushButton_2.clicked.connect( QtCore.QCoreApplication.instance().quit )
        self.ui.pushButton.clicked.connect( self.load_int )
        self.ui.pushButton_3.clicked.connect( self.new )
        self.ui.pushButton_4.clicked.connect( self.editor )

    def load_int(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Load HexMap', './saves', 'HexMaps (*.hexmap)')
        if filename=='':
            return()
        else:
            print("Loading {}".format(filename))
            print("The main program hasn't been implemented yet")

    def editor(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Edit HexMap', './saves', 'HexMaps (*.hexmap)')
        
        if filename!='':
            print("Loading {}".format(filename))
        else:
            return()
        self.editor_ui.prep_map(filename)
        self.editor_ui.show()
        self.editor_ui.showFullScreen()
        #self.editor_gui.hide()
        

    def new(self):
        # Ridge or From scratch?  
        pass


app = QtGui.QApplication(sys.argv)
app_instance = main_gui()


# quit button
if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())



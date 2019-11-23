#!/usr/bin/python3.6
from PyQt4 import QtCore, QtGui
from HexMap.guis.main_menu import Ui_MainWindow as main_menu
# from HexMap.map_paint import editor_instance, application

import sys
import time

# open the gui
class main_gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = main_menu()
        self.ui.setupUi(self)

app = QtGui.QApplication(sys.argv)
app_instance = main_gui()

def load_int():
    filename = QtGui.QFileDialog.getOpenFileName(None, 'Load HexMap', './saves', 'HexMaps (*.hexmap)')
    if filename=='':
        return()
    else:
        print("Loading {}".format(filename))
        print("The main program hasn't been implemented yet")

def editor():
    filename = QtGui.QFileDialog.getOpenFileName(None, 'Edit HexMap', './saves', 'HexMaps (*.hexmap)')
    if filename=='':
        return()
    else:
        print("Loading {}".format(filename))
        app.hide()
#        editor_instance.show()
#        application.exec_()
#        application.hide()
        app.show()
   

def new():
    # Ridge or From scratch?  
    pass

# quit button
app_instance.ui.pushButton_2.clicked.connect( QtCore.QCoreApplication.instance().quit )
app_instance.ui.pushButton.clicked.connect( load_int )
app_instance.ui.pushButton_3.clicked.connect( new )
app_instance.ui.pushButton_4.clicked.connect( editor )

if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())



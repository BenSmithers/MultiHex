
from PyQt5 import QtCore, QtGui, QtWidgets
import os


"""
This file defines the UI of the dialog window is displayed when MultiHex first launches 
"""

class new_load_gui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 279)

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.picture = QtWidgets.QLabel(Dialog)
        self.picture.setText("")
        self.picture.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "Artwork", 'wiki_images', 'multihex_logo.png')).scaledToWidth(350) )
        self.picture.setScaledContents(False)
        self.picture.setObjectName("picture")
        self.picture.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.picture)

        self.new_map_button = QtWidgets.QPushButton(Dialog)
        self.new_map_button.setObjectName("new_map_button")
        self.verticalLayout.addWidget(self.new_map_button)

        self.load_map_button = QtWidgets.QPushButton(Dialog)
        self.load_map_button.setObjectName("load_map_button")
        self.verticalLayout.addWidget(self.load_map_button)

        self.quit_button = QtWidgets.QPushButton(Dialog)
        self.quit_button.setObjectName("quit_button")
        self.verticalLayout.addWidget(self.quit_button)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Welcome to MultiHex!"))
        self.new_map_button.setText(_translate("Dialog","New Map"))
        self.load_map_button.setText(_translate("Dialog","Load Map"))
        self.quit_button.setText(_translate("Dialog","Quit"))

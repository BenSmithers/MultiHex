# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_dialogue.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGridLayout, QApplication, QRadioButton, QLineEdit, QLabel, QDialogButtonBox, QSpacerItem, QSizePolicy

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(396, 298)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.title = QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName(_fromUtf8("title"))
        self.gridLayout.addWidget(self.title, 0, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 1)
        self.blank = QRadioButton(Dialog)
        self.blank.setObjectName(_fromUtf8("blank"))
        self.gridLayout.addWidget(self.blank, 2, 0, 1, 1)
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 6, 0, 1, 1)
        self.label = QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.ridgeline = QRadioButton(Dialog)
        self.ridgeline.setObjectName(_fromUtf8("ridgeline"))
        self.gridLayout.addWidget(self.ridgeline, 3, 0, 1, 1)
        self.full = QRadioButton(Dialog)
        self.full.setObjectName(_fromUtf8("full"))
        self.gridLayout.addWidget(self.full, 4, 0, 1, 1)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.title.setText(_translate("Dialog", "New Map Parameters", None))
        self.blank.setText(_translate("Dialog", "Blank Map", None))
        self.lineEdit.setText(_translate("Dialog", "generated.hexmap", None))
        self.label.setText(_translate("Dialog", "New Map Name:", None))
        self.ridgeline.setText(_translate("Dialog", "Generate from ridgeline", None))
        self.full.setText(_translate("Dialog", "Full Generation", None))


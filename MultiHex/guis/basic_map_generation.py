# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic_map_generation.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class basic_map_dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(526, 263)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileNameEntry = QtWidgets.QLineEdit(Dialog)
        self.fileNameEntry.setObjectName("fileNameEntry")
        self.verticalLayout.addWidget(self.fileNameEntry)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.map_type_combo = QtWidgets.QComboBox(Dialog)
        self.map_type_combo.setObjectName("map_type_combo")
        self.map_type_combo.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.map_type_combo)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tileset_combo = QtWidgets.QComboBox(Dialog)
        self.tileset_combo.setObjectName("tileset_combo")
        self.tileset_combo.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tileset_combo)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.gen_preset_combo = QtWidgets.QComboBox(Dialog)
        self.gen_preset_combo.setObjectName("gen_preset_combo")
        self.gen_preset_combo.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gen_preset_combo)
        self.advanced_gen_button = QtWidgets.QPushButton(Dialog)
        self.advanced_gen_button.setObjectName("advanced_gen_button")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.advanced_gen_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.generate_button = QtWidgets.QPushButton(Dialog)
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout.addWidget(self.generate_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Map Settings"))
        self.label.setText(_translate("Dialog", "Map Type"))
        self.map_type_combo.setItemText(0, _translate("Dialog", "Standard"))
        self.label_2.setText(_translate("Dialog", "Tileset"))
        self.tileset_combo.setItemText(0, _translate("Dialog", "Standard"))
        self.label_3.setText(_translate("Dialog", "Generation Preset"))
        self.gen_preset_combo.setItemText(0, _translate("Dialog", "Continents"))
        self.advanced_gen_button.setText(_translate("Dialog", "Advanced Generation"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.generate_button.setText(_translate("Dialog", "Generate"))


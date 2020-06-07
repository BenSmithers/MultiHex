# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'civilization_design_file.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QDialog, QColorDialog

from MultiHex.map_types.overland import Town, Nation
from MultiHex.objects import Icons
from MultiHex.about_class import about_dialog
from MultiHex.tools import QEntityItem

from MultiHex.guis.main_gui import main_gui
from MultiHex.guis.ward_dialog import Ui_Dialog as ward_ui



import os
art_dir = os.path.join( os.path.dirname(__file__), '..', 'Artwork', 'buttons')

class civ_ui:
    def __init__(self, MainWindow):
        self.parent = MainWindow

        which_ui = MainWindow.ui

        self.ent_select_button_0 = QtWidgets.QToolButton(which_ui.centralwidget)
        self.ent_select_button_0.setMinimumSize(QtCore.QSize(40, 40))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_location.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ent_select_button_0.setIcon(icon1)
        self.ent_select_button_0.setIconSize(QtCore.QSize(32, 32))
        self.ent_select_button_0.setObjectName("ent_select_button_0")
        which_ui.toolPane.addWidget(self.ent_select_button_0)
        self.loc_button_1 = QtWidgets.QToolButton(which_ui.centralwidget)
        self.loc_button_1.setMinimumSize(QtCore.QSize(40, 40))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "new_location.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loc_button_1.setIcon(icon5)
        self.loc_button_1.setIconSize(QtCore.QSize(32, 32))
        self.loc_button_1.setObjectName("loc_button_1")
        which_ui.toolPane.addWidget(self.loc_button_1)
        self.setl_button_2 = QtWidgets.QToolButton(which_ui.centralwidget)
        self.setl_button_2.setMinimumSize(QtCore.QSize(40, 40))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "new_settle.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setl_button_2.setIcon(icon6)
        self.setl_button_2.setIconSize(QtCore.QSize(32, 32))
        self.setl_button_2.setObjectName("setl_button_2")
        which_ui.toolPane.addWidget(self.setl_button_2)
        self.road_button_3 = QtWidgets.QToolButton(which_ui.centralwidget)
        self.road_button_3.setMinimumSize(QtCore.QSize(40, 40))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(os.path.join( art_dir, "new_road.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.road_button_3.setIcon(icon7)
        self.road_button_3.setIconSize(QtCore.QSize(32, 32))
        self.road_button_3.setObjectName("road_button_3")
        which_ui.toolPane.addWidget(self.road_button_3)
        self.count_sel_button_1 = QtWidgets.QToolButton(which_ui.centralwidget)
        self.count_sel_button_1.setMinimumSize(QtCore.QSize(40, 40))
        self.count_sel_button_1.setToolTip("")
        self.count_sel_button_1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_county.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.count_sel_button_1.setIcon(icon2)
        self.count_sel_button_1.setIconSize(QtCore.QSize(32, 32))
        self.count_sel_button_1.setObjectName("count_sel_button_1")
        which_ui.toolPane.addWidget(self.count_sel_button_1)
        self.count_button_4 = QtWidgets.QToolButton(which_ui.centralwidget)
        self.count_button_4.setMinimumSize(QtCore.QSize(40, 40))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "county.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.count_button_4.setIcon(icon8)
        self.count_button_4.setIconSize(QtCore.QSize(32, 32))
        self.count_button_4.setObjectName("count_button_4")
        which_ui.toolPane.addWidget(self.count_button_4)
        self.spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        which_ui.toolPane.addItem(self.spacerItem2)

        self.Locations = QtWidgets.QWidget()
        self.Locations.setGeometry(QtCore.QRect(0, 0, 250, 630))
        self.Locations.setObjectName("Locations")
        self.formLayout_3 = QtWidgets.QFormLayout(self.Locations)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setObjectName("formLayout_3")
        self.loc_name_edit = QtWidgets.QLineEdit(self.Locations)
        self.loc_name_edit.setObjectName("loc_name_edit")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.loc_name_edit)
        self.loc_name_label = QtWidgets.QLabel(self.Locations)
        self.loc_name_label.setObjectName("loc_name_label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.loc_name_label)
        self.loc_desc_label = QtWidgets.QLabel(self.Locations)
        self.loc_desc_label.setObjectName("loc_desc_label")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.loc_desc_label)
        self.loc_desc_edit = QtWidgets.QTextEdit(self.Locations)
        self.loc_desc_edit.setObjectName("loc_desc_edit")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.loc_desc_edit)
        self.loc_icon = QtWidgets.QComboBox(self.Locations) 
        self.loc_icon.setObjectName("loc_icon")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.loc_icon)
        self.loc_save = QtWidgets.QPushButton(self.Locations)
        self.loc_save.setObjectName("loc_save")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.loc_save)
        self.status_label = QtWidgets.QLabel(self.Locations)
        self.status_label.setMinimumSize(QtCore.QSize(80, 0))
        self.status_label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.status_label.setFrameShape(QtWidgets.QFrame.Box)
        self.status_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.status_label)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_3.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem3)
        self.loc_list_view = QtWidgets.QListView(self.Locations)
        self.loc_list_view.setObjectName("loc_list_view")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.loc_list_view)
        self.loc_deselect = QtWidgets.QPushButton(self.Locations)
        self.loc_deselect.setObjectName("loc_deselect")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.loc_deselect)
        self.loc_delete = QtWidgets.QPushButton(self.Locations)
        self.loc_delete.setObjectName("loc_delete")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.loc_delete)
        which_ui.contextPane.addItem(self.Locations, "")
        self.Settlements = QtWidgets.QWidget()
        self.Settlements.setGeometry(QtCore.QRect(0, 0, 250, 630))
        self.Settlements.setObjectName("Settlements")
        self.formLayout = QtWidgets.QFormLayout(self.Settlements)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.set_name_label = QtWidgets.QLabel(self.Settlements)
        self.set_name_label.setObjectName("set_name_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.set_name_label)
        self.set_name_edit = QtWidgets.QLineEdit(self.Settlements)
        self.set_name_edit.setObjectName("set_name_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.set_name_edit)
        self.set_desc_label = QtWidgets.QLabel(self.Settlements)
        self.set_desc_label.setObjectName("set_desc_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.set_desc_label)
        self.set_desc_edit = QtWidgets.QTextEdit(self.Settlements)
        self.set_desc_edit.setObjectName("set_desc_edit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.set_desc_edit)
        self.set_button_apply = QtWidgets.QPushButton(self.Settlements)
        self.set_button_apply.setObjectName("set_button_apply")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.set_button_apply)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem4)
        self.set_ward_label = QtWidgets.QLabel(self.Settlements)
        self.set_ward_label.setObjectName("set_ward_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.set_ward_label)
        self.set_ward_dd = QtWidgets.QComboBox(self.Settlements)
        self.set_ward_dd.setObjectName("set_ward_dd")
        self.set_ward_dd.addItem("")
        self.set_ward_dd.addItem("")
        self.set_ward_dd.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.set_ward_dd)
        self.set_wname_label = QtWidgets.QLabel(self.Settlements)
        self.set_wname_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.set_wname_label.setObjectName("set_wname_label")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.set_wname_label)
        self.set_name_view = QtWidgets.QLabel(self.Settlements)
        self.set_name_view.setFrameShape(QtWidgets.QFrame.Box)
        self.set_name_view.setFrameShadow(QtWidgets.QFrame.Raised)
        self.set_name_view.setText("")
        self.set_name_view.setObjectName("set_name_view")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.set_name_view)
        self.set_pop_label = QtWidgets.QLabel(self.Settlements)
        self.set_pop_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.set_pop_label.setObjectName("set_pop_label")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.set_pop_label)
        self.set_pop_disp = QtWidgets.QLabel(self.Settlements)
        self.set_pop_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.set_pop_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.set_pop_disp.setText("")
        self.set_pop_disp.setObjectName("set_pop_disp")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.set_pop_disp)
        self.set_wealth_label = QtWidgets.QLabel(self.Settlements)
        self.set_wealth_label.setObjectName("set_wealth_label")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.set_wealth_label)
        self.set_weal_disp = QtWidgets.QLabel(self.Settlements)
        self.set_weal_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.set_weal_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.set_weal_disp.setText("")
        self.set_weal_disp.setObjectName("set_weal_disp")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.set_weal_disp)
        self.set_demo_view = QtWidgets.QTextBrowser(self.Settlements)
        self.set_demo_view.setObjectName("set_demo_view")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.set_demo_view)
        self.set_edit_button = QtWidgets.QPushButton(self.Settlements)
        self.set_edit_button.setObjectName("set_edit_button")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.SpanningRole, self.set_edit_button)
        self.line = QtWidgets.QFrame(self.Settlements)
        self.line.setMinimumSize(QtCore.QSize(100, 0))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.line)
        which_ui.contextPane.addItem(self.Settlements, "")
        self.Roads = QtWidgets.QWidget()
        self.Roads.setGeometry(QtCore.QRect(0, 0, 250, 630))
        self.Roads.setObjectName("Roads")
        self.formLayout_2 = QtWidgets.QFormLayout(self.Roads)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setObjectName("formLayout_2")
        self.road_name_lbl = QtWidgets.QLabel(self.Roads)
        self.road_name_lbl.setObjectName("road_name_lbl")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.road_name_lbl)
        self.road_name_edit = QtWidgets.QLineEdit(self.Roads)
        self.road_name_edit.setObjectName("road_name_edit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.road_name_edit)
        self.road_qual_lbl = QtWidgets.QLabel(self.Roads)
        self.road_qual_lbl.setObjectName("road_qual_lbl")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.road_qual_lbl)
        self.road_qual_edit = QtWidgets.QDoubleSpinBox(self.Roads)
        self.road_qual_edit.setObjectName("road_qual_edit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.road_qual_edit)
        self.roads_list = QtWidgets.QListView(self.Roads)
        self.roads_list.setObjectName("roads_list")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.roads_list)
        self.road_roads_lbl = QtWidgets.QLabel(self.Roads)
        self.road_roads_lbl.setObjectName("road_roads_lbl")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.road_roads_lbl)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.road_start_pop = QtWidgets.QPushButton(self.Roads)
        self.road_start_pop.setObjectName("road_start_pop")
        self.gridLayout.addWidget(self.road_start_pop, 0, 0, 1, 1)
        self.road_end_pop = QtWidgets.QPushButton(self.Roads)
        self.road_end_pop.setObjectName("road_end_pop")
        self.gridLayout.addWidget(self.road_end_pop, 0, 1, 1, 1)
        self.road_end_add = QtWidgets.QPushButton(self.Roads)
        self.road_end_add.setObjectName("road_end_add")
        self.gridLayout.addWidget(self.road_end_add, 1, 1, 1, 1)
        self.road_start_add = QtWidgets.QPushButton(self.Roads)
        self.road_start_add.setObjectName("road_start_add")
        self.gridLayout.addWidget(self.road_start_add, 1, 0, 1, 1)
        self.formLayout_2.setLayout(5, QtWidgets.QFormLayout.SpanningRole, self.gridLayout)
        self.delete_road = QtWidgets.QPushButton(self.Roads)
        self.delete_road.setObjectName("delete_road")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.delete_road)
        self.road_apply_but = QtWidgets.QPushButton( self.Roads )
        self.road_apply_but.setObjectName("road_apply_but")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.road_apply_but)
        which_ui.contextPane.addItem(self.Roads, "")
        self.Counties = QtWidgets.QWidget()
        self.Counties.setGeometry(QtCore.QRect(0, 0, 250, 630))
        self.Counties.setObjectName("Counties")
        self.formLayout_4 = QtWidgets.QFormLayout(self.Counties)
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setObjectName("formLayout_4")
        self.count_name_lbl = QtWidgets.QLabel(self.Counties)
        self.count_name_lbl.setObjectName("count_name_lbl")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.count_name_lbl)
        self.count_name_edit = QtWidgets.QLineEdit(self.Counties)
        self.count_name_edit.setObjectName("count_name_edit")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.count_name_edit)
        self.count_pop_disp_2 = QtWidgets.QLabel(self.Counties)
        self.count_pop_disp_2.setObjectName("count_pop_disp_2")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.count_pop_disp_2)
        self.count_pop_disp = QtWidgets.QLabel(self.Counties)
        self.count_pop_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.count_pop_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.count_pop_disp.setText("")
        self.count_pop_disp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.count_pop_disp.setObjectName("count_pop_disp")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.count_pop_disp)
        self.count_weal_lbl = QtWidgets.QLabel(self.Counties)
        self.count_weal_lbl.setObjectName("count_weal_lbl")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.count_weal_lbl)
        self.count_weal_disp = QtWidgets.QLabel(self.Counties)
        self.count_weal_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.count_weal_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.count_weal_disp.setText("")
        self.count_weal_disp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.count_weal_disp.setObjectName("count_weal_disp")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.count_weal_disp)
        self.count_city_lbl = QtWidgets.QLabel(self.Counties)
        self.count_city_lbl.setObjectName("count_city_lbl")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.count_city_lbl)
        self.count_city_list = QtWidgets.QListView(self.Counties)
        self.count_city_list.setObjectName("count_city_list")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.count_city_list)
        self.label_2 = QtWidgets.QLabel(self.Counties)
        self.label_2.setObjectName("label_2")
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalSlider = QtWidgets.QSlider(self.Counties)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.horizontalSlider)
        self.label_3 = QtWidgets.QLabel(self.Counties)
        self.label_3.setObjectName("label_3")
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.Counties)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.horizontalSlider_2)
        self.label_4 = QtWidgets.QLabel(self.Counties)
        self.label_4.setObjectName("label_4")
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.Counties)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.horizontalSlider_3)

        self.county_color_lbl = QtWidgets.QLabel(self.Counties)
        self.county_color_lbl.setObjectName("county_color_lbl")
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.LabelRole,self.county_color_lbl)
        self.county_color_button = QtWidgets.QPushButton(self.Counties)
        self.county_color_button.setObjectName("county_color_button")
        self.formLayout_4.setWidget(9,QtWidgets.QFormLayout.FieldRole,self.county_color_button)

        self.pushButton = QtWidgets.QPushButton(self.Counties)
        self.pushButton.setObjectName("pushButton")
        self.formLayout_4.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.pushButton)


        self.count_king_button = QtWidgets.QPushButton(self.Counties)
        self.count_king_button.setObjectName("count_king_button")
        self.formLayout_4.setWidget(12, QtWidgets.QFormLayout.SpanningRole, self.count_king_button)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_4.setItem(11, QtWidgets.QFormLayout.LabelRole, spacerItem5)
        self.label_12 = QtWidgets.QLabel(self.Counties)
        self.label_12.setObjectName("label_12")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtWidgets.QLabel(self.Counties)
        self.label_13.setFrameShape(QtWidgets.QFrame.Box)
        self.label_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_13)
        which_ui.contextPane.addItem(self.Counties, "")

        self.Kingdoms = QtWidgets.QWidget()
        self.Kingdoms.setGeometry(QtCore.QRect(0, 0, 250, 630))
        self.Kingdoms.setObjectName("Kingdoms")
        self.formLayout_5 = QtWidgets.QFormLayout(self.Kingdoms)
        self.formLayout_5.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_5.setObjectName("formLayout_5")
        self.king_name_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_name_lbl.setObjectName("king_name_lbl")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.king_name_lbl)
        self.king_name_edit = QtWidgets.QLineEdit(self.Kingdoms)
        self.king_name_edit.setText("")
        self.king_name_edit.setObjectName("king_name_edit")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.king_name_edit)
        self.king_subj_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_subj_lbl.setObjectName("king_subj_lbl")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.king_subj_lbl)
        self.king_subj_disp = QtWidgets.QLabel(self.Kingdoms)
        self.king_subj_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.king_subj_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.king_subj_disp.setText("")
        self.king_subj_disp.setObjectName("king_subj_disp")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.king_subj_disp)
        self.king_weal_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_weal_lbl.setObjectName("king_weal_lbl")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.king_weal_lbl)
        self.king_weal_disp = QtWidgets.QLabel(self.Kingdoms)
        self.king_weal_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.king_weal_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.king_weal_disp.setText("")
        self.king_weal_disp.setObjectName("king_weal_disp")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.king_weal_disp)
        self.label_11 = QtWidgets.QLabel(self.Kingdoms)
        self.label_11.setObjectName("label_11")
        self.formLayout_5.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.label_11)
        self.listWidget = QtWidgets.QListView(self.Kingdoms)
        self.listWidget.setObjectName("listWidget")
        self.formLayout_5.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.listWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.king_count_new_but = QtWidgets.QPushButton(self.Kingdoms)
        self.king_count_new_but.setObjectName("king_count_new_but")
        self.horizontalLayout_3.addWidget(self.king_count_new_but)
        self.king_count_rem_but = QtWidgets.QPushButton(self.Kingdoms)
        self.king_count_rem_but.setObjectName("king_count_rem_but")
        self.horizontalLayout_3.addWidget(self.king_count_rem_but)
        self.formLayout_5.setLayout(10, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_3)
        self.king_dissolve_but = QtWidgets.QPushButton(self.Kingdoms)
        self.king_dissolve_but.setObjectName("king_dissolve_but")
        self.formLayout_5.setWidget(13, QtWidgets.QFormLayout.SpanningRole, self.king_dissolve_but)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(12, QtWidgets.QFormLayout.LabelRole, spacerItem6)
        self.king_gdg_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_gdg_lbl.setObjectName("king_gdg_lbl")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.king_gdg_lbl)
        self.king_gdg_disp = QtWidgets.QLabel(self.Kingdoms)
        self.king_gdg_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.king_gdg_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.king_gdg_disp.setText("")
        self.king_gdg_disp.setObjectName("king_gdg_disp")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.king_gdg_disp)
        self.king_order_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_order_lbl.setObjectName("king_order_lbl")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.king_order_lbl)
        self.king_order_sld = QtWidgets.QSlider(self.Kingdoms)
        self.king_order_sld.setOrientation(QtCore.Qt.Horizontal)
        self.king_order_sld.setObjectName("king_order_sld")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.king_order_sld) #9 10 11
        self.king_war_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_war_lbl.setObjectName("king_war_lbl")
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.king_war_lbl)
        self.king_war_sld = QtWidgets.QSlider(self.Kingdoms)
        self.king_war_sld.setOrientation(QtCore.Qt.Horizontal)
        self.king_war_sld.setObjectName("king_war_sld")
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.king_war_sld)
        self.king_spirit_lbl = QtWidgets.QLabel(self.Kingdoms)
        self.king_spirit_lbl.setObjectName("king_spirit_lbl")
        self.formLayout_5.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.king_spirit_lbl)
        self.king_spirit_sld = QtWidgets.QSlider(self.Kingdoms)
        self.king_spirit_sld.setOrientation(QtCore.Qt.Horizontal)
        self.king_spirit_sld.setObjectName("king_spirit_sld")
        self.formLayout_5.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.king_spirit_sld)
        self.king_apply = QtWidgets.QPushButton(self.Kingdoms)
        self.king_apply.setObjectName("king_apply")
        self.formLayout_5.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.king_apply)
        self.king_state = QtWidgets.QLabel()
        self.king_state.setObjectName("king_state")
        self.formLayout_5.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.king_state)
        which_ui.contextPane.addItem(self.Kingdoms, "")


        self.menuView = QtWidgets.QMenu(which_ui.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(which_ui.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.actionBiome_Borders = QtWidgets.QAction(MainWindow)
        self.actionBiome_Borders.setCheckable(True)
        self.actionBiome_Borders.setObjectName("actionBiome_Borders")
        self.actionCounty_Borders = QtWidgets.QAction(MainWindow)
        self.actionCounty_Borders.setCheckable(True)
        self.actionCounty_Borders.setChecked(True)
        self.actionCounty_Borders.setObjectName("actionCounty_Borders")

        self.actionAbout_MultiHex = QtWidgets.QAction(MainWindow)
        self.actionAbout_MultiHex.setObjectName("actionAbout_MultiHex")
        self.actionBiome_Names = QtWidgets.QAction(MainWindow)
        self.actionBiome_Names.setCheckable(True)
        self.actionBiome_Names.setChecked(True)
        self.actionBiome_Names.setObjectName("actionBiome_Names")
        self.actionCounty_Names = QtWidgets.QAction(MainWindow)
        self.actionCounty_Names.setCheckable(True)
        self.actionCounty_Names.setChecked(True)
        self.actionCounty_Names.setObjectName("actionCounty_Names")
        self.actionTowns = QtWidgets.QAction(MainWindow)
        self.actionTowns.setCheckable(True)
        self.actionTowns.setChecked(True)
        self.actionTowns.setObjectName("actionTowns")
        self.actionLocations = QtWidgets.QAction(MainWindow)
        self.actionLocations.setCheckable(True)
        self.actionLocations.setChecked(True)
        self.actionLocations.setObjectName("actionLocations")
        self.menuView.addAction(self.actionBiome_Borders)
        self.menuView.addAction(self.actionBiome_Names)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionLocations)
        self.menuView.addAction(self.actionTowns)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionCounty_Borders)
        self.menuView.addAction(self.actionCounty_Names)
        self.menuHelp.addAction(self.actionAbout_MultiHex)

        which_ui.menubar.addAction(self.menuView.menuAction())
        which_ui.menubar.addAction(self.menuHelp.menuAction())

        which_ui.contextPane.setCurrentIndex(0)

        _translate = QtCore.QCoreApplication.translate
        self.ent_select_button_0.setText(_translate("MainWindow", "..."))
        self.loc_button_1.setText(_translate("MainWindow", "..."))
        self.setl_button_2.setText(_translate("MainWindow", "..."))
        self.road_button_3.setText(_translate("MainWindow", "..."))
        self.count_button_4.setText(_translate("MainWindow", "..."))
        self.loc_name_label.setText(_translate("MainWindow", "Name"))
        self.loc_desc_label.setText(_translate("MainWindow", "\n"
        " Description"))
        self.loc_save.setText(_translate("MainWindow", "Save"))
        self.status_label.setText(_translate("MainWindow", "..."))
        self.loc_deselect.setText(_translate("MainWindow", "Deselect"))
        self.loc_delete.setText(_translate("MainWindow", "Delete"))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.Locations), _translate("MainWindow", "Locations"))
        self.set_name_label.setText(_translate("MainWindow", "Name"))
        self.set_desc_label.setText(_translate("MainWindow", "\n"
        "Description"))
        self.set_button_apply.setText(_translate("MainWindow", "Apply"))
        self.set_ward_label.setText(_translate("MainWindow", "City Section:"))
        self.set_ward_dd.setItemText(0, _translate("MainWindow", "City as Whole"))
        self.set_ward_dd.setItemText(1, _translate("MainWindow", "City Center"))
        self.set_ward_dd.setItemText(2, _translate("MainWindow", "Add New Ward"))
        self.set_wname_label.setText(_translate("MainWindow", "Name:"))
        self.set_pop_label.setText(_translate("MainWindow", "Population:"))
        self.set_wealth_label.setText(_translate("MainWindow", "Wealth:"))
        self.set_edit_button.setText(_translate("MainWindow", "Edit Section"))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.Settlements), _translate("MainWindow", "Settlements"))
        self.road_name_lbl.setText(_translate("MainWindow", "Name: "))
        self.road_qual_lbl.setText(_translate("MainWindow", "Quality: "))
        self.road_roads_lbl.setText(_translate("MainWindow", "\n"
        "\nRoads: "))
        self.road_start_pop.setText(_translate("MainWindow", "Pop Start"))
        self.road_end_pop.setText(_translate("MainWindow", "Pop End"))
        self.road_end_add.setText(_translate("MainWindow", "Add To End"))
        self.road_start_add.setText(_translate("MainWindow", "Add To Start"))
        self.delete_road.setText(_translate("MainWindow", "Delete Road"))
        self.road_apply_but.setText(_translate("MainWindow","Apply"))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.Roads), _translate("MainWindow", "Roads"))
        self.count_name_lbl.setText(_translate("MainWindow", "Name:"))
        self.count_pop_disp_2.setText(_translate("MainWindow", "Population:"))
        self.count_weal_lbl.setText(_translate("MainWindow", "Wealth:"))
        self.count_city_lbl.setText(_translate("MainWindow", "\n"
        "Contained Cities:"))
        self.label_2.setText(_translate("MainWindow", "Order: "))
        self.label_3.setText(_translate("MainWindow", "War: "))
        self.label_4.setText(_translate("MainWindow", "Spirit: "))
        self.county_color_lbl.setText(_translate("MainWindow","Choose Color: "))
        self.pushButton.setText(_translate("MainWindow", "Apply"))
        self.count_king_button.setText(_translate("MainWindow", "Create New Kingdom"))
        self.label_12.setText(_translate("MainWindow", "GDG: "))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.Counties), _translate("MainWindow", "Counties"))
        self.king_name_lbl.setText(_translate("MainWindow", "Name: "))
        self.king_subj_lbl.setText(_translate("MainWindow", "Subjects: "))
        self.king_weal_lbl.setText(_translate("MainWindow", "Wealth: "))
        self.label_11.setText(_translate("MainWindow", "\n"
        "Counties:"))
        self.king_count_new_but.setText(_translate("MainWindow", "Add New County"))
        self.king_count_rem_but.setText(_translate("MainWindow", "Remove"))
        self.king_apply.setText(_translate("MainWindow","Apply"))
        self.king_dissolve_but.setText(_translate("MainWindow", "Dissolve"))
        self.king_gdg_lbl.setText(_translate("MainWindow", "GDG: "))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.Kingdoms), _translate("MainWindow", "Kingoms"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionBiome_Borders.setText(_translate("MainWindow", "Biome Borders"))
        self.actionCounty_Borders.setText(_translate("MainWindow", "County Borders"))
        self.king_state.setText(_translate("MainWindow","..."))
        self.actionAbout_MultiHex.setText(_translate("MainWindow", "About MultiHex"))
        self.actionBiome_Names.setText(_translate("MainWindow", "Biome Names"))
        self.actionCounty_Names.setText(_translate("MainWindow", "County Names"))
        self.actionTowns.setText(_translate("MainWindow", "Towns"))
        self.actionLocations.setText(_translate("MainWindow", "Locations"))
        self.king_order_lbl.setText(_translate("MainWindow", "Order"))
        self.king_war_lbl.setText(_translate("MainWindow", "War"))
        self.king_spirit_lbl.setText(_translate("MainWindow", "Spirit"))
        self.king_spirit_sld.setEnabled(False)
        self.king_war_sld.setEnabled(False)
        self.king_order_sld.setEnabled(False)

        # drop-down menu buttons
        self.actionBiome_Borders.triggered.connect( self.action_biome_bord )
        self.actionCounty_Borders.triggered.connect(self.action_county_bord )
        self.actionBiome_Names.triggered.connect( self.action_biome_names )
        self.actionCounty_Names.triggered.connect( self.action_county_names )
        self.actionTowns.triggered.connect( self.action_towns )
        self.actionLocations.triggered.connect( self.action_locations )
        self.actionAbout_MultiHex.triggered.connect( self.actionAbout )

        #toolbar buttons
        self.ent_select_button_0.clicked.connect(  self.entity_selector_toolbar)
        self.count_sel_button_1.clicked.connect( self.county_selector_toolbar )
        self.loc_button_1.clicked.connect( self.new_location_button_toolbar)
        self.setl_button_2.clicked.connect( self.new_settlement_button_toolbar )
        self.road_button_3.clicked.connect( self.new_road_button_toolbar )
        self.count_button_4.clicked.connect( self.new_county_button_toolbar )

        # location tab buttons 
        self.loc_list_entry = QtGui.QStandardItemModel()
        self.loc_list_view.setModel( self.loc_list_entry )
        self.loc_save.clicked.connect( self.loc_save_entity )
        self.loc_delete.clicked.connect( self.loc_delete_func )
        self.loc_deselect.clicked.connect( self.parent.entity_control.deselect_hex )
        self.loc_list_view.clicked[QtCore.QModelIndex].connect(self.loc_list_item_clicked)
        
        # settlement tab buttons 
        self.set_ward_dd.currentIndexChanged.connect( self.set_dropdown_activate )
        self.set_button_apply.clicked.connect( self.set_button_apply_func )
        self.set_edit_button.clicked.connect( self.set_ward_edit_button )

        # road tab buttons
        self.road_list_entry = QtGui.QStandardItemModel()
        self.roads_list.setModel( self.road_list_entry )
        self.roads_list.clicked[QtCore.QModelIndex].connect( self.road_item_clicked )
        self.road_start_pop.clicked.connect( self.road_ps_button )
        self.road_end_pop.clicked.connect( self.road_pe_button )
        self.road_end_add.clicked.connect( self.road_add_end )
        self.road_start_add.clicked.connect( self.road_add_start )
        self.delete_road.clicked.connect( self.road_delete )
        self.road_apply_but.clicked.connect( self.road_apply )

        # county tab buttons
        self.county_list_entry = QtGui.QStandardItemModel()
        self.count_city_list.setModel( self.county_list_entry)
        self.county_color_button.clicked.connect(self.county_color_click)
        self.pushButton.clicked.connect( self.county_apply )
        self.count_king_button.clicked.connect( self.county_kingdom_button )
        self.count_city_list.clicked[QtCore.QModelIndex].connect(self.county_list_item_clicked)

        # Nation List Buttons
        self.nation_list_entry = QtGui.QStandardItemModel()
        self.listWidget.setModel( self.nation_list_entry )
        self.listWidget.clicked[QtCore.QModelIndex].connect(self.nation_list_item_clicked)
        self.king_apply.clicked.connect( self.nation_apply_button )
        self.king_count_new_but.clicked.connect(self.nation_add_to)
        self.king_count_rem_but.clicked.connect(self.nation_remove_from)
        self.king_dissolve_but.clicked.connect(self.nation_dissolve)

        self.ward_accept=False

        self.icons = self.parent.icons
        for icon in self.icons.pixdict.keys():
            self.loc_icon.addItem( QtGui.QIcon(self.icons.pixdict[icon]), icon )

    def clear_ui(self, which_ui):
        which_ui.toolPane.removeWidget(self.ent_select_button_0)
        which_ui.toolPane.removeWidget(self.count_sel_button_1)
        which_ui.toolPane.removeWidget(self.loc_button_1)
        which_ui.toolPane.removeWidget(self.setl_button_2)
        which_ui.toolPane.removeWidget(self.road_button_3)
        which_ui.toolPane.removeWidget(self.count_button_4)

        self.ent_select_button_0.deleteLater()
        self.count_sel_button_1.deleteLater()
        self.loc_button_1.deleteLater()
        self.setl_button_2.deleteLater()
        self.road_button_3.deleteLater()
        self.count_button_4.deleteLater()

        which_ui.toolPane.removeItem(self.spacerItem2)

        for i in range(5):
            which_ui.contextPane.removeItem(0)

        which_ui.menubar.removeAction(self.menuView.menuAction())
        which_ui.menubar.removeAction(self.menuHelp.menuAction())

    def action_biome_names(self):
        state = self.actionBiome_Names.isChecked()
        self.parent.biome_control.draw_names = state
        self.parent._redraw_biomes()

    def action_biome_bord(self):
        state = self.actionBiome_Borders.isChecked()
        self.parent.biome_control.draw_borders = state
        self.parent._redraw_biomes()

    def action_county_bord(self):
        state = self.actionCounty_Borders.isChecked()
        self.parent.county_control.draw_borders = state
        self.parent._redraw_counties()
        
    def action_county_names(self):
        state = self.actionCounty_Names.isChecked()
        self.parent.county_control.draw_names = state
        self.parent._redraw_counties()

    def action_towns(self):
        state = self.actionTowns.isChecked()
        self.parent.entity_control.draw_settlements = state
        self.parent._redraw_entities()

    def action_locations(self):
        state = self.actionLocations.isChecked()
        self.parent.entity_control.draw_entities = state
        self._redraw_entities()

    def actionAbout(self):
        dialog = about_dialog( self.parent )
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()

    def road_item_clicked( self , index=None):
        item = self.road_list_entry.itemFromIndex(index)
        pID = item.eID

        if pID is not None:
            the_path = self.parent.main_map.path_catalog['roads'][pID]

            self.road_name_edit.setText(the_path.name)
            self.road_qual_edit.setValue( the_path.quality )

            self.parent.path_control.select_pid( pID )
        else:
            self.road_name_edit.setText('')
            self.road_qual_edit.setValue( 0.0 )

    def road_apply(self):
        if self.parent.path_control.selected_pid is not None:
            self.parent.main_map.path_catalog['roads'][self.parent.path_control.selected_pid].name = self.road_name_edit.text()
            self.parent.main_map.path_catalog['roads'][self.parent.path_control.selected_pid].quality = self.road_qual_edit.value()

            # update the list to reflect the new name! 
            self.road_update_list()

    def road_ps_button(self):
        self.parent.path_control.pop_selected_start()

    def road_pe_button(self):
        self.parent.path_control.pop_selected_end()
   
    # these two just tell the path control to enter a specific state relating to adding to the end of a 
    def road_add_start(self):
        self.parent.path_control.prepare( 4 )
    def road_add_end(self):
        self.parent.path_control.prepare( 3 )

    def road_delete(self):
        self.parent.path_control.delete_selected()
        self.road_update_list()

    def road_update_list( self ):
        self.road_list_entry.clear()
        
        if not( 'roads' in self.parent.main_map.path_catalog ):
            return

        for pID in self.parent.main_map.path_catalog['roads']:
            self.road_list_entry.appendRow( QEntityItem(self.parent.main_map.path_catalog['roads'][pID].name , pID))

    def set_button_apply_func(self):

        which = self.parent.entity_control.selected

        # skip this if nothing is selected
        if not isinstance(which, int):
            return

        # ensure that the selected eID is actually an entity
        if not isinstance( self.parent.main_map.eid_catalogue[which], Town ):
            raise TypeError("A {} type object is selected instead of a town. How did this happen?".format(type(self.parent.main_map.eid_catalogue[which])))

        # apply the changes
        self.parent.main_map.eid_catalogue[which].name = self.set_name_edit.text()
        self.parent.main_map.eid_catalogue[which].description = self.set_desc_edit.toPlainText()

    def set_dropdown_activate(self, index):
        """
        Called when an entry is selected in the drop down menu in the settlement tab
         0 - city as a whole
         1 - city center
         ... - wards
         -1 - new ward
        """
        which = self.parent.entity_control.selected
        if not isinstance( which, int):
            return #none is selec ted
        if not isinstance( self.parent.main_map.eid_catalogue[which], Town ):
            raise TypeError("A {} type object is selected instead of a town. How did this happen?".format(type(self.parent.main_map.eid_catalogue[which])))

        if index==(self.set_ward_dd.count() - 1):
            # add new ward
            pass
        elif index==0:
            # all city
            self.set_update_ward_info( which )
        else:
            # take the index, subtract 1. This gives the ward number! 
            self.set_update_ward_info( which, index - 1)

    def set_update_selection(self, eID=None):
        """
        Updates the settlement menu gui with the proper information about it
        """
        # set dropdown menu to default setup 
        while self.set_ward_dd.count()>3:
            self.set_ward_dd.removeItem( self.set_ward_dd.count() -2 )

        if eID is not None:
            assert( isinstance( eID , int ))
            if not isinstance( self.parent.main_map.eid_catalogue[eID], Town):
                raise TypeError("Something terribly wrong has happened. Trying to update Entity {} as if it were {}, but it is {}".format(eID, Town, type( self.main_map.eid_catalogue[eID]) ))

            self.set_name_edit.setText( self.parent.main_map.eid_catalogue[ eID ].name)
            self.set_desc_edit.setText( self.parent.main_map.eid_catalogue[ eID ].description )

            self.set_ward_dd.setCurrentIndex(0)
            self.set_update_ward_info(eID)

            for ward in self.parent.main_map.eid_catalogue[eID].wards:
                self.set_ward_dd.insertItem(self.set_ward_dd.count()-1, ward.name)
        else:
            # eID is None-type. So let's clear 
            self.set_name_edit.setText( "" )
            self.set_desc_edit.setText( "" )
            self.set_clear_ward_info()

    def set_ward_edit_button( self ):
        """
        Called when the 'ward edit' button is clicked 
        """
        if self.parent.entity_control.selected is None:
            print("nothing selected")
            return
        if not isinstance( self.parent.main_map.eid_catalogue[self.parent.entity_control.selected], Town):
            print("got entity type {}, expected {}".format(type(self.parent.main_map.eid_catalogue[self.parent.entity_control.selected]), Town) )
            return
        self.ward_accept = False

        setting = self.set_ward_dd.currentIndex()
        # 0 is whole city
        # 1 is city center
        # last is for a new ward
        if (setting+1)==self.set_ward_dd.count():
            setting = -1
            new_ward = Town("New Ward", is_ward=True)
            dialog = ward_dialog( self.parent, new_ward, setting )
        else:
            dialog = ward_dialog( self.parent, self.parent.main_map.eid_catalogue[ self.parent.entity_control.selected ], setting )
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()

        if setting==-1 and (new_ward is not None):
            self.parent.main_map.eid_catalogue[self.parent.entity_control.selected].add_ward( new_ward )

        #update! 
        self.set_update_selection( self.parent.entity_control.selected )

        # redraw the hex ( the icon may have changed )
        self.parent.entity_control.redraw_entities_at_hex( self.parent.main_map.eid_catalogue[self.parent.entity_control.selected].location ) 

    def set_update_ward_info(self, eID, ward = None):
        """
        For the settlement page. Updates the ward section in the GUI with the specified ward.
        """
        assert( isinstance( eID, int))
        
        this_city = self.parent.main_map.eid_catalogue[eID]

        # if no ward is specified, update the ward info with the town's overall values 
        if ward is None:
            self.set_name_view.setText( this_city.name )
            self.set_pop_disp.setText( str(this_city.population))
            self.set_weal_disp.setText( str(this_city.wealth) )
            self.set_demo_view.setPlainText("A City")
        else:
            assert( isinstance( ward, int))
            # 0 - city center
            # > 0 - some ward...
            if ward==0:
                self.set_name_view.setText( "City Center")
                self.set_pop_disp.setText( str(this_city.partial_population ))
                self.set_weal_disp.setText( str(this_city.partial_wealth))
                self.set_demo_view.setPlainText( this_city.get_demographics_as_str() )
            else:
                self.set_name_view.setText( this_city.wards[ward-1].name )
                self.set_pop_disp.setText( str(this_city.wards[ward-1].population ))
                self.set_weal_disp.setText( str(this_city.wards[ward-1].wealth))
                self.set_demo_view.setPlainText( this_city.wards[ward-1].get_demographics_as_str() )



    def set_clear_ward_info(self):
        self.set_name_view.setText("")
        self.set_pop_disp.setText("")
        self.set_weal_disp.setText("")
        self.set_demo_view.setText("")

    def loc_update_name_text(self, eID):
        """
        Should be called when a new location is selected. Writes the name and description
        """
        self.loc_name_edit.setText( self.parent.main_map.eid_catalogue[ eID ].name)
        self.loc_desc_edit.setText( self.parent.main_map.eid_catalogue[ eID ].description)
        
        temp_index = self.loc_icon.findText( self.parent.main_map.eid_catalogue[eID].icon )
        if temp_index >= 0:
            self.loc_icon.setCurrentIndex( temp_index )


    def loc_update_selection(self, HexID=None):
        """
        Updates the location menu gui with the proper information for the specified Hex. Adds the list of entities there
        """
        self.status_label.setText("...")
        self.loc_name_edit.setText( "" )
        self.loc_desc_edit.setText( "" )

        # clear out the list no matter what
        self.loc_list_entry.clear()
        if HexID is not None:
            # write out a list of all the entities at the selected Hex
            try:
                for eID in self.parent.main_map.eid_map[ HexID ]:
                    self.loc_list_entry.appendRow( QEntityItem(self.parent.main_map.eid_catalogue[eID].name , eID))
            except KeyError:
                # there are no entities here
                pass


    def loc_delete_func(self):
        """
        Called when the delete button is pressed in the locations tab
        """
        if self.parent.entity_control.selected is not None:
            loc_id = self.parent.main_map.eid_catalogue[ self.parent.entity_control.selected ].location
            self.parent.main_map.remove_entity( self.parent.entity_control.selected )
            
            # this deletes the old drawing 
            try:
                self.parent.entity_control.draw_entity( self.parent.entity_control.selected )
            except ValueError:
                # this means that the entity was never drawn. That's okay. Just pass it...
                pass 

            # redraw the entities here in case we now have a more prominent thing to draw  
            self.parent.entity_control.redraw_entities_at_hex( loc_id )
            self.parent.entity_control.update_wrt_new_hex()
            self.status_label.setText("deleted")
    
    def loc_save_entity(self):
        if self.parent.entity_control.selected is not None:
            self.parent.main_map.eid_catalogue[ self.parent.entity_control.selected ].name = self.loc_name_edit.text()
            self.parent.main_map.eid_catalogue[ self.parent.entity_control.selected ].description = self.loc_desc_edit.toPlainText()
            self.parent.main_map.eid_catalogue[ self.parent.entity_control.selected ].icon = self.loc_icon.currentText()
            self.parent.entity_control.update_wrt_new_hex()
            self.parent.entity_control.redraw_entities_at_hex( self.parent.entity_control.selected_hex )
            self.status_label.setText("saved")

    def loc_list_item_clicked( self , index):
        item = self.loc_list_entry.itemFromIndex(index)
        
        # select the new entity and update the name/description
        self.parent.entity_control.select_entity( item.eID )
        if isinstance( self.parent.main_map.eid_catalogue[ item.eID ], Town):
            self.parent.ui.contextPane.setCurrentIndex( 1 )
            self.set_update_selection( item.eID )
        else:
            self.loc_update_name_text( item.eID )


    def new_location_button_toolbar(self):
        """
        Called by a GUI button. Drops any active tool, swaps to the entity control, changes to the proper toolBox page, and prepares to create a new Location
        """
        self.parent.ui.contextPane.setCurrentIndex( 0 )
        self.parent.scene.select(self.parent.entity_control )
        self.parent.entity_control.prep_new(0)
    def new_settlement_button_toolbar(self):
        """
        Called by a GUI button. Drops any active tool, swaps to the entity control, changes to the Settlement page, and prepares to create a new town. 
        """
        self.parent.ui.contextPane.setCurrentIndex( 1 )
        self.parent.scene.select(self.parent.entity_control )
        self.parent.entity_control.prep_new(1)
    def new_road_button_toolbar(self):
        self.parent.ui.contextPane.setCurrentIndex( 2 )
        self.parent.scene.select(self.parent.path_control)
        self.parent.path_control.prepare(1)

    def new_county_button_toolbar(self):
        self.parent.ui.contextPane.setCurrentIndex( 3 )
        self.parent.scene.select(self.parent.county_control)
        self.parent.county_control.set_state( 1 )

    def entity_selector_toolbar(self):
        """
        Ensures that the entity brush is active. Drops whatever brush used to be selected and selects this one! 
        """
        self.parent.ui.contextPane.setCurrentIndex( 0 )
        self.parent.scene.select(self.parent.entity_control)

    def county_color_click(self):
        if self.parent.county_control.selected is None:
            pass
        else:
            old_one = self.parent.main_map.rid_catalogue[self.parent.county_control.r_layer][self.parent.county_control.selected].color
            qt_old_one = QtGui.QColor(old_one[0], old_one[1], old_one[2])
            new_color = QColorDialog.getColor(initial = qt_old_one, parent=self.parent)

            if new_color.isValid():
                self.parent.main_map.rid_catalogue[self.parent.county_control.r_layer][self.parent.county_control.selected].color = (new_color.red(), new_color.green(), new_color.blue())
                self.parent.county_control.redraw_region(self.parent.county_control.selected)

    def county_selector_toolbar(self):
        self.parent.ui.contextPane.setCurrentIndex(3)
        self.parent.scene.select(self.parent.county_control)
        self.parent.county_control.set_state( 0 )

    def county_update_with_selected(self):
        this_rid = self.parent.county_control.selected
        self.county_list_entry.clear()

        if this_rid is None:
            self.count_name_edit.setText( '')
            self.count_pop_disp.setText( '')
            self.count_weal_disp.setText( '' )
            self.label_13.setText( '' )

            # update and disable sliders
            self.horizontalSlider.setValue(0)
            self.horizontalSlider_2.setValue(0)
            self.horizontalSlider_3.setValue(0)
            self.horizontalSlider.setEnabled(False)
            self.horizontalSlider_2.setEnabled(False)
            self.horizontalSlider_3.setEnabled(False)

        else:
            this_county = self.parent.main_map.rid_catalogue[ 'county' ][this_rid]
        
            self.count_name_edit.setText( this_county.name )
            self.count_pop_disp.setText( str(this_county.population ))
            self.count_weal_disp.setText( str(this_county.wealth ))
            if this_county.population==0:
                self.label_13.setText( "NaN" )
            else:
                self.label_13.setText( '{:06.2f}'.format(float(this_county.wealth)/this_county.population) )

            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider_2.setEnabled(True)
            self.horizontalSlider_3.setEnabled(True)
            self.horizontalSlider.setValue(this_county.order*100. )
            self.horizontalSlider_2.setValue(this_county.war*100. )
            self.horizontalSlider_3.setValue(this_county.spirit*100. )
            
            if this_county.nation is None:
                self.count_king_button.setText("Create New Kingdom")
            else:
                self.count_king_button.setText("Edit Kingdom")

            for eID in self.parent.main_map.rid_catalogue['county'][this_rid].eIDs:
                if isinstance( self.parent.main_map.eid_catalogue[eID], Town):
                    self.county_list_entry.appendRow( QEntityItem(self.parent.main_map.eid_catalogue[eID].name , eID))
                        
            self.parent.county_control.redraw_region( this_rid )

    def county_apply(self):
        this_rid = self.parent.county_control.selected

        if this_rid is None:
            return
        else:
            this_county = self.parent.main_map.rid_catalogue[ 'county' ][this_rid]
            
            this_county.name = self.count_name_edit.text()
            this_county.set_order(float(self.horizontalSlider.value())/100. )
            this_county.set_war(float(self.horizontalSlider_2.value())/100.)
            this_county.set_spirit(float(self.horizontalSlider_3.value())/100. )

            self.county_update_with_selected()

    def county_list_item_clicked(self, index):
        item = self.county_list_entry.itemFromIndex(index)
        self.parent.entity_control.select_entity( item.eID )
        self.parent.ui.contextPane.setCurrentIndex( 1 )
        self.set_update_selection( item.eID )

        self.parent.scene.select(self.entity_control)

    def county_kingdom_button(self):
        this_rid = self.parent.county_control.selected

        if this_rid is None:
            pass
        else:
            this_county = self.parent.main_map.rid_catalogue['county'][this_rid]
            if this_county.nation is None:
                new_nation = Nation(self.parent.main_map, this_rid)
                self.parent.nation_control.select( new_nation )
            else:
                self.parent.nation_control.select( this_county.nation )
            
            self.nation_update_gui()

            self.parent.scene.select(self.parent.nation_control)
            self.parent.ui.contextPane.setCurrentIndex(4)

    def nation_list_item_clicked(self, index):
        item = self.nation_list_entry.itemFromIndex(index)
        this_county = item.eID

        self.parent.county_control.select( item.eID )
        self.parent.ui.contextPane.setCurrentIndex(3)
        self.county_update_with_selected()

        self.parent.scene.select( self.parent.county_control)

    def nation_update_gui(self):
        self.parent.ui.contextPane.setCurrentIndex(4)
        self.nation_list_entry.clear()
        this_nation = self.parent.nation_control.selected

        if this_nation is None:
            self.king_name_edit.setText("")
            self.king_subj_disp.setText("")
            self.king_weal_disp.setText("")
            self.king_gdg_disp.setText("")

            self.king_war_sld.setValue(0)
            self.king_war_sld.setEnabled(False)
            self.king_order_sld.setValue(0)
            self.king_order_sld.setEnabled(False)
            self.king_spirit_sld.setValue(0)
            self.king_spirit_sld.setEnabled(False)

        else:
            self.king_name_edit.setText( this_nation.name )
            self.king_subj_disp.setText( str(this_nation.subjects) )
            self.king_weal_disp.setText( str(this_nation.total_wealth) )
            if this_nation.subjects==0:
                self.king_gdg_disp.setText( "NaN" )
            else:
                self.king_gdg_disp.setText( '{:06.2f}'.format(float(this_nation.total_wealth)/this_nation.subjects) )
            for rID in self.parent.nation_control.selected.counties:
                self.nation_list_entry.appendRow( QEntityItem(self.parent.main_map.rid_catalogue['county'][rID].name, rID ))

            self.king_war_sld.setEnabled(True)
            self.king_order_sld.setEnabled(True)
            self.king_spirit_sld.setEnabled(True)
            self.king_war_sld.setValue(this_nation.war*100)
            self.king_order_sld.setValue(this_nation.order*100)
            self.king_spirit_sld.setValue(this_nation.spirit*100)

        self.update_state()

    def update_state(self):
        
        the_state =self.parent.nation_control._state
        if the_state == 0:
            self.king_state.setText('...')
        elif the_state==1:
            self.king_state.setText('Creating Kingdom')
        elif the_state==2:
            self.king_state.setText('Adding to Kingdom')
        elif the_state==3:
            self.king_state.setText('Removing From Kingdom')

    def nation_add_to(self):
        self.parent.scene.select(self.parent.nation_control)
        if self.parent.nation_control.selected is not None:
            self.parent.nation_control.set_state(2)
        self.update_state()

    def nation_remove_from(self):
        self.parent.scene.select(self.parent.nation_control)
        if self.parent.nation_control.selected is not None:
            self.parent.nation_control.set_state(3)
        self.update_state()

    def nation_apply_button(self):
        this_nation = self.parent.nation_control.selected

        if this_nation is None:
            pass
        else:
            this_nation.name = self.king_name_edit.text()
            this_nation.set_war( float(self.king_war_sld.value())/100 )
            this_nation.set_order( float(self.king_order_sld.value())/100 )
            this_nation.set_spirit( float(self.king_spirit_sld.value())/100 )

    def nation_dissolve(self):
        pass


class ward_dialog(QDialog):
    def __init__(self,parent, which, setting):
        """
        which - which ward is being edited
        setting - specifies what exactly is being done. 
                     -1 the new town-like object 
                     0 whole city
                     1 city center 
                     higher numbers for wards
                   
        """

        #for some reason, the accept function is called twice.... 
        self._done = False

        super(ward_dialog, self).__init__(parent)
        self.ui = ward_ui()
        self.ui.setupUi(self)
        self.ui.accept_reject.accepted.connect( self.accept )
        self.ui.accept_reject.rejected.connect( self.reject )
        self.setting = setting

        if setting==0 or setting==-1 or setting==1:
            self.editing_ward = which
        else:            
            self.editing_ward = which.wards[ setting -2 ]

        if setting==1:
            self.ui.name_edit.setText( "City Center" )
            self.ui.pop_value.setText( str( self.editing_ward.partial_population ))
            self.ui.pop_edit.setText( str(self.editing_ward.partial_population ))
            self.ui.wealth_value.setText( str( self.editing_ward.partial_wealth ))
            self.ui.wealth_edit.setText(str( self.editing_ward.partial_wealth ))
        else:
            self.ui.name_edit.setText( self.editing_ward.name )
            self.ui.pop_value.setText( str( self.editing_ward.population ))
            self.ui.pop_edit.setText( str(self.editing_ward.population ))
            self.ui.wealth_value.setText( str( self.editing_ward.wealth ))
            self.ui.wealth_edit.setText(str( self.editing_ward.wealth ))

        self.ui.walled_chck.setChecked( self.editing_ward.walled ) 
        self.ui.order_slider.setValue(100*self.editing_ward.order)
        self.ui.spirit_slider.setValue(100*self.editing_ward.spirit)
        self.ui.war_slider.setValue(100*self.editing_ward.war)

        #currentIndexChanged.conect
        self.ui.pop_dropdown.currentIndexChanged.connect( self.set_population )
        self.ui.wealth_dropdown.currentIndexChanged.connect( self.set_wealth )
        # 2 - order; 3 - war; 4 - spirit

        if setting==0:
            # restrict some parts that can't be edited for the whole
            #self.ui.checkBox.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
            self.ui.demo_edit.setEnabled(False)
            self.ui.order_slider.setEnabled(False)
            self.ui.war_slider.setEnabled(False)
            self.ui.spirit_slider.setEnabled(False)
            self.ui.walled_chck.setEnabled(False)
        else:
            # set the things
            new_text = "# Use \"+\" to start a new category\n# And write entries as \"<type>:<value>\"\n #Categories will be auto-normalized\n\n"+ self.editing_ward.get_demographics_as_str()
            self.ui.demo_edit.setPlainText(new_text)

        self.ui.wealth_edit.setEnabled(False)
        self.ui.pop_edit.setEnabled(False)


    def set_wealth(self, index):
        # writes the wealth after changing the dropdown menu
        #  0 is keep at, 1 is set to, 2 is add to
        if index==0:
            self.ui.wealth_edit.setText("")
            self.ui.wealth_edit.setEnabled(False)
        elif index==1:
            self.ui.wealth_edit.setEnabled(True)
            if self.setting==1:
                self.ui.wealth_edit.setText( str(self.editing_ward.partial_wealth) )
            else:
                self.ui.wealth_edit.setText( str(self.editing_ward.wealth) )
        else:
            self.ui.wealth_edit.setEnabled(True)
            self.ui.wealth_edit.setText( "0" )
            
    def set_population(self, index):
        # writes the population after changing the dropdown menu
        #  0 is keep at, 1 is set to, 2 is add to
        if index==0:
            self.ui.pop_edit.setText("")
            self.ui.pop_edit.setEnabled(False)
        elif index==1:
            self.ui.pop_edit.setEnabled(True)
            if self.setting==1:
                self.ui.pop_edit.setText( str(self.editing_ward.partial_population ))
            else:
                self.ui.pop_edit.setText( str( self.editing_ward.population ))
        else:
            self.ui.pop_edit.setEnabled(True)
            self.ui.pop_edit.setText("0")

    def accept(self):
        """
        Called when the 'okay' option is selected. For some reason it gets called twice though... 
        """

        if self._done:
            return
        else:
            self._done = True

        #which.walled = walled_chck.state()  <-- not sure about this syntax
        self.editing_ward.walled = self.ui.walled_chck.isChecked()
        if not self.setting==1:
            self.editing_ward.name = self.ui.name_edit.text()
       
        if self.setting!=0:
            self.editing_ward.set_war( self.ui.war_slider.value()/100. )
            self.editing_ward.set_order( self.ui.order_slider.value()/100. )
            self.editing_ward.set_spirit( self.ui.spirit_slider.value()/100. )


        if self.setting==0: 
            passed_demo = None
        else:
            try:
                if self.ui.demo_edit.toPlainText()=="":
                    passed_demo = None
                else:
                    self.ui.demo_edit.update()
                    passed_demo = parse_demographic( self.ui.demo_edit.toPlainText() )
            except ValueError:
                print("Error parsing demographic text block")
                self.reject()

        if self.setting==0:
            which_ward = None
        elif self.setting ==  -1:
            which_ward = None
        else:
            which_ward = self.setting - 1

        # how to change the population
        if self.ui.pop_dropdown.currentIndex() == 0: # keep 
            pass
        elif self.ui.pop_dropdown.currentIndex() == 1:
            self.editing_ward.set_population(int( self.ui.pop_edit.text() ), which_ward = which_ward)
        else:
            self.editing_ward.add_population(int( self.ui.pop_edit.text() ), which_ward = which_ward, demographics=passed_demo)
        
        if self.ui.wealth_dropdown.currentIndex() == 0:
            pass
        elif self.ui.wealth_dropdown.currentIndex() == 1:
            self.editing_ward.set_wealth( int( self.ui.wealth_edit.text()), which_ward = which_ward)
        else: 
            self.editing_ward.add_wealth( int( self.ui.wealth_edit.text()), which_ward = which_ward)

        if (self.ui.comboBox.currentIndex()==0) and (passed_demo is not None):
            self.editing_ward.set_demographics( passed_demo )

        self.editing_ward.update_icon()
        super( ward_dialog, self).accept()

    def reject(self):
        if self.setting==-1:
            which = None
        super(ward_dialog, self).reject()

def parse_demographic( text ):
    """
    This parses the text in the demographic box. It ignores lines with a comment character: #. 
    
    It builds a dictionary assuming that the user prepares the data like 
        key : value
    and it ignores whitespace. If it fails, it raises a ValueError 
    """

    # add an EOL character at the end
    text = text + '\n'

    lines = []
    line = ""
    ignore = False
    for char in text:
        # at an end of line character we append what we have and start reading again
        if char == '\n':
            stripped = "".join( line.split(" ") )
            if stripped!="":
                lines.append( stripped )
                line = ""
            ignore = False
            continue

        # if we hit a comment character, ignore the rest of the line 
        if char =="#":
            ignore = True
            continue

        if ignore:
            continue

        line = line + char 
    
    # parse the lines intoa dictionary 
    new_dict = {}
    key = ""
    for line in lines:
        if line[0]=='+':
            # new key
            key = line[1:]
            if key not in new_dict:
                new_dict[key] = {}
            continue
        else:
            if key=="":
                raise ValueError("Bad Formatting.")

            split = line.split(":")
            if len(split)!=2:
                # this means there aren't the right number of ":" in the line
                raise ValueError("Bad formatting")
            # make it lower case to avoid case-sensitivity 
            subkey = split[0].lower()
            # will raise ValueError if this is not a number 
            value = float(split[1])

            new_dict[key][subkey]=value
    
    # normalize the built dictionary
    for key in new_dict:
        total = 0
        for subkey in new_dict[key]:
            total += new_dict[key][subkey]
        # divide each value by the sum of the values
        for subkey in new_dict[key]:
            new_dict[key][subkey]/= float(total)

    return( new_dict )
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'civilization_design_file.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import os

art_dir = os.path.join( os.path.dirname(__file__), '..', '..','Artwork')

class editor_gui_window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1139, 847)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 800))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("hexes","draw_several.gif")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.ent_select_button_0 = QtWidgets.QToolButton(self.centralwidget)
        self.ent_select_button_0.setMinimumSize(QtCore.QSize(40, 40))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_location.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ent_select_button_0.setIcon(icon1)
        self.ent_select_button_0.setIconSize(QtCore.QSize(32, 32))
        self.ent_select_button_0.setObjectName("ent_select_button_0")
        self.verticalLayout.addWidget(self.ent_select_button_0)
        self.count_sel_button_1 = QtWidgets.QToolButton(self.centralwidget)
        self.count_sel_button_1.setMinimumSize(QtCore.QSize(40, 40))
        self.count_sel_button_1.setToolTip("")
        self.count_sel_button_1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_county.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.count_sel_button_1.setIcon(icon2)
        self.count_sel_button_1.setIconSize(QtCore.QSize(32, 32))
        self.count_sel_button_1.setObjectName("count_sel_button_1")
        self.verticalLayout.addWidget(self.count_sel_button_1)
        self.county_brush = QtWidgets.QToolButton(self.centralwidget)
        self.county_brush.setToolTip("")
        self.county_brush.setToolTipDuration(-1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "temp.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.county_brush.setIcon(icon3)
        self.county_brush.setIconSize(QtCore.QSize(32, 32))
        self.county_brush.setObjectName("county_brush")
        self.verticalLayout.addWidget(self.county_brush)
        self.hand_button_2 = QtWidgets.QToolButton(self.centralwidget)
        self.hand_button_2.setMinimumSize(QtCore.QSize(40, 40))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"hand.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hand_button_2.setIcon(icon4)
        self.hand_button_2.setIconSize(QtCore.QSize(32, 32))
        self.hand_button_2.setObjectName("hand_button_2")
        self.verticalLayout.addWidget(self.hand_button_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.loc_button_1 = QtWidgets.QToolButton(self.centralwidget)
        self.loc_button_1.setMinimumSize(QtCore.QSize(40, 40))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "new_location.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loc_button_1.setIcon(icon5)
        self.loc_button_1.setIconSize(QtCore.QSize(32, 32))
        self.loc_button_1.setObjectName("loc_button_1")
        self.verticalLayout.addWidget(self.loc_button_1)
        self.setl_button_2 = QtWidgets.QToolButton(self.centralwidget)
        self.setl_button_2.setMinimumSize(QtCore.QSize(40, 40))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "new_settle.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setl_button_2.setIcon(icon6)
        self.setl_button_2.setIconSize(QtCore.QSize(32, 32))
        self.setl_button_2.setObjectName("setl_button_2")
        self.verticalLayout.addWidget(self.setl_button_2)
        self.road_button_3 = QtWidgets.QToolButton(self.centralwidget)
        self.road_button_3.setMinimumSize(QtCore.QSize(40, 40))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(os.path.join( art_dir, "new_road.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.road_button_3.setIcon(icon7)
        self.road_button_3.setIconSize(QtCore.QSize(32, 32))
        self.road_button_3.setObjectName("road_button_3")
        self.verticalLayout.addWidget(self.road_button_3)
        self.count_button_4 = QtWidgets.QToolButton(self.centralwidget)
        self.count_button_4.setMinimumSize(QtCore.QSize(40, 40))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(os.path.join(art_dir, "county.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.count_button_4.setIcon(icon8)
        self.count_button_4.setIconSize(QtCore.QSize(32, 32))
        self.count_button_4.setObjectName("count_button_4")
        self.verticalLayout.addWidget(self.count_button_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setMinimumSize(QtCore.QSize(250, 0 ))
        self.toolBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.toolBox.setObjectName("toolBox")
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
        self.loc_save = QtWidgets.QPushButton(self.Locations)
        self.loc_save.setObjectName("loc_save")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.loc_save)
        self.status_label = QtWidgets.QLabel(self.Locations)
        self.status_label.setMinimumSize(QtCore.QSize(80, 0))
        self.status_label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.status_label.setFrameShape(QtWidgets.QFrame.Box)
        self.status_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.status_label)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_3.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem3)
        self.loc_list_view = QtWidgets.QListView(self.Locations)
        self.loc_list_view.setObjectName("loc_list_view")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.loc_list_view)
        self.loc_deselect = QtWidgets.QPushButton(self.Locations)
        self.loc_deselect.setObjectName("loc_deselect")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.loc_deselect)
        self.loc_delete = QtWidgets.QPushButton(self.Locations)
        self.loc_delete.setObjectName("loc_delete")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.loc_delete)
        self.toolBox.addItem(self.Locations, "")
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
        self.toolBox.addItem(self.Settlements, "")
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
        self.toolBox.addItem(self.Roads, "")
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
        self.pushButton = QtWidgets.QPushButton(self.Counties)
        self.pushButton.setObjectName("pushButton")
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.pushButton)
        self.count_king_button = QtWidgets.QPushButton(self.Counties)
        self.count_king_button.setObjectName("count_king_button")
        self.formLayout_4.setWidget(11, QtWidgets.QFormLayout.SpanningRole, self.count_king_button)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_4.setItem(10, QtWidgets.QFormLayout.LabelRole, spacerItem5)
        self.label_12 = QtWidgets.QLabel(self.Counties)
        self.label_12.setObjectName("label_12")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtWidgets.QLabel(self.Counties)
        self.label_13.setFrameShape(QtWidgets.QFrame.Box)
        self.label_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_13)
        self.toolBox.addItem(self.Counties, "")

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
        self.toolBox.addItem(self.Kingdoms, "")
        self.horizontalLayout.addWidget(self.toolBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1139, 22))
        self.menubar.setObjectName("menubar")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionBiome_Borders = QtWidgets.QAction(MainWindow)
        self.actionBiome_Borders.setCheckable(True)
        self.actionBiome_Borders.setObjectName("actionBiome_Borders")
        self.actionCounty_Borders = QtWidgets.QAction(MainWindow)
        self.actionCounty_Borders.setCheckable(True)
        self.actionCounty_Borders.setChecked(True)
        self.actionCounty_Borders.setObjectName("actionCounty_Borders")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
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
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout_MultiHex)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ent_select_button_0.setText(_translate("MainWindow", "..."))
        self.county_brush.setText(_translate("MainWindow", "..."))
        self.hand_button_2.setText(_translate("MainWindow", "..."))
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
        self.toolBox.setItemText(self.toolBox.indexOf(self.Locations), _translate("MainWindow", "Locations"))
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
        self.toolBox.setItemText(self.toolBox.indexOf(self.Settlements), _translate("MainWindow", "Settlements"))
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
        self.toolBox.setItemText(self.toolBox.indexOf(self.Roads), _translate("MainWindow", "Roads"))
        self.count_name_lbl.setText(_translate("MainWindow", "Name:"))
        self.count_pop_disp_2.setText(_translate("MainWindow", "Population:"))
        self.count_weal_lbl.setText(_translate("MainWindow", "Wealth:"))
        self.count_city_lbl.setText(_translate("MainWindow", "\n"
"Contained Cities:"))
        self.label_2.setText(_translate("MainWindow", "Order: "))
        self.label_3.setText(_translate("MainWindow", "War: "))
        self.label_4.setText(_translate("MainWindow", "Spirit: "))
        self.pushButton.setText(_translate("MainWindow", "Apply"))
        self.count_king_button.setText(_translate("MainWindow", "Create New Kingdom"))
        self.label_12.setText(_translate("MainWindow", "GDG: "))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Counties), _translate("MainWindow", "Counties"))
        self.king_name_lbl.setText(_translate("MainWindow", "Name: "))
        self.king_subj_lbl.setText(_translate("MainWindow", "Subjects: "))
        self.king_weal_lbl.setText(_translate("MainWindow", "Wealth: "))
        self.label_11.setText(_translate("MainWindow", "\n"
"Counties:"))
        self.king_count_new_but.setText(_translate("MainWindow", "Add New"))
        self.king_count_rem_but.setText(_translate("MainWindow", "Remove"))
        self.king_apply.setText(_translate("MainWindow","Apply"))
        self.king_dissolve_but.setText(_translate("MainWindow", "Dissolve"))
        self.king_gdg_lbl.setText(_translate("MainWindow", "GDG: "))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Kingdoms), _translate("MainWindow", "Kingoms"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionBiome_Borders.setText(_translate("MainWindow", "Biome Borders"))
        self.actionCounty_Borders.setText(_translate("MainWindow", "County Borders"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
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



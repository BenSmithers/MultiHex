# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'terrain_editor_2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1109, 815)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tool_hex_select = QtWidgets.QToolButton(self.centralwidget)
        self.tool_hex_select.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_hex_select.setObjectName("tool_hex_select")
        self.verticalLayout.addWidget(self.tool_hex_select)
        self.tool_detail = QtWidgets.QToolButton(self.centralwidget)
        self.tool_detail.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_detail.setObjectName("tool_detail")
        self.verticalLayout.addWidget(self.tool_detail)
        self.tool_hex_brush = QtWidgets.QToolButton(self.centralwidget)
        self.tool_hex_brush.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_hex_brush.setObjectName("tool_hex_brush")
        self.verticalLayout.addWidget(self.tool_hex_brush)
        self.tool_riv_but = QtWidgets.QToolButton(self.centralwidget)
        self.tool_riv_but.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_riv_but.setObjectName("tool_riv_but")
        self.verticalLayout.addWidget(self.tool_riv_but)
        self.tool_biome_but = QtWidgets.QToolButton(self.centralwidget)
        self.tool_biome_but.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_biome_but.setObjectName("tool_biome_but")
        self.verticalLayout.addWidget(self.tool_biome_but)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.toolBox.setObjectName("toolBox")
        self.Detaoer = QtWidgets.QWidget()
        self.Detaoer.setGeometry(QtCore.QRect(0, 0, 250, 629))
        self.Detaoer.setObjectName("Detaoer")
        self.formLayout_4 = QtWidgets.QFormLayout(self.Detaoer)
        self.formLayout_4.setObjectName("formLayout_4")
        self.det_noise_combo = QtWidgets.QComboBox(self.Detaoer)
        self.det_noise_combo.setObjectName("det_noise_combo")
        self.det_noise_combo.addItem("")
        self.det_noise_combo.addItem("")
        self.det_noise_combo.addItem("")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.det_noise_combo)
        self.det_edit_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_edit_lbl.setObjectName("det_edit_lbl")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.det_edit_lbl)
        self.det_brush_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_brush_lbl.setObjectName("det_brush_lbl")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.det_brush_lbl)
        self.det_Brush_spin = QtWidgets.QSpinBox(self.Detaoer)
        self.det_Brush_spin.setMinimum(1)
        self.det_Brush_spin.setMaximum(3)
        self.det_Brush_spin.setObjectName("det_Brush_spin")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.det_Brush_spin)
        self.det_mag_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_mag_lbl.setObjectName("det_mag_lbl")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.det_mag_lbl)
        self.det_mag_spin = QtWidgets.QDoubleSpinBox(self.Detaoer)
        self.det_mag_spin.setMinimum(0.1)
        self.det_mag_spin.setMaximum(2.0)
        self.det_mag_spin.setSingleStep(0.05)
        self.det_mag_spin.setObjectName("det_mag_spin")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.det_mag_spin)
        self.det_but_noise = QtWidgets.QPushButton(self.Detaoer)
        self.det_but_noise.setObjectName("det_but_noise")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.det_but_noise)
        self.det_but_color = QtWidgets.QPushButton(self.Detaoer)
        self.det_but_color.setObjectName("det_but_color")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.det_but_color)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_4.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        self.det_hexid_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_hexid_lbl.setObjectName("det_hexid_lbl")
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.det_hexid_lbl)
        self.det_hexid_disp = QtWidgets.QLCDNumber(self.Detaoer)
        self.det_hexid_disp.setObjectName("det_hexid_disp")
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.det_hexid_disp)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_4.setItem(12, QtWidgets.QFormLayout.FieldRole, spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_4.setItem(7, QtWidgets.QFormLayout.FieldRole, spacerItem4)
        self.det_alt_slide = QtWidgets.QSlider(self.Detaoer)
        self.det_alt_slide.setOrientation(QtCore.Qt.Horizontal)
        self.det_alt_slide.setObjectName("det_alt_slide")
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.det_alt_slide)
        self.det_temp_slide = QtWidgets.QSlider(self.Detaoer)
        self.det_temp_slide.setOrientation(QtCore.Qt.Horizontal)
        self.det_temp_slide.setObjectName("det_temp_slide")
        self.formLayout_4.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.det_temp_slide)
        self.det_rain_slide = QtWidgets.QSlider(self.Detaoer)
        self.det_rain_slide.setOrientation(QtCore.Qt.Horizontal)
        self.det_rain_slide.setObjectName("det_rain_slide")
        self.formLayout_4.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.det_rain_slide)
        self.det_alt_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_alt_lbl.setObjectName("det_alt_lbl")
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.det_alt_lbl)
        self.det_temp_slide_2 = QtWidgets.QLabel(self.Detaoer)
        self.det_temp_slide_2.setObjectName("det_temp_slide_2")
        self.formLayout_4.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.det_temp_slide_2)
        self.det_rain_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_rain_lbl.setObjectName("det_rain_lbl")
        self.formLayout_4.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.det_rain_lbl)
        self.toolBox.addItem(self.Detaoer, "")
        self.HexBrush = QtWidgets.QWidget()
        self.HexBrush.setGeometry(QtCore.QRect(0, 0, 250, 629))
        self.HexBrush.setObjectName("HexBrush")
        self.formLayout = QtWidgets.QFormLayout(self.HexBrush)
        self.formLayout.setObjectName("formLayout")
        self.hex_brush_lbl = QtWidgets.QLabel(self.HexBrush)
        self.hex_brush_lbl.setObjectName("hex_brush_lbl")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.hex_brush_lbl)
        self.hex_brush_disp = QtWidgets.QSpinBox(self.HexBrush)
        self.hex_brush_disp.setMinimum(1)
        self.hex_brush_disp.setMaximum(3)
        self.hex_brush_disp.setObjectName("hex_brush_disp")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.hex_brush_disp)
        self.hex_sub_list = QtWidgets.QListView(self.HexBrush)
        self.hex_sub_list.setObjectName("hex_sub_list")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.hex_sub_list)
        self.hex_select_lbl = QtWidgets.QLabel(self.HexBrush)
        self.hex_select_lbl.setObjectName("hex_select_lbl")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.hex_select_lbl)
        self.hex_select_disp = QtWidgets.QLabel(self.HexBrush)
        self.hex_select_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.hex_select_disp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hex_select_disp.setText("")
        self.hex_select_disp.setObjectName("hex_select_disp")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.hex_select_disp)
        self.hex_type_lbl = QtWidgets.QLabel(self.HexBrush)
        self.hex_type_lbl.setObjectName("hex_type_lbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.hex_type_lbl)
        self.hex_type_combo = QtWidgets.QComboBox(self.HexBrush)
        self.hex_type_combo.setObjectName("hex_type_combo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hex_type_combo)
        self.hex_subtype_lbl = QtWidgets.QLabel(self.HexBrush)
        self.hex_subtype_lbl.setObjectName("hex_subtype_lbl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.hex_subtype_lbl)
        self.toolBox.addItem(self.HexBrush, "")
        self.RiverPen = QtWidgets.QWidget()
        self.RiverPen.setGeometry(QtCore.QRect(0, 0, 250, 629))
        self.RiverPen.setObjectName("RiverPen")
        self.formLayout_2 = QtWidgets.QFormLayout(self.RiverPen)
        self.formLayout_2.setObjectName("formLayout_2")
        self.river_label = QtWidgets.QLabel(self.RiverPen)
        self.river_label.setObjectName("river_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.river_label)
        self.river_list = QtWidgets.QListView(self.RiverPen)
        self.river_list.setObjectName("river_list")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.river_list)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.riv_but_pstart = QtWidgets.QPushButton(self.RiverPen)
        self.riv_but_pstart.setObjectName("riv_but_pstart")
        self.gridLayout_2.addWidget(self.riv_but_pstart, 0, 0, 1, 1)
        self.riv_but_pend = QtWidgets.QPushButton(self.RiverPen)
        self.riv_but_pend.setObjectName("riv_but_pend")
        self.gridLayout_2.addWidget(self.riv_but_pend, 0, 1, 1, 1)
        self.riv_but_astart = QtWidgets.QPushButton(self.RiverPen)
        self.riv_but_astart.setObjectName("riv_but_astart")
        self.gridLayout_2.addWidget(self.riv_but_astart, 1, 0, 1, 1)
        self.riv_but_aend = QtWidgets.QPushButton(self.RiverPen)
        self.riv_but_aend.setObjectName("riv_but_aend")
        self.gridLayout_2.addWidget(self.riv_but_aend, 1, 1, 1, 1)
        self.formLayout_2.setLayout(5, QtWidgets.QFormLayout.SpanningRole, self.gridLayout_2)
        self.river_trib = QtWidgets.QLabel(self.RiverPen)
        self.river_trib.setObjectName("river_trib")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.river_trib)
        self.river_trib_list = QtWidgets.QListView(self.RiverPen)
        self.river_trib_list.setMaximumSize(QtCore.QSize(16777215, 75))
        self.river_trib_list.setObjectName("river_trib_list")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.river_trib_list)
        self.riv_but_delete = QtWidgets.QPushButton(self.RiverPen)
        self.riv_but_delete.setObjectName("riv_but_delete")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.riv_but_delete)
        self.riv_name_lbl = QtWidgets.QLabel(self.RiverPen)
        self.riv_name_lbl.setObjectName("riv_name_lbl")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.riv_name_lbl)
        self.river_name_disp = QtWidgets.QLabel(self.RiverPen)
        self.river_name_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.river_name_disp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.river_name_disp.setText("")
        self.river_name_disp.setObjectName("river_name_disp")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.river_name_disp)
        self.toolBox.addItem(self.RiverPen, "")
        self.BiomePainter = QtWidgets.QWidget()
        self.BiomePainter.setGeometry(QtCore.QRect(0, 0, 250, 629))
        self.BiomePainter.setObjectName("BiomePainter")
        self.formLayout_3 = QtWidgets.QFormLayout(self.BiomePainter)
        self.formLayout_3.setObjectName("formLayout_3")
        self.bio_name_disp = QtWidgets.QLabel(self.BiomePainter)
        self.bio_name_disp.setObjectName("bio_name_disp")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.bio_name_disp)
        self.bio_name_edit = QtWidgets.QLineEdit(self.BiomePainter)
        self.bio_name_edit.setObjectName("bio_name_edit")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.bio_name_edit)
        self.bio_color_lbl = QtWidgets.QLabel(self.BiomePainter)
        self.bio_color_lbl.setObjectName("bio_color_lbl")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.bio_color_lbl)
        self.bio_color_combo = QtWidgets.QComboBox(self.BiomePainter)
        self.bio_color_combo.setObjectName("bio_color_combo")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.bio_color_combo)
        self.bio_name_but_gen = QtWidgets.QPushButton(self.BiomePainter)
        self.bio_name_but_gen.setObjectName("bio_name_but_gen")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.bio_name_but_gen)
        self.biome_but_apply = QtWidgets.QPushButton(self.BiomePainter)
        self.biome_but_apply.setObjectName("biome_but_apply")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.biome_but_apply)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_3.setItem(7, QtWidgets.QFormLayout.FieldRole, spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_3.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem6)
        self.toolBox.addItem(self.BiomePainter, "")
        self.horizontalLayout.addWidget(self.toolBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1109, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHeatmaps = QtWidgets.QMenu(self.menubar)
        self.menuHeatmaps.setObjectName("menuHeatmaps")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout_MultiHex = QtWidgets.QAction(MainWindow)
        self.actionAbout_MultiHex.setObjectName("actionAbout_MultiHex")
        self.actionTemperature = QtWidgets.QAction(MainWindow)
        self.actionTemperature.setCheckable(False)
        self.actionTemperature.setObjectName("actionTemperature")
        self.actionAltitude = QtWidgets.QAction(MainWindow)
        self.actionAltitude.setObjectName("actionAltitude")
        self.actionRainfall = QtWidgets.QAction(MainWindow)
        self.actionRainfall.setObjectName("actionRainfall")
        self.actionBiome_Names = QtWidgets.QAction(MainWindow)
        self.actionBiome_Names.setCheckable(True)
        self.actionBiome_Names.setObjectName("actionBiome_Names")
        self.actionBiome_Borders = QtWidgets.QAction(MainWindow)
        self.actionBiome_Borders.setCheckable(True)
        self.actionBiome_Borders.setObjectName("actionBiome_Borders")
        self.actionRivers = QtWidgets.QAction(MainWindow)
        self.actionRivers.setCheckable(True)
        self.actionRivers.setObjectName("actionRivers")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout_MultiHex)
        self.menuHeatmaps.addAction(self.actionAltitude)
        self.menuHeatmaps.addAction(self.actionRainfall)
        self.menuHeatmaps.addAction(self.actionTemperature)
        self.menuView.addAction(self.actionBiome_Names)
        self.menuView.addAction(self.actionBiome_Borders)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionRivers)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHeatmaps.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tool_hex_select.setToolTip(_translate("MainWindow", "Hex Selector"))
        self.tool_hex_select.setText(_translate("MainWindow", "..."))
        self.tool_detail.setToolTip(_translate("MainWindow", "Detailer"))
        self.tool_detail.setText(_translate("MainWindow", "..."))
        self.tool_hex_brush.setToolTip(_translate("MainWindow", "Hex Brush"))
        self.tool_hex_brush.setText(_translate("MainWindow", "..."))
        self.tool_riv_but.setToolTip(_translate("MainWindow", "Make New River"))
        self.tool_riv_but.setText(_translate("MainWindow", "..."))
        self.tool_biome_but.setToolTip(_translate("MainWindow", "Make New Biome"))
        self.tool_biome_but.setText(_translate("MainWindow", "..."))
        self.det_noise_combo.setItemText(0, _translate("MainWindow", "Altitude"))
        self.det_noise_combo.setItemText(1, _translate("MainWindow", "Rainfall"))
        self.det_noise_combo.setItemText(2, _translate("MainWindow", "Temperature"))
        self.det_edit_lbl.setText(_translate("MainWindow", "Editing:"))
        self.det_brush_lbl.setText(_translate("MainWindow", "Brush Size:"))
        self.det_mag_lbl.setText(_translate("MainWindow", "Magnitude:"))
        self.det_but_noise.setText(_translate("MainWindow", "Inject Noise"))
        self.det_but_color.setText(_translate("MainWindow", "Recalculate Color"))
        self.det_hexid_lbl.setText(_translate("MainWindow", "HexID"))
        self.det_alt_lbl.setText(_translate("MainWindow", "Altitude"))
        self.det_temp_slide_2.setText(_translate("MainWindow", "Temperature"))
        self.det_rain_lbl.setText(_translate("MainWindow", "Rainfall"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Detaoer), _translate("MainWindow", "Detailer"))
        self.hex_brush_lbl.setText(_translate("MainWindow", "Brush Size"))
        self.hex_select_lbl.setText(_translate("MainWindow", "Selected: "))
        self.hex_type_lbl.setText(_translate("MainWindow", "Type:"))
        self.hex_subtype_lbl.setText(_translate("MainWindow", "\n"
"Subtype:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.HexBrush), _translate("MainWindow", "Hex Brush"))
        self.river_label.setText(_translate("MainWindow", "Rivers:"))
        self.riv_but_pstart.setText(_translate("MainWindow", "Pop Start"))
        self.riv_but_pend.setText(_translate("MainWindow", "Pop End"))
        self.riv_but_astart.setText(_translate("MainWindow", "Add To Start"))
        self.riv_but_aend.setText(_translate("MainWindow", "Add To End"))
        self.river_trib.setText(_translate("MainWindow", "Tributaries:"))
        self.riv_but_delete.setText(_translate("MainWindow", "Delte River"))
        self.riv_name_lbl.setText(_translate("MainWindow", "Selected: "))
        self.toolBox.setItemText(self.toolBox.indexOf(self.RiverPen), _translate("MainWindow", "River Pen"))
        self.bio_name_disp.setText(_translate("MainWindow", "Biome:"))
        self.bio_color_lbl.setText(_translate("MainWindow", "Color:"))
        self.bio_name_but_gen.setText(_translate("MainWindow", "Generate Name"))
        self.biome_but_apply.setText(_translate("MainWindow", "Apply"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.BiomePainter), _translate("MainWindow", "Biome Painter"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuHeatmaps.setTitle(_translate("MainWindow", "Heatmaps"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout_MultiHex.setText(_translate("MainWindow", "About MultiHex"))
        self.actionTemperature.setText(_translate("MainWindow", "Temperature"))
        self.actionAltitude.setText(_translate("MainWindow", "Altitude"))
        self.actionRainfall.setText(_translate("MainWindow", "Rainfall"))
        self.actionBiome_Names.setText(_translate("MainWindow", "Biome Names"))
        self.actionBiome_Borders.setText(_translate("MainWindow", "Biome Borders"))
        self.actionRivers.setText(_translate("MainWindow", "Rivers"))


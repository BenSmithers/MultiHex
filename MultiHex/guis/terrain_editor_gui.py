"""
This file defines all the terrain editor components and adds the appropriate map functionality 
"""

# Qt items an Qt accessories
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog, QDialog, QColorDialog
from MultiHex.tools import QEntityItem

# MultiHex imports 
from MultiHex.guis.main_gui import main_gui
from MultiHex.generator.noise import generate_gradients, sample_noise
from MultiHex.generator.util import create_name
from MultiHex.map_types.overland import Nation

# these are a couple dialogs
from MultiHex.guis.confirm_inject import Ui_Dialog as confirm_ui
from MultiHex.about_class import about_dialog


import os
art_dir = os.path.join( os.path.dirname(__file__),'..','Artwork','buttons')

class ConfirmationDialog(QDialog):
    def __init__(self, parent=None, warning=''):
        QDialog.__init__(self,parent)
        self.ui=confirm_ui()
        self.ui.setupUi(self)

        if warning!='':
            if not isinstance(warning, str):
                raise TypeError("Optional arg 'warning' must be {}, not {}".format(str,type(warning)))
            self.ui.label_2.setText(warning)

class terrain_ui:
    def __init__(self,MainWindow):
        self.parent = MainWindow
        which_ui = MainWindow.ui

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_hex.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_hex_select = QtWidgets.QToolButton(which_ui.centralwidget)
        self.tool_hex_select.setIcon(icon)
        self.tool_hex_select.setIconSize(QtCore.QSize(32, 32))
        self.tool_hex_select.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_hex_select.setObjectName("tool_hex_select")
        which_ui.toolPane.addWidget(self.tool_hex_select)
        self.tool_detail = QtWidgets.QToolButton(which_ui.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"detailer.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_detail.setIcon(icon)
        self.tool_detail.setIconSize(QtCore.QSize(32, 32))
        self.tool_detail.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_detail.setObjectName("tool_detail")
        which_ui.toolPane.addWidget(self.tool_detail)
        self.tool_hex_brush = QtWidgets.QToolButton(which_ui.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"hex_brush.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_hex_brush.setIcon(icon)
        self.tool_hex_brush.setIconSize(QtCore.QSize(32, 32))
        self.tool_hex_brush.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_hex_brush.setObjectName("tool_hex_brush")
        which_ui.toolPane.addWidget(self.tool_hex_brush)
        self.tool_riv_but = QtWidgets.QToolButton(which_ui.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"new_river.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_riv_but.setIcon(icon)
        self.tool_riv_but.setIconSize(QtCore.QSize(32, 32))
        self.tool_riv_but.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_riv_but.setObjectName("tool_riv_but")
        which_ui.toolPane.addWidget(self.tool_riv_but)
        self.tool_biome_but = QtWidgets.QToolButton(which_ui.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"biome_brush.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_biome_but.setIcon(icon)
        self.tool_biome_but.setIconSize(QtCore.QSize(32, 32))
        self.tool_biome_but.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_biome_but.setObjectName("tool_biome_but")
        which_ui.toolPane.addWidget(self.tool_biome_but)
        self.tool_biome_sel = QtWidgets.QToolButton(which_ui.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_biome.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_biome_sel.setIcon(icon)
        self.tool_biome_sel.setIconSize(QtCore.QSize(32, 32))
        self.tool_biome_sel.setMinimumSize(QtCore.QSize(40,40))
        self.tool_biome_sel.setObjectName("tool_biome_sel")
        which_ui.toolPane.addWidget(self.tool_biome_sel)
        self.spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        which_ui.toolPane.addItem(self.spacerItem1)

        # define the 

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
        self.det_Brush_spin.setMinimum(0)
        self.det_Brush_spin.setMaximum(3)
        self.det_Brush_spin.setValue(2)
        self.det_Brush_spin.setObjectName("det_Brush_spin")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.det_Brush_spin)
        self.det_mag_lbl = QtWidgets.QLabel(self.Detaoer)
        self.det_mag_lbl.setObjectName("det_mag_lbl")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.det_mag_lbl)
        self.det_mag_spin = QtWidgets.QDoubleSpinBox(self.Detaoer)
        self.det_mag_spin.setMinimum(0.1)
        self.det_mag_spin.setMaximum(2.0)
        self.det_mag_spin.setSingleStep(0.1)
        self.det_mag_spin.setValue(1.0)
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
        self.det_hexid_disp = QtWidgets.QLabel(self.Detaoer)
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
        self.det_apply_button = QtWidgets.QPushButton( self.Detaoer )
        self.det_apply_button.setObjectName("det_apply_button")
        self.formLayout_4.setWidget(13, QtWidgets.QFormLayout.SpanningRole, self.det_apply_button )
        self.det_close_heatmap = QtWidgets.QPushButton( self.Detaoer )
        self.det_close_heatmap.setObjectName("det_close_heatmap")
        self.formLayout_4.setWidget(14, QtWidgets.QFormLayout.SpanningRole, self.det_close_heatmap )

        which_ui.contextPane.addItem(self.Detaoer, "")
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
        self.hex_brush_disp.setMaximum(2)
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
        which_ui.contextPane.addItem(self.HexBrush, "")
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
        self.river_trib_back_but =QtWidgets.QPushButton(self.RiverPen)
        self.river_trib_back_but.setObjectName("river_trib_back_but")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.river_trib_back_but)

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
        which_ui.contextPane.addItem(self.RiverPen, "")
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
        self.bio_color_combo = QtWidgets.QPushButton(self.BiomePainter)
        self.bio_color_combo.setObjectName("bio_color_combo")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.bio_color_combo)
        self.bio_name_but_gen = QtWidgets.QPushButton(self.BiomePainter)
        self.bio_name_but_gen.setObjectName("bio_name_but_gen")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.bio_name_but_gen)
        self.biome_but_apply = QtWidgets.QPushButton(self.BiomePainter)
        self.biome_but_apply.setObjectName("biome_but_apply")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.biome_but_apply)
        self.biome_but_delete = QtWidgets.QPushButton(self.BiomePainter)
        self.biome_but_delete.setObjectName("biome_but_delete")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.biome_but_delete)

        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_3.setItem(6, QtWidgets.QFormLayout.FieldRole, spacerItem6)
        which_ui.contextPane.addItem(self.BiomePainter, "")


        self.menuHelp = QtWidgets.QMenu(which_ui.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHeatmaps = QtWidgets.QMenu(which_ui.menubar)
        self.menuHeatmaps.setObjectName("menuHeatmaps")
        self.menuView = QtWidgets.QMenu(which_ui.menubar)
        self.menuView.setObjectName("menuView")

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

        self.menuHelp.addAction(self.actionAbout_MultiHex)
        self.menuHeatmaps.addAction(self.actionAltitude)
        self.menuHeatmaps.addAction(self.actionRainfall)
        self.menuHeatmaps.addAction(self.actionTemperature)
        self.menuView.addAction(self.actionBiome_Names)
        self.menuView.addAction(self.actionBiome_Borders)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionRivers)
        which_ui.menubar.addAction(self.menuView.menuAction())
        which_ui.menubar.addAction(self.menuHeatmaps.menuAction())
        which_ui.menubar.addAction(self.menuHelp.menuAction())

        which_ui.contextPane.setCurrentIndex(0)

        _translate = QtCore.QCoreApplication.translate
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
        self.tool_biome_sel.setToolTip(_translate("MainWindow", "Biome Selector"))
        self.tool_biome_sel.setText(_translate("MainWindow", "..."))
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
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.Detaoer), _translate("MainWindow", "Detailer"))
        self.hex_brush_lbl.setText(_translate("MainWindow", "Brush Size"))
        self.hex_select_lbl.setText(_translate("MainWindow", "Selected: "))
        self.hex_type_lbl.setText(_translate("MainWindow", "Type:"))
        self.hex_subtype_lbl.setText(_translate("MainWindow", "\n"
        "Subtype:"))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.HexBrush), _translate("MainWindow", "Hex Brush"))
        self.river_label.setText(_translate("MainWindow", "Rivers:"))
        self.riv_but_pstart.setText(_translate("MainWindow", "Pop Start"))
        self.riv_but_pend.setText(_translate("MainWindow", "Pop End"))
        self.riv_but_astart.setText(_translate("MainWindow", "Add To Start"))
        self.riv_but_aend.setText(_translate("MainWindow", "Add To End"))
        self.river_trib.setText(_translate("MainWindow", "Tributaries:"))
        self.river_trib_back_but.setText(_translate("MainWindow","Back"))
        self.det_apply_button.setText(_translate("MainWindow", "Apply"))
        self.det_close_heatmap.setText(_translate("MainWindow","Close Heatmap"))
        self.riv_but_delete.setText(_translate("MainWindow", "Delte River"))
        self.riv_name_lbl.setText(_translate("MainWindow", "Selected: "))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.RiverPen), _translate("MainWindow", "River Pen"))
        self.bio_name_disp.setText(_translate("MainWindow", "Biome:"))
        self.bio_color_lbl.setText(_translate("MainWindow", "Color:"))
        self.bio_name_but_gen.setText(_translate("MainWindow", "Generate Name"))
        self.biome_but_apply.setText(_translate("MainWindow", "Apply"))
        self.biome_but_delete.setText(_translate("MainWindow", "Delete"))
        which_ui.contextPane.setItemText(which_ui.contextPane.indexOf(self.BiomePainter), _translate("MainWindow", "Biome Painter"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuHeatmaps.setTitle(_translate("MainWindow", "Heatmaps (Beta)"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionAbout_MultiHex.setText(_translate("MainWindow", "About MultiHex"))
        self.actionTemperature.setText(_translate("MainWindow", "Temperature"))
        self.actionAltitude.setText(_translate("MainWindow", "Altitude"))
        self.actionRainfall.setText(_translate("MainWindow", "Rainfall"))
        self.actionBiome_Names.setText(_translate("MainWindow", "Biome Names"))
        self.actionBiome_Borders.setText(_translate("MainWindow", "Biome Borders"))
        self.actionRivers.setText(_translate("MainWindow", "Rivers"))

        # toolbar buttons
        self.tool_hex_select.clicked.connect( self.tb_hex_select )
        self.tool_hex_brush.clicked.connect( self.tb_hex_brush )
        self.tool_detail.clicked.connect( self.tb_detailer )
        self.tool_riv_but.clicked.connect( self.tb_new_river )
        self.tool_biome_but.clicked.connect( self.tb_new_biome )
        self.tool_biome_sel.clicked.connect( self.tb_sel_biome )

        # Detailer contextPane connections
        self.det_noise_combo.currentIndexChanged.connect( self.det_comboBox_select )
        self.det_but_noise.clicked.connect( self.det_inject_button )
        self.det_but_color.clicked.connect( self.det_color_button )
        self.det_apply_button.clicked.connect( self.det_apply_button_func )
        self.det_Brush_spin.valueChanged.connect(self.det_brush_size_change)
        self.det_mag_spin.valueChanged.connect(self.det_mag_changed)
        self.parent.detail_control.set_configuring("_altitude_base")
        self.det_close_heatmap.clicked.connect(self.det_clear_heatmap)
        self.det_close_heatmap.setEnabled(False)

        # Hexbar contextPane connections
        self.hex_type_combo.currentIndexChanged.connect( self.hex_comboBox_select )
        self.hex_list_entry = QtGui.QStandardItemModel() 
        self.hex_sub_list.setModel( self.hex_list_entry )
        self.hex_sub_list.clicked[QtCore.QModelIndex].connect( self.hex_subtype_clicked )
        self.hex_brush_disp.valueChanged.connect( self.hex_brush_change )

        self.hex_fill_supertypes()

        # river contextPane connections
        #   first all the list stuff
        self.river_list_entry = QtGui.QStandardItemModel()
        self.tributary_list_entry = QtGui.QStandardItemModel()
        self.river_list.setModel( self.river_list_entry )
        self.river_trib_list.setModel( self.tributary_list_entry )
        self.river_list.clicked[QtCore.QModelIndex].connect( self.river_list_click )
        self.river_trib_list.clicked[QtCore.QModelIndex].connect( self.river_trib_click )
        # now all the buttons
        self.riv_but_pstart.clicked.connect( self.river_ps )
        self.riv_but_pend.clicked.connect( self.river_pe )
        self.riv_but_astart.clicked.connect( self.river_as )
        self.riv_but_aend.clicked.connect( self.river_ae )
        self.riv_but_delete.clicked.connect( self.river_delete )
        self.river_trib_back_but.clicked.connect( self.river_back )
        self.river_trib_back_but.setEnabled(False)

        #biome painter buttons
        self.bio_name_but_gen.clicked.connect( self.biome_name_gen )
        self.biome_but_apply.clicked.connect( self.biome_apply )
        self.bio_color_combo.clicked.connect(self.biome_color_button)
        self.biome_but_delete.clicked.connect( self.biome_delete )

        # drop-down menu buttons
        self.actionAbout_MultiHex.triggered.connect( self.menu_help )
        self.actionTemperature.triggered.connect( self.menu_heatmap_temperature )
        self.actionAltitude.triggered.connect( self.menu_heatmap_altitude )
        self.actionRainfall.triggered.connect( self.menu_heatmap_rainfall )
        self.actionBiome_Names.triggered.connect( self.menu_view_biome_name )
        self.actionBiome_Borders.triggered.connect( self.menu_view_biome_border )
        self.actionRivers.triggered.connect( self.menu_view_rivers )
        self.actionBiome_Names.setChecked(True)
        self.actionBiome_Borders.setChecked(True)
        self.actionRivers.setChecked(True)

        self.river_update_list()

    def clear_ui(self, which_ui):
        which_ui.toolPane.removeWidget(self.tool_hex_select)
        which_ui.toolPane.removeWidget(self.tool_detail)
        which_ui.toolPane.removeWidget(self.tool_hex_brush)
        which_ui.toolPane.removeWidget(self.tool_riv_but)
        which_ui.toolPane.removeWidget(self.tool_biome_but)
        which_ui.toolPane.removeWidget(self.tool_biome_sel)

        self.tool_hex_select.deleteLater()
        self.tool_detail.deleteLater()
        self.tool_hex_brush.deleteLater()
        self.tool_riv_but.deleteLater()
        self.tool_biome_but.deleteLater()
        self.tool_biome_sel.deleteLater()

        self.tool_hex_select = None
        self.tool_detail= None
        self.tool_hex_brush= None
        self.tool_riv_but= None
        self.tool_biome_but= None
        self.tool_biome_sel= None

        which_ui.toolPane.removeItem(self.spacerItem1)

        self.Detaoer = None
        self.HexBrush = None
        self.RiverPen = None
        self.BiomePainter = None
        for i in range(4):
            which_ui.contextPane.removeItem(0)

        which_ui.menubar.removeAction(self.menuView.menuAction())
        which_ui.menubar.removeAction(self.menuHeatmaps.menuAction())
        which_ui.menubar.removeAction(self.menuHelp.menuAction())


    def _update_with_hex_id(self, id = None):
        if id is not None:
            if not isinstance(id, int):
                raise TypeError("Expected {}, got {}".format(int, type(id)))

            self.hex_select_disp.setText(str(id))
            self.det_hexid_disp.setText( str(id) )
        else:
            self.hex_select_disp.setText("")
            self.det_hexid_disp.setText("")

    def det_show_selected(self, id = None):
        """
        Function called when a new hex is selected 
        """
        if id is not None:
            if not isinstance(id, int):
                raise TypeError("Expected {}, got {}".format(int, type(id)))

            self.det_alt_slide.setValue( self.parent.main_map.catalog[id]._altitude_base*100 )
            self.det_temp_slide.setValue( self.parent.main_map.catalog[id]._temperature_base*100)
            self.det_rain_slide.setValue( self.parent.main_map.catalog[id]._rainfall_base*100)

        self._update_with_hex_id( id )
    
    def tb_hex_select(self):
        self.parent.scene.select(self.parent.hex_control)
        self.parent.hex_control.set_state(0)
        self.parent.ui.contextPane.setCurrentIndex(0)

    def tb_detailer(self):
        self.parent.scene.select(self.parent.detail_control)
        self.parent.ui.contextPane.setCurrentIndex(0)

    def tb_hex_brush(self):
        self.parent.scene.select(self.parent.hex_control)
        self.parent.hex_control.set_state(1)
        self.parent.ui.contextPane.setCurrentIndex(1)

    def tb_new_river(self):
        self.parent.ui.contextPane.setCurrentIndex(2)
        self.parent.scene.select(self.parent.river_control)
        self.parent.river_control.prepare(1)

    def tb_new_biome(self):
        self.parent.ui.contextPane.setCurrentIndex(3)
        self.parent.scene.select(self.parent.biome_control )
        self.parent.biome_control.set_state( 1 )

    def tb_sel_biome(self):
        self.parent.ui.contextPane.setCurrentIndex(3)
        self.parent.scene.select(self.parent.biome_control)
        self.parent.biome_control.set_state( 0 )

    def det_brush_size_change(self):
        new_radius = self.det_Brush_spin.value()
        self.parent.detail_control.set_radius(new_radius)

    def det_mag_changed(self):
        new_magnitude = self.det_mag_spin.value()/20.0
        self.parent.detail_control.set_magnitude( new_magnitude )

    def det_comboBox_select(self):
        combo_status = self.det_noise_combo.currentText()
        attribute = ''
        if combo_status == 'Altitude':
            attribute = '_altitude_base'
        elif combo_status == 'Rainfall':
            attribute = '_rainfall_base'
        elif combo_status == 'Temperature':
            attribute = '_temperature_base'
        else:
            raise NotImplementedError("Somehow got '{}' from combo box.".format(combo_status))

        self.parent.detail_control.set_configuring( attribute )

    def det_inject_button(self):
        """
        This button injects perlin noise into the Hexmap. 
        It uses the current state of the drop-down menu to decide which attribute to inject into

        It asks for confirmation before doing this. 
        """
        dialog = ConfirmationDialog(self.parent)
        result = dialog.exec_() 
        if result==1:
            print("Injecting")

            combo_status = self.det_noise_combo.currentText()
            attribute = ''
            if combo_status == 'Altitude':
                attribute = '_altitude_base'
            elif combo_status == 'Rainfall':
                attribute = '_rainfall_base'
            elif combo_status == 'Temperature':
                attribute = '_temperature_base'
            else:
                raise NotImplementedError("Somehow got '{}' from combo box.".format(combo_status))

            # we aren't using the perlinize function, since that tries to load/save the whole map 
            # first generate a texture file
            texture = generate_gradients()
            
            # apply the noise
            for hexID in self.parent.main_map.catalog:
                center = self.parent.main_map.catalog[hexID].center
                scale = (0.9+self.det_mag_spin.value())

                new_value = getattr( self.parent.main_map.catalog[hexID], attribute) \
                        + scale*sample_noise(center.x, center.y, 1.1*self.parent.main_map.dimensions[0],\
                        1.1*self.parent.main_map.dimensions[1], texture)

                setattr( self.parent.main_map.catalog[hexID], attribute, new_value)

                # apply the relevant heatmep

    def det_color_button(self):
        # make a Climatizer
        note = "This will take a few minutes. MultiHex may seem unresponsive. This process is irreversible"
        dialog = ConfirmationDialog(self.parent, note)
        result = dialog.exec_() 

        if result==0:
            return
        
        for hexID in self.parent.main_map.catalog:
            if self.parent.main_map.catalog[hexID].biome=='mountain':
                continue

            self.parent.climatizer.apply_climate_to_hex( self.parent.main_map.catalog[hexID] )
            self.parent.main_map.catalog[hexID].rescale_color()
            self.parent.hex_control.redraw_hex(hexID)


    def det_apply_button_func(self):
        # build the dictionary to adjut the hex
        params = {
                    "_altitude_base": self.det_alt_slide.value()/100., 
                    "_rainfall_base": self.det_rain_slide.value()/100.,
                    "_temperature_base": self.det_temp_slide.value()/100.
            }
        if self.parent.hex_control.selected is None:
            return
        self.parent.hex_control.adjust_hex( self.parent.main_map.catalog[self.parent.hex_control.selected] , params )
        self.parent.climatizer.apply_climate_to_hex( self.parent.main_map.catalog[self.parent.hex_control.selected])
        self.parent.hex_control.redraw_hex( self.parent.hex_control.selected )

    def hex_comboBox_select(self):
        """
        Called when you choose a new entry in the drop-down menu
        """
        self.hex_list_entry.clear()
        this_sub = self.hex_type_combo.currentText()

        for entry in self.parent.config[self.parent.main_map.tileset]["types"][this_sub]:
            this = QtGui.QStandardItem(entry)
            color =  self.parent.config[self.parent.main_map.tileset]["types"][this_sub][entry]["color"]
            this.setBackground( QtGui.QColor(color[0], color[1], color[2] ))
            self.hex_list_entry.appendRow(this)


    def hex_subtype_clicked(self, index=None):
        """
        Called when you click on a subtype 
        """
        # get ready to draw
        self.tb_hex_brush()

        sub_type = index.data()
        this_type = self.hex_type_combo.currentText()

        new_param = {}
        for key in self.parent.params:
            new_param[key] = self.parent.config[self.parent.main_map.tileset]["types"][this_type][sub_type][key]
        
        self.parent.hex_control.set_color(self.parent.config[self.parent.main_map.tileset]["types"][this_type][sub_type]["color"])
        self.parent.hex_control.set_params( new_param )

    def hex_brush_change(self):
        """
        Called when the brush size changes. Tells the hex_control to switch to the new size
        """
        value = self.hex_brush_disp.value()
        self.parent.hex_control.set_brush_size( value )


    def hex_fill_supertypes(self):
        # hex_type_combo
        where = self.parent.main_map.tileset
        for super_type in self.parent.config[self.parent.main_map.tileset]["types"]:
            self.hex_type_combo.addItem(super_type)

        self.hex_type_combo.setCurrentIndex(0)

    def river_list_click(self, index=None):
        """
        Called when an entry in the list of rivers is clicked 
        """
        # river_list_entry
        item = self.river_list_entry.itemFromIndex(index)
        pID = item.eID

        if pID is not None:
            self.parent.river_control.select_pid(pID)

        self.parent.river_control.sub_select( '' )
        self.river_update_gui()

    def river_trib_click(self, index=None):
        """
        Called when a tributary entry is clicked on. It selects that tributary, and reupdates the tributary list
        """
        item = self.tributary_list_entry.itemFromIndex(index).eID
        self.parent.river_control.sub_select( self.parent.river_control.sub_selection + str(item) )
        self.river_update_gui()


    def river_update_list(self):
        """
        This updates the Gui with a new list of rivers
        """
        self.river_list_entry.clear()

        if not ('rivers' in self.parent.main_map.path_catalog):
            return
        for pID in self.parent.main_map.path_catalog['rivers']:
            self.river_list_entry.appendRow( QEntityItem("River {}".format(pID), pID))

    def river_update_gui(self):
        """
        Should be called when the gui needs updating because a tributary or river was selected. 
        """
        selected = self.parent.river_control.get_sub_selection()

        self.tributary_list_entry.clear()
        if self.parent.river_control.selected_pid is not None:
            if selected.tributaries is not None:
                self.tributary_list_entry.appendRow( QEntityItem("Tributary 0".format(0), 0))
                self.tributary_list_entry.appendRow( QEntityItem("Tributary 1".format(1), 1))

        if selected.tributaries is not None:
            self.riv_but_pstart.setEnabled(False)
            self.riv_but_astart.setEnabled(False)
        else:
            self.riv_but_pstart.setEnabled(True)
            self.riv_but_astart.setEnabled(True)

        # can only add or remove from the end if this is not a tributary 
        if self.parent.river_control.sub_selection == '':
            self.riv_but_pend.setEnabled(True)
            self.riv_but_aend.setEnabled(True)
            self.river_trib_back_but.setEnabled(False)
        else:
            self.riv_but_pend.setEnabled(False)
            self.riv_but_aend.setEnabled(False)
            self.river_trib_back_but.setEnabled(True)

    def river_back(self):
        self.parent.river_control.sub_select( self.parent.river_control.sub_selection[:-1] )
        self.river_update_gui()

    def river_ps(self):
        self.parent.river_control.pop_selected_start()

    def river_pe(self):
        self.parent.river_control.pop_selected_end()

    def river_as(self):
        self.parent.scene.select(self.parent.river_control)
        self.parent.river_control.prepare( 5 )

    def river_ae(self):
        self.parent.scene.select(self.parent.river_control)
        self.parent.river_control.prepare( 3 )

    def river_delete(self):
        self.parent.river_control.delete_selected()
        self.river_update_list()

    def biome_name_gen(self):
        """
        Generates a new name for the Biome (Region)

        Uses the first registered ID to determine an overall theme (Forest, Grassland, etc)
        """
        if self.parent.biome_control.selected is None:
            return

        # this is the first registered Hex
        first = self.parent.main_map.rid_catalog[self.parent.biome_control.r_layer][self.parent.biome_control.selected].ids[0]

        new_one = create_name( self.parent.main_map.catalog[first].biome )
        self.bio_name_edit.setText( new_one )

    def biome_apply(self):
        if self.parent.biome_control.selected is None:
            pass
        else:
            self.parent.main_map.rid_catalog[self.parent.biome_control.r_layer][self.parent.biome_control.selected].name = self.bio_name_edit.text()
            self.parent.biome_control.redraw_region_text( self.parent.biome_control.selected)

    def biome_update_gui(self):
        if self.parent.biome_control.selected is None:
            self.bio_name_edit.setText("")
            self.bio_color_combo.setEnabled(False)
        else:
            self.bio_name_edit.setText(self.parent.main_map.rid_catalog[self.parent.biome_control.r_layer][self.parent.biome_control.selected].name)
            self.bio_color_combo.setEnabled(True)

    def biome_color_button(self):
        if self.parent.biome_control.selected is None:
            pass
        else:
            old_one = self.parent.main_map.rid_catalog[self.parent.biome_control.r_layer][self.parent.biome_control.selected].color
            qt_old_one = QtGui.QColor(old_one[0], old_one[1], old_one[2])
            new_color = QColorDialog.getColor(initial = qt_old_one, parent=self.parent)

            if new_color.isValid():
                self.parent.main_map.rid_catalog[self.parent.biome_control.r_layer][self.parent.biome_control.selected].color = (new_color.red(), new_color.green(), new_color.blue())
                self.parent.biome_control.redraw_region(self.parent.biome_control.selected)
    
    def biome_delete(self):
        if self.parent.biome_control.selected is None:
            pass
        else:
            self.parent.main_map.remove_region( self.parent.biome_control.selected, self.parent.biome_control.r_layer)


        self.parent.biome_control.redraw_region( self.parent.biome_control.selected )
        self.parent.biome_control.select(None)


    def menu_view_biome_name(self):
        state  = self.actionBiome_Names.isChecked()
        self.parent.biome_control.draw_names = state
        self.parent._redraw_biomes()

    def menu_view_biome_border(self):
        state = self.actionBiome_Borders.isChecked()
        self.parent.biome_control.draw_borders = state
        self.parent._redraw_biomes()

    def menu_view_rivers(self):
        state =  self.actionRivers.isChecked()
        self.parent.river_control._drawing = state
        self.parent.river_control.redraw_rivers()

    def menu_heatmap_altitude(self):
        self.parent.scene.select( self.parent.detail_control)
        self.parent.ui.contextPane.setCurrentIndex(0)
        self.hex_control.use_param_as_color = '_altitude_base'
        self.parent._redraw_hexes()
        self.det_close_heatmap.setEnabled(True)

    def menu_heatmap_temperature(self):
        self.scene.select( self.parent.detail_control)
        self.parent.ui.contextPane.setCurrentIndex(0)
        self.parent.hex_control.use_param_as_color = '_temperature_base'
        self.parent._redraw_hexes()
        self.det_close_heatmap.setEnabled(True)

    def menu_heatmap_rainfall(self):
        self.parent.scene.select( self.parent.detail_control)
        self.parent.ui.contextPane.setCurrentIndex(0)
        self.parent.hex_control.use_param_as_color = '_rainfall_base'
        self.parent._redraw_hexes()
        self.det_close_heatmap.setEnabled(True)

    def det_clear_heatmap(self):
        self.parent.hex_control.use_param_as_color = ''
        self.parent._redraw_hexes()
        self.det_close_heatmap.setEnabled(False)

    def menu_help(self):
        dialog = about_dialog(self.parent)
        dialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        dialog.exec_()
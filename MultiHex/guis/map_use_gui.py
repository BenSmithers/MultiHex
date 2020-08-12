"""
This file defines the properties of the Map Use mode for MultiHex
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import os

from MultiHex.clock import Time

art_dir = os.path.join( os.path.dirname(__file__),'..','Artwork','buttons')

class TimeTableEntry(QtWidgets.QTableWidgetItem):
    def __init__(self, time_):
        QtWidgets.QTableWidgetItem.__init__(self, str(time_))

        if not isinstance(time_, Time):
            raise TypeError("Expected {} object, not {}".format(Time, type(time_)))

        self.time = time_

class map_use_ui:
    def __init__(self, MainWindow):
        self.parent = MainWindow
        which_ui = MainWindow.ui

        # define buttons for the toolbar
        '''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(art_dir,"select_hex.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tool_hex_select = QtWidgets.QToolButton(which_ui.centralwidget)
        self.tool_hex_select.setIcon(icon)
        self.tool_hex_select.setIconSize(QtCore.QSize(32, 32))
        self.tool_hex_select.setMinimumSize(QtCore.QSize(40, 40))
        self.tool_hex_select.setObjectName("tool_hex_select")
        which_ui.toolPane.addWidget(self.tool_hex_select)
        '''

        # the panels
        self.Calendar = QtWidgets.QWidget()
        self.Calendar.setGeometry(QtCore.QRect(0,0,450,630))
        self.Calendar.setObjectName("Calendar")
        self.cal_formLayout = QtWidgets.QFormLayout(self.Calendar)
        self.cal_formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cal_formLayout.setObjectName("cal_formLayout")
        
        self.cal_obj_name_lbl = QtWidgets.QLabel(self.Calendar)
        self.cal_obj_name_lbl.setObjectName("cal_obj_name_lbl")
        self.cal_obj_name_lbl.setText("Looking at: ")
        self.cal_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.cal_obj_name_lbl)
        self.cal_obj_name_disp = QtWidgets.QLabel(self.Calendar)
        self.cal_obj_name_disp.setObjectName("cal_obj_name_disp")
        self.cal_obj_name_disp.setText("${Object_Name}")
        self.cal_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cal_obj_name_disp)
        self.cal_lat_lbl = QtWidgets.QLabel(self.Calendar)
        self.cal_lat_lbl.setObjectName("cal_lat_lbl")
        self.cal_lat_lbl.setText("Latitude: ")
        self.cal_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.cal_lat_lbl)
        self.cal_lat_disp = QtWidgets.QLabel(self.Calendar)
        self.cal_lat_disp.setObjectName("cal_lat_disp")
        self.cal_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cal_lat_disp)
        self.cal_lon_lbl = QtWidgets.QLabel(self.Calendar)
        self.cal_lon_lbl.setObjectName("cal_lon_lbl")
        self.cal_lon_lbl.setText("Longitude: ")
        self.cal_formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.cal_lon_lbl)
        self.cal_lon_disp = QtWidgets.QLabel(self.Calendar)
        self.cal_lon_disp.setObjectName("cal_lat_disp")
        self.cal_formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cal_lon_disp)
        self.cal_date_disp = QtWidgets.QLabel(self.Calendar)
        self.cal_date_disp.setObjectName("cal_date_disp")
        self.cal_date_disp.setText("10 August 2020, 8:43 PM")
        self.cal_formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.cal_date_disp)
        
        self.cal_next_evt_layout = QtWidgets.QHBoxLayout()
        self.cal_next_evt_layout.setObjectName("cal_next_evt_layout")
        self.cal_next_evt_button = QtWidgets.QPushButton(self.Calendar)
        self.cal_next_evt_button.setObjectName("cal_next_evt_button")
        self.cal_next_evt_button.setText("Next Event")
        self.cal_next_evt_layout.addWidget(self.cal_next_evt_button)
        self.cal_next_sun_button = QtWidgets.QPushButton(self.Calendar)
        self.cal_next_sun_button.setObjectName("cal_next_sun_button")
        self.cal_next_sun_button.setText("Next Suntime")
        self.cal_next_evt_layout.addWidget(self.cal_next_sun_button)
        self.cal_next_some_button = QtWidgets.QPushButton(self.Calendar)
        self.cal_next_some_button.setObjectName("cal_next_some_button")
        self.cal_next_some_button.setText("Something")
        self.cal_next_evt_layout.addWidget(self.cal_next_some_button)
        self.cal_formLayout.setLayout(5, QtWidgets.QFormLayout.SpanningRole, self.cal_next_evt_layout)
        
        self.cal_scroll_area = QtWidgets.QScrollArea()
        self.cal_scroll_area.setObjectName("cal_scroll_area")
        self.cal_formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.cal_scroll_area)

        self.cal_scroll_layout = QtWidgets.QVBoxLayout()
        self.cal_scroll_layout.setObjectName("cal_scroll_layout")
        self.cal_evt_table = QtWidgets.QTableWidget(self.Calendar)
        self.cal_evt_table.setColumnCount(2)
        self.cal_evt_table.setVerticalHeaderLabels(["Date","Description"])
        self.cal_evt_table.setSortingEnabled(True)
        self.cal_evt_table.setEnabled(False)
        self._add_row_entry(Time(1,13,2,5,120),"Birthday?")
        self._add_row_entry(Time(1,27,2,2,120),"Happy day")
        self._add_row_entry(Time(13,15,4,4,119),"Happiest day")
        self.cal_evt_table.horizontalHeader().setStretchLastSection(True)
        self.cal_evt_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.cal_scroll_layout.addWidget(self.cal_evt_table)
        self.cal_scroll_area.setLayout(self.cal_scroll_layout)


        # put in the big whatchamajigger
        self.cal_skip_layout = QtWidgets.QHBoxLayout()
        self.cal_skip_layout.setObjectName("cal_skip_layout")
        self.cal_skip_button = QtWidgets.QPushButton(self.Calendar)
        self.cal_skip_button.setObjectName("cal_skip_button")
        self.cal_skip_button.setText("Skip")
        self.cal_skip_layout.addWidget(self.cal_skip_button)
        self.cal_skip_number_spin = QtWidgets.QSpinBox(self.Calendar)
        self.cal_skip_number_spin.setObjectName("cal_skip_number_spin")
        self.cal_skip_number_spin.setMinimum(1)
        self.cal_skip_number_spin.setMaximum(60)
        self.cal_skip_number_spin.setSingleStep(1)
        self.cal_skip_layout.addWidget(self.cal_skip_number_spin)
        self.cal_skip_combo = QtWidgets.QComboBox(self.Calendar)
        self.cal_skip_combo.setObjectName("cal_skip_combo")
        self.cal_skip_combo.addItem("Minutes")
        self.cal_skip_combo.addItem("Hours")
        self.cal_skip_combo.addItem("Days")
        self.cal_skip_combo.addItem("Weeks")
        self.cal_skip_combo.addItem("Months")
        self.cal_skip_combo.addItem("Years")
        self.cal_skip_layout.addWidget(self.cal_skip_combo)
        self.cal_formLayout.setLayout(7, QtWidgets.QFormLayout.SpanningRole, self.cal_skip_layout)
        self.cal_new_evt_button=QtWidgets.QPushButton(self.Calendar)
        self.cal_new_evt_button.setObjectName("cal_new_evt_button")
        self.cal_new_evt_button.setText("Add New Event")
        self.cal_formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.cal_new_evt_button)

        which_ui.contextPane.addItem(self.Calendar,"Calendar")

    def _add_row_entry(self, date, description):
        """
        Adds an entry to the table
        """
        if not isinstance(date, Time):
            raise TypeError("Expected {} object, not {}".format(Time, type(date)))

        #self.cal_evt_table.setRowCount(self.cal_evt_table.rowCount()+1)
        #self.cal_evt_table.setColumnCount(self.cal_evt_table.columnCount()+1)

        insertion_row = 0
        
        #self.cal_evt_table.itemAt(1,1)

        if self.cal_evt_table.rowCount()>0:
            while date > self.cal_evt_table.itemAt(insertion_row, 0).time:
                insertion_row+=1
                if insertion_row==self.cal_evt_table.rowCount():
                    break

        self.cal_evt_table.insertRow(insertion_row)
        self.cal_evt_table.setItem(insertion_row,0,TimeTableEntry(date))
        self.cal_evt_table.setItem(insertion_row,1,QtWidgets.QTableWidgetItem(description))

    def clear_ui(self, which_ui):
        pass

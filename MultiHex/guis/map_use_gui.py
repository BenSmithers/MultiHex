"""
This file defines the properties of the Map Use mode for MultiHex
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import os

from MultiHex.clock import Time, MultiHexCalendar

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
        self.cal_form_layout = QtWidgets.QFormLayout(self.Calendar)
        self.cal_form_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cal_form_layout.setObjectName("cal_form_layout")
        self.cal_Calendar = MultiHexCalendar(self.Calendar, Time(3,12,4,17,210))
        self.cal_Calendar.setObjectName("Actual calendar")
        self.cal_form_layout.setWidget(1,QtWidgets.QFormLayout.SpanningRole, self.cal_Calendar)

        which_ui.contextPane.addItem(self.Calendar,"Calendar")

        #=======  Defining the event list panel  =============================
        self.EventsList = QtWidgets.QWidget()
        self.EventsList.setGeometry(QtCore.QRect(0,0,450,630))
        self.EventsList.setObjectName("EventsList")
        self.evt_formLayout = QtWidgets.QFormLayout(self.EventsList)
        self.evt_formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.evt_formLayout.setObjectName("evt_formLayout")
        self.evt_obj_name_lbl = QtWidgets.QLabel(self.EventsList)
        self.evt_obj_name_lbl.setObjectName("evt_obj_name_lbl")
        self.evt_obj_name_lbl.setText("Looking at: ")
        self.evt_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.evt_obj_name_lbl)
        self.evt_obj_name_disp = QtWidgets.QLabel(self.EventsList)
        self.evt_obj_name_disp.setObjectName("evt_obj_name_disp")
        self.evt_obj_name_disp.setText("${Object_Name}")
        self.evt_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.evt_obj_name_disp)
        self.evt_lat_lbl = QtWidgets.QLabel(self.EventsList)
        self.evt_lat_lbl.setObjectName("evt_lat_lbl")
        self.evt_lat_lbl.setText("Latitude: ")
        self.evt_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.evt_lat_lbl)
        self.evt_lat_disp = QtWidgets.QLabel(self.EventsList)
        self.evt_lat_disp.setObjectName("evt_lat_disp")
        self.evt_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.evt_lat_disp)
        self.evt_lon_lbl = QtWidgets.QLabel(self.EventsList)
        self.evt_lon_lbl.setObjectName("evt_lon_lbl")
        self.evt_lon_lbl.setText("Longitude: ")
        self.evt_formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.evt_lon_lbl)
        self.evt_lon_disp = QtWidgets.QLabel(self.EventsList)
        self.evt_lon_disp.setObjectName("evt_lat_disp")
        self.evt_formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.evt_lon_disp)
        self.evt_date_disp = QtWidgets.QLabel(self.EventsList)
        self.evt_date_disp.setObjectName("evt_date_disp")
        self.evt_date_disp.setText("10 August 2020, 8:43 PM")
        self.evt_formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.evt_date_disp)
        self.evt_next_evt_layout = QtWidgets.QHBoxLayout()
        self.evt_next_evt_layout.setObjectName("evt_next_evt_layout")
        self.evt_next_evt_button = QtWidgets.QPushButton(self.EventsList)
        self.evt_next_evt_button.setObjectName("evt_next_evt_button")
        self.evt_next_evt_button.setText("Next Event")
        self.evt_next_evt_layout.addWidget(self.evt_next_evt_button)
        self.evt_next_sun_button = QtWidgets.QPushButton(self.EventsList)
        self.evt_next_sun_button.setObjectName("evt_next_sun_button")
        self.evt_next_sun_button.setText("Next Suntime")
        self.evt_next_evt_layout.addWidget(self.evt_next_sun_button)
        self.evt_next_some_button = QtWidgets.QPushButton(self.EventsList)
        self.evt_next_some_button.setObjectName("evt_next_some_button")
        self.evt_next_some_button.setText("Something")
        self.evt_next_evt_layout.addWidget(self.evt_next_some_button)
        self.evt_formLayout.setLayout(5, QtWidgets.QFormLayout.SpanningRole, self.evt_next_evt_layout)
        self.evt_scroll_area = QtWidgets.QScrollArea()
        self.evt_scroll_area.setObjectName("evt_scroll_area")
        self.evt_formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.evt_scroll_area)
        self.evt_scroll_layout = QtWidgets.QVBoxLayout()
        self.evt_scroll_layout.setObjectName("evt_scroll_layout")
        self.evt_evt_table = QtWidgets.QTableWidget(self.EventsList)
        self.evt_evt_table.setColumnCount(2)
        self.evt_evt_table.setVerticalHeaderLabels(["Date","Description"])
        self.evt_evt_table.setSortingEnabled(True)
        self.evt_evt_table.setEnabled(False)
        self._add_row_entry(Time(1,13,2,5,120),"Birthday?")
        self._add_row_entry(Time(1,27,2,2,120),"Happy day")
        self._add_row_entry(Time(13,15,4,4,119),"Happiest day")
        self.evt_evt_table.horizontalHeader().setStretchLastSection(True)
        self.evt_evt_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.evt_scroll_layout.addWidget(self.evt_evt_table)
        self.evt_scroll_area.setLayout(self.evt_scroll_layout)
        self.evt_skip_layout = QtWidgets.QHBoxLayout()
        self.evt_skip_layout.setObjectName("evt_skip_layout")
        self.evt_skip_button = QtWidgets.QPushButton(self.EventsList)
        self.evt_skip_button.setObjectName("evt_skip_button")
        self.evt_skip_button.setText("Skip")
        self.evt_skip_layout.addWidget(self.evt_skip_button)
        self.evt_skip_number_spin = QtWidgets.QSpinBox(self.EventsList)
        self.evt_skip_number_spin.setObjectName("evt_skip_number_spin")
        self.evt_skip_number_spin.setMinimum(1)
        self.evt_skip_number_spin.setMaximum(60)
        self.evt_skip_number_spin.setSingleStep(1)
        self.evt_skip_layout.addWidget(self.evt_skip_number_spin)
        self.evt_skip_combo = QtWidgets.QComboBox(self.EventsList)
        self.evt_skip_combo.setObjectName("evt_skip_combo")
        self.evt_skip_combo.addItem("Minutes")
        self.evt_skip_combo.addItem("Hours")
        self.evt_skip_combo.addItem("Days")
        self.evt_skip_combo.addItem("Weeks")
        self.evt_skip_combo.addItem("Months")
        self.evt_skip_combo.addItem("Years")
        self.evt_skip_layout.addWidget(self.evt_skip_combo)
        self.evt_formLayout.setLayout(7, QtWidgets.QFormLayout.SpanningRole, self.evt_skip_layout)
        self.evt_new_evt_button=QtWidgets.QPushButton(self.EventsList)
        self.evt_new_evt_button.setObjectName("evt_new_evt_button")
        self.evt_new_evt_button.setText("Add New Event")
        self.evt_formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.evt_new_evt_button)
        which_ui.contextPane.addItem(self.EventsList,"Event List")
        
        #self.cal_Calendar.signals.signal.connect(self.dis_is_a_test)

    def _add_row_entry(self, date, description):
        """
        Adds an entry to the table
        """
        if not isinstance(date, Time):
            raise TypeError("Expected {} object, not {}".format(Time, type(date)))

        #self.evt_evt_table.setRowCount(self.evt_evt_table.rowCount()+1)
        #self.evt_evt_table.setColumnCount(self.evt_evt_table.columnCount()+1)

        insertion_row = 0
        
        #self.evt_evt_table.itemAt(1,1)

        if self.evt_evt_table.rowCount()>0:
            while date > self.evt_evt_table.itemAt(insertion_row, 0).time:
                insertion_row+=1
                if insertion_row==self.evt_evt_table.rowCount():
                    break

        self.evt_evt_table.insertRow(insertion_row)
        self.evt_evt_table.setItem(insertion_row,0,TimeTableEntry(date))
        self.evt_evt_table.setItem(insertion_row,1,QtWidgets.QTableWidgetItem(description))


    def clear_ui(self, which_ui):
        pass

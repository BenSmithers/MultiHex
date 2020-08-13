"""
This file defines the properties of the Map Use mode for MultiHex
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import os

from MultiHex.clock import Time, month_list, day_list, days_in_month, months_in_year

art_dir = os.path.join( os.path.dirname(__file__),'..','Artwork','buttons')

class TimeTableEntry(QtWidgets.QTableWidgetItem):
    def __init__(self, time_):
        QtWidgets.QTableWidgetItem.__init__(self, str(time_))

        if not isinstance(time_, Time):
            raise TypeError("Expected {} object, not {}".format(Time, type(time_)))

        self.time = time_

class MultiHexCalendar(QtWidgets.QWidget):
    def __init__(self, parent, time):
        QtWidgets.QWidget.__init__(self, parent)
        if not isinstance(time, Time):
            raise TypeError("Expected {}, got {}".format(Time, type(time)))

        self.time = time

        self.setObjectName("MuliHexCalendar")
        self.layout = QtWidgets.QVBoxLayout(self)

        self.year_layout = QtWidgets.QHBoxLayout(self)
        self.leftButton = QtWidgets.QPushButton(self)
        self.leftButton.setObjectName("leftButton")
        self.leftButton.setFixedSize(25,25)
        self.leftButton.setText("<-")
        self.rightButton = QtWidgets.QPushButton(self)
        self.rightButton.setObjectName("rightButton")
        self.rightButton.setFixedSize(25,25)
        self.rightButton.setText("->")
        self.yearLabel = QtWidgets.QLabel(self)
        self.yearLabel.setObjectName("yearLabel")
        self.yearLabel.setText("{}".format(self.time.year))
        self.yearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.year_layout.addWidget(self.leftButton)
        self.year_layout.addWidget(self.yearLabel)
        self.year_layout.addWidget(self.rightButton)
        self.layout.addItem(self.year_layout)

        self.month_layout = QtWidgets.QHBoxLayout(self)
        self.leftButtonMon = QtWidgets.QPushButton(self)
        self.leftButtonMon.setObjectName("leftButtonMon")
        self.leftButtonMon.setFixedSize(25,25)
        self.leftButtonMon.setText("<-")
        self.rightButtonMon = QtWidgets.QPushButton(self)
        self.rightButtonMon.setObjectName("rightButtonMon")
        self.rightButtonMon.setFixedSize(25,25)
        self.rightButtonMon.setText("->")
        self.month_combo = QtWidgets.QComboBox(self)
        self.month_combo.setObjectName("month_combo")
        for month in month_list:
            self.month_combo.addItem(month)
        self.month_layout.addWidget(self.leftButtonMon)
        self.month_layout.addWidget(self.month_combo)
        self.month_layout.addWidget(self.rightButtonMon)
        self.layout.addItem(self.month_layout)
        self.month_combo.setCurrentIndex(self.time.month)

        
        weekday_lbls ={}
        self.weekday_list = QtWidgets.QHBoxLayout(self)
        for day in range(len(day_list)):
            weekday_lbls[day] = QtWidgets.QLabel(self)
            weekday_lbls[day].setText(day_list[day][:2])
            weekday_lbls[day].setObjectName(day_list[day])
            weekday_lbls[day].setAlignment(QtCore.Qt.AlignCenter)

            self.weekday_list.addWidget(weekday_lbls[day])
        self.layout.addItem(self.weekday_list)

        self.day_buttons = {}
        self.calendarGrid =  QtWidgets.QGridLayout(self)
        self.total_rows = int(days_in_month /len(day_list) ) + 1

        row = 0
        column = 0
        day = 0
        while row<=self.total_rows:
            self.day_buttons[day] = QtWidgets.QPushButton(self)
            self.day_buttons[day].setFixedSize(25,25)
            self.day_buttons[day].setText("")
            self.day_buttons[day].setEnabled(False)
            self.calendarGrid.addWidget(self.day_buttons[day],row,column)

            column+=1
            day+=1
            if column==(len(day_list)):
                column = 0
                row += 1
        self.days = day
        self.layout.addItem(self.calendarGrid)
        self.fill_days()

        self.month_combo.currentIndexChanged.connect(self.change_month)
        self.leftButton.clicked.connect(self.remove_year)
        self.rightButton.clicked.connect(self.add_year)
        self.leftButtonMon.clicked.connect(self.leftMon)
        self.rightButtonMon.clicked.connect(self.rightMon)

    def fill_days(self):

        # total days is N

        counting = False
        days_so_far = 0
        day = 0 
        first_of_month = Time(year=self.time.year, month = self.time.month, day=0).get_day_of_week()

        while day < self.days:
            if day==first_of_month and days_so_far==0:
                counting = True

            if counting:
                days_so_far += 1
                self.day_buttons[day].setText(str(days_so_far))
                self.day_buttons[day].setEnabled(True)
            else:
                self.day_buttons[day].setText("")
                self.day_buttons[day].setEnabled(False)

            if days_so_far==days_in_month:
                counting=False

            day+=1

    def leftMon(self):
        new = self.month_combo.currentIndex() -1
        if new<0:
            self.time = self.time - Time(year=1)
            self.month_combo.setCurrentIndex(months_in_year-1)
        else:
            self.month_combo.setCurrentIndex(new)

    def rightMon(self):
        new = self.month_combo.currentIndex() +1
        if new==months_in_year:
            self.time = self.time + Time(year=1)
            self.month_combo.setCurrentIndex(0)
        else:
            self.month_combo.setCurrentIndex(new)

    def change_month(self):
        month_diff = self.month_combo.currentIndex() - self.time.month
        if month_diff > 0 :
            self.time =self.time+ Time(month=month_diff )
        elif month_diff <0:
            self.time = self.time- Time(month=-1*month_diff)
        self.fill_days()
        self.yearLabel.setText("{}".format(self.time.year))

    def add_year(self):
        self.time += Time(year=1)
        self.yearLabel.setText("{}".format(self.time.year))
        self.fill_days()

    def remove_year(self):
        self.time -= Time(year=1)
        self.yearLabel.setText("{}".format(self.time.year))
        self.fill_days()



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

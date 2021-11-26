"""
Three classes are defined here

    Time  -  an instance in time. Has a number of years, months, days, etc...
    Clock - keeps track of time across a whole planet. Incl timezones. Includes utilities for skipping around to significant times (sunrise, sunset). Can return light levels at any latitude/longitude.
                keeps track of moon too.
    MultiHexCalendar - A Qt widget for the calendar in the time system described here 
"""


from PyQt5 import QtWidgets, QtCore

from math import pi, floor
from math import cos, sin, sqrt

from numpy import arcsin, arccos

degrees = pi/180.

minutes_in_hour = 60
hours_in_day    = 24
days_in_month   = 33
months_in_year  = 12

minutes_in_day   = minutes_in_hour*hours_in_day
minutes_in_month = minutes_in_day*days_in_month
minutes_in_year  = minutes_in_month*months_in_year

# Idea: load these days in from a config file! 
month_list = [ "January",
            "Febuary",
            "Maruary",
            "Apruary",
            "Mayuary",
            "Junuary",
            "Juluary",
            "Auguary",
            "Sepuary",
            "Octuary",
            "Novuary",
            "Decuary" ]
assert( len(month_list) == months_in_year )


day_list = [ "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"]

days_in_week = len(day_list)

phases = {  "New":0.0,
            "Waxing Crescent":0.3,
            "Waxing Gibbous":0.6,
            "Full":1.0,
            "Wanning Gibbous":0.6,
            "Wanning Crescent":0.3}


class Time:
    """
    Used to pass around and properly format the times
    """

    def __init__(self, minute=0, hour=0, day = 0, month=0, year = 0,date=True, **kwargs):
        if not ( minute>=0 ):
            raise ValueError("Invalid number of minutes {}".format(minute))
        if not (hour>=0 and hour<hours_in_day):
            raise ValueError("Invalid number of hours {}".format(hour))


        self._hour      = hour 
        self._minute    = minute
        self._month     = month
        self._day       = day
        self._year      = year

        self.date      = date

        while self._minute > minutes_in_hour:
            self._hour += 1
            self._minute -= minutes_in_hour
        while self._hour > hours_in_day:
            self._hour -= hours_in_day
            self._day += 1

        self.morning = ( hour < hours_in_day/2  )

        self._day_shift = 2

    @property
    def year(self):
        return( self._year )
    @property
    def month(self):
        return( self._month )
    @property
    def day(self):
        return( self._day )
    @property
    def hour(self):

        return( self._hour )
    @property
    def minute(self):

        return(self._minute)

    def get_day_of_week(self):
        """
        Returns the day of the week given the current time
        """
        n_days = self._day_shift + self.day + days_in_month*(self.month + months_in_year*self.year)
        return(  n_days % len(day_list) )

    def get_day_of_week_str(self):
        """
        Returns the day of the week as a string. 
        """
        return(day_list[self.get_day_of_week()])

    def month_str(self):
        """
        Returns the current month as a string
        """
        if type(self._month )!=int:
            raise TypeError("That's not right... month is type {}".format(type(self._month)))
        
        return( month_list[self._month] )

    def _month_step(self, months):
        """
        Steps forward by given number of months
        """
        if not isinstance( months, int):
            raise TypeError("Expected {} for months, got {}".format(int, type(months)))
        self._month = months + self._month

        while self._month >= months_in_year:
            self._year += 1
            self._month -= months_in_year

    def _day_step(self, days):
        """
        Steps forward by given number of days
        """
        if not isinstance( days, int):
            raise TypeError("Expected {} for days, got {}".format(int, type(days)))
        self._day += days

        while self._day >= (days_in_month):
            self._month_step( 1 )
            self._day-= days_in_month

    def _hour_step(self, hours):
        """
        Steps forward by given number of hours
        """
        if not isinstance( hours, int):
            raise TypeError("Expected {} for hours, got {}".format(int, type(hours)))
        self._hour += hours

        while self._hour >= hours_in_day:
            self._day_step(1)
            self._hour -= hours_in_day


    def _minute_step(self, minutes):
        """
        Steps forward by given number of minutes
        """
        if not isinstance( minutes, int):
            raise TypeError("Expected {} for minutes, got {}".format(int, type(minutes)))
        self._minute += minutes
        
        while self._minute >= minutes_in_hour:
            self._hour_step(1)
            self._minute -= minutes_in_hour
 
    def time_step(self, minutes=0, hours=0, days=0, months=0, years=0):
        """
        Move the current time forward by some number of minutes (or optionally years, months, etc)
        """
        if minutes!=0:
            self._minute_step( minutes )
        if hours!=0:
            self._hour_step( hours)
        if days!=0:
            self._day_step(days)
        if months!=0:
            self._month_step(months)

        self._year += years

    def __str__(self):
        if self.date:
            self.morning = ( self.hour < hours_in_day/2  )
            if self.morning:
                if self.hour == 0:
                    out = "12:{:02d} AM".format( self.minute )
                else:
                    out = "{}:{:02d} AM".format( self.hour, self.minute )
            else: 
                if self.hour == 12:
                    out = "12:{:02d} PM".format( self.minute)
                else:
                    out = "{}:{:02d} PM".format( int(self.hour - hours_in_day/2 ), self.minute)

            return("{} {}, {}, at {}".format(self.month_str(), self._day+1, self._year, out))
        else:
            out = ""
            if self._year!=0:
                out+="{} years, ".format(self._year)
            if self._month!=0:
                out+="{} months, ".format(self._month)
            if self._day!=0:
                out+="{} days, ".format(self._day)
            if self._hour!=0:
                out+="{} hours, ".format(self._hour)
            if out!="":
                out+="and "
            out += "{} minutes".format(self._minute)
            return(out)

    def __repr__(self):
        return("<Time Object: {}>".format(self))

    def __add__(self, other ):
        """
        Define method by which two times are added together
        """
        new = Time(minute=self.minute,hour=self.hour,day=self.day,month=self.month,year=self.year)
        new._hour += other.hour
        new._minute+= other.minute
        new._day += other.day
        new._month += other.month
        new._year += other.year

        while new._minute>= minutes_in_hour:
            new._minute -= minutes_in_hour
            new._hour += 1
        while new._hour>= hours_in_day:
            new._hour -= hours_in_day
            new._day  += 1
        while new._day>= days_in_month:
            new._day -=  days_in_month
            new._month += 1
        while new._month>= months_in_year:
            new._month -= months_in_year
            new._year += 1

        return(new)
        

    def __sub__(self, other):
        new = Time(self.minute, self.hour, self.day, self.month, self.year)
        new._minute -= other._minute
        while new.minute<0:
            new._minute+=minutes_in_hour
            new._hour -= 1
        new._hour -= other.hour
        while new.hour < 0:
            new._hour += hours_in_day
            new._day -= 1
        new._day -= other.day
        while new.day <0:
            new._day += days_in_month
            new._month -= 1
        new._month -= other.month
        while new._month <0 :
            new._month += months_in_year
            new._year -= 1
        new._year -= other.year

        return(new)
    
    def __lt__(self, other):
        """
        implements the "<" operator 
        """
        if self.year < other.year:
            return( True )
        elif other.year < self.year:
            return( False )
        else: # years are equal
            if self.month < other.month:
                return( True )
            elif other.month < self.month:
                return( False )
            else: #months are equal
                if self.day < other.day:
                    return( True )
                elif other.day < self.day:
                    return( False )
                else: # days are equal
                    if self.hour < other.hour:
                        return( True )
                    elif other.hour < self.hour:
                        return( False )
                    else: # hours are equal
                        if self.minute < other.minute:
                            return( True )
                        else: # either it's greater than or equal to
                            return( False )
    def __gt__(self, other):
        """
        Implements the ">" operator. Opposite of "<" operator but they can't be equal! 
        """
        return( (not self.__lt__(other)) and (self.minute!=other.minute))

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError("Cannot multiply by type {}".format(type(other)))

        add = other>=0
        other = abs(other)
        mins = self.minute*other
        hours = self.hour*other
        days = self.day*other
        mons = self.month*other
        years = self.year*other
        return Time(mins,hours,days,mons,years)

    def __rmul__(self,other):
        return self.__mul__(other)


    def __eq__(self,other):
        """
        Implements the "==" operator. 
        """
        return( self.hour == other.hour and self.minute == other.minute and self.month == other.month and self.day==other.day and self.year==other.year)

    def __float__(self):
        return float(int(self))

    def __int__(self):
        """
        We need this special casting of the Time object so we can properly serialize these objects in the Pandas DataFrame
        """
        value = self.minute
        value += minutes_in_hour*self.hour + minutes_in_day*self.day + minutes_in_month*self.month + minutes_in_year*self.year
        return(int(value))

minute = Time(minute=1)
hour = Time(hour=1)
day = Time(day=1)
month = Time(month=1)
year = Time(year=1)


class Clock:
    """
    Simple clock class to keep track of the time 
    """

    def __init__(self):
        
        # GMT like time counter
        self._time = Time(0 , 0)

        self._axial_tilt = 23.5*degrees
        self._coax = cos(self._axial_tilt)
        self._siax = sin(self._axial_tilt)

        self._lunar_offset = 3 
        self._lunar_length = 28

        self._holidays = { "Winter_Solstice":Time(month=0),
                    "Spring_Equinox":Time(month=3),
                    "Summer_Solstice":Time(month=6),
                    "Autumnal_Equinox":Time(month=9) }
            
        # cache some things to speed up sunrise and sunset calculations
        self._cache_lat = None
        self._cache_lon = None
        self._cache_co_lat = 0.0
        self._cache_sin_lat = 0.0
        self._cache_co_lon = 0.0
        self._cache_sin_lon = 0.0

    @property
    def time(self):
        return self._time

    def get_day_of_week(self):
        """
        Returns the current day of the week
        """
        return(self._time.get_day_of_week())

    def change_axial_tilt(self, new_tilt):
        """
        Changes the axial tilt of the planet to the provided tilt

        @param new_tilt     - float, radian ( 0 , pi )
        """
        if not isinstance( new_tilt, float):
            raise TypeError("Expected {}, got {}".format(float, type(new_tilt)))
        if not (new_tilt>0 and new_tilt<pi):
            raise ValueError("Invalid tilt {}".format(new_tilt))

        self._axial_tilt = new_tilt

    def get_tilt(self):
        """
        Returns the axial tilt of the planet
        """
        return( self._axial_tilt )

    def skip_to_holiday(self, holiday):
        """
        Skips the clock to the registered holiday with specified key (name)
        """
        if not isinstance(holiday, str):
            raise TypeError("Expected type {}, got {}".format(str, type(holiday)))
        if holiday not in self._holidays:
            raise ValueError("{} not a known holiday".format(holiday))

        when = self._holidays[holiday]
        self.skip_to_day( when )

    def skip_to_hour(self, what_time):
        """
        Dials the clock /forward/ to a specific time of day
        """
        if not isinstance(what_time, Time):
            raise TypeError("Expected {}, got {}".format(Time, type(what_time)))

        what_time._year = self._time.year
        what_time._month = self._time.month
        what_time._day   = self._time.day

        if what_time < self._time:
            what_time._day = what_time._day + 1

        self.skip_to( what_time )

    def skip_to_day( self, day ):
        """
        Skips to a specific day of the year. 

        @param day  - A Time object. Its year, minute, and hour are ignored. Only the day and month are used
        """
        if not isinstance(day, Time):
            raise TypeError("Expected {}, got {}".format(Time, type(day)))

        day._year = self._time.year
        day._minute= 0
        day._hour  = 0
        if day < self._time:
            day._year = day._year + 1

        self.skip_to( day )

    def add_holiday( self, time_obj, name):
        """
        Registers a _federal_ holiday with the Clock
        """
        if not isinstance(name, str):
            raise TypeError("Expected type {}, got {}".format(str, type(name)))
        if not isinstance(time_obj, Time):
            raise TypeError("Expected type {}, got {}".format(Time, type(time_obj)))
        if name in self._holidays.keys():
            raise ValueError("Key '{}' already in holiday list".format(name))

        self._holidays[name] = time_obj

    def remove_holiday(self, name):
        if not isinstance(name, str):
            raise TypeError("Expected type {}, got {}".format(str, type(name)))

        del self._holidays[name]

    def get_local_time( self, lon ):
        """
        Uses the longitude of the given point to shift to a different time zone

        We assume standard time zones 
        """

        if not ( lon>=0 and (lon<(2*pi))):
            raise ValueError("Invalid longitude {}".format(lon))

        hour_shift = int( hours_in_day*(lon/(2*pi))) # - 0.5*hours_in_day)

        if hour_shift >= 0 :
            return( self._time + Time(hour=hour_shift ) )
        else:
            return( self._time - Time(hour=-1*hour_shift))

    def skip_to_suntime(self, latitude, longitude):
        """
        Skips to the next sunrise or sunset at the given latitude and longitude 
        """
        when    = self.get_next_suntime(latitude, longitude)
        now     = self.get_local_time(longitude)

        self.skip_time( when - now )

    def skip_to_phase(self, phase):
        if not isinstance(phase, str):
            raise TypeError("Expected {}, got {}".format(str, type(phase)))


        # how many days through a cycle is the target phase?
        how_many = int(list(phases.keys()).index(phase)*float(self._lunar_length)/len(phases.keys()))

        # how many days through the cycle are we?
        total_days = self._time.day + self._time.month*days_in_month + self._time.year*days_in_month*months_in_year
        days_through_cycle = (total_days - self._lunar_offset) % self._lunar_length 
        
        if days_through_cycle > how_many:
            # if we're passed it, step into the next cycle
            days_to_skip = self._lunar_length - (days_through_cycle - how_many)
        else:
            # if we haven't reached it, go to it
            days_to_skip = how_many - days_through_cycle

        # sted to one day before the cycle 
        if days_to_skip > 1:
            self.skip_time(Time( day = (days_to_skip - 1  )))

        # default time is midnight
        # skip to then
        self.skip_to_hour( Time() )

    def get_moon_phase(self):
        """
        returns the current phase of the moon 
        
        Moon phase simplified to be exactly 28 days long
        """

        total_days = self._time.day + self._time.month*days_in_month + self._time.year*days_in_month*months_in_year
        days_through_cycle = (total_days - self._lunar_offset) % self._lunar_length 
        
        percent_through = float( days_through_cycle )/self._lunar_length
        which_part = int( percent_through * len(phases.keys()) )
        
        return( list(phases.keys())[which_part] )

    def get_base_moon_light(self):
        """
        Returns the amount of light given off by the moon right now (regardless of where it is in the sky) 
        """
        return(phases[self.get_moon_phase()])

         
    def skip_to(self, new_time):
        """
        Turns the clock forward to the given Time
        """
        if not isinstance(new_time, Time):
            raise TypeError("Expected object of type {}, got {}.".format(Time, type(new_time)))

        if new_time < self._time:
            raise ValueError("{} is in the past. It's {}".format(new_time, self._time))

        lapse = new_time - self._time

        self.skip_time(Time(lapse.minute, lapse.hour, lapse.day, lapse.month, lapse.year))

    def get_time_to_holiday(self, holiday):
        """
        Returns the amount of time, as a Time object, to the next holiday 
        """
        if not isinstance(holiday, str):
            raise TypeError("Expected type {}, got {}".format(str, type(holiday)))
        if holiday not in self._holidays:
            raise ValueError("{} not a known holiday".format(holiday))

        when = self._holidays[holiday]
        when._year = self._time.year

        if when < self._time:
            when._year = when._year + 1

        time_to = when - self._time
        time_to.date = False

        return(time_to)

    def get_sun_angle(self, lat, long):
        """
        Returns the height of the sun above the horizon, in radians
        """
        ll = -1*self.get_current_light_level(lat, long)

        if ll > 0:
            return()
        else:
            return( pi - arccos( ll ) )

    def get_light_level(self, time_minutes, lat, long):
        """
        Returns the light level (-1 to 1) at the given latitude, longitude, and point in time

        < -0.1 is nighttime 
        -0.1 < ll < 0.1 is twilight
        >0.1 is day time
        """
        if not isinstance(time_minutes, int):
            raise TypeError("Expected time_minutes of {}, got {}".format(int, type(time_minutes)))
        yr_freq = 2*pi/minutes_in_year
        dy_freq = 2*pi/minutes_in_day

        cos_omgom   = cos(time_minutes*(yr_freq + dy_freq))
        sin_omgom   = sin(time_minutes*(yr_freq + dy_freq))

        if (lat==self._cache_lat and long==self._cache_lon):
            pass
        else:
            # calculate and cache these
            self._cache_lat = lat
            self._cache_lon = long
            self._cache_co_lat =  cos(lat)
            self._cache_co_lon =  cos(long)
            self._cache_sin_lat = sin(lat)
            self._cache_sin_lon = sin(long)


        light_level     = cos(yr_freq*time_minutes)*(cos_omgom*self._cache_co_lat*self._cache_co_lon*self._coax - sin_omgom*self._cache_co_lat*self._cache_sin_lon*self._coax - self._siax*self._cache_sin_lat)
        light_level    += sin(yr_freq*time_minutes)*(sin_omgom*self._cache_co_lat*self._cache_co_lon + cos_omgom*self._cache_co_lat*self._cache_sin_lon )
        light_level    *= -1

        return(light_level)

    def skip_time(self, amount):
        """
        Turns the clock forward by an amount of time.

        amount should be of type Time
        """

        if not isinstance(amount, Time):
            raise TypeError("Expected object of type {}, got {}.".format(Time, type(amount)))
        self._time.time_step( amount.minute, amount.hour, amount.day, amount.month, amount.year)

    def get_current_light_level(self, lat, lon):
        """
        Get the latitude and longitude at the current moment in time 
        """
        return( self.get_light_level( self.get_time_in_minutes(), lat,lon))

    def get_next_suntime( self, lat, lon):
        """
        Returns the time of the next sunrise or sunset 
        """
        ll = self.get_current_light_level(lat, lon)
        time = self.get_time_in_minutes()
        stepped = 0

        starts_positive = (ll > 0)

        while starts_positive==( ll > 0 ):
            if abs(ll) > 0.5:
                time += int(0.5*minutes_in_hour)
                stepped += int(0.5*minutes_in_hour)
            elif abs(ll) > 0.25:
                time += int(0.25*minutes_in_hour)
                stepped += int(0.25*minutes_in_hour)
            else:
                time += 1
                stepped += 1
            ll = self.get_light_level( time, lat, lon)

        
        return(  self.get_local_time(lon) + Time( minute = stepped) )

    def get_moon_visibility(self, long, current=True, time=None):
        """
        Returns a bool: True for visible, Fasle for not visible 
        """
        if current:
            time_minutes = self.get_time_in_minutes()
        else:
            if time is None:
                raise ValueError("If not asking for current, must provide time")
            if not isinstance(time, int):
                raise TypeError("Expected type {}, got {}".format(int, type(time)))
            time_minutes = time

        yr_freq = 2*pi/minutes_in_year
        dy_freq = 2*pi/minutes_in_day

        cos_lat     = 1
        sin_lat     = 0
        cos_lon     = cos(long)
        sin_lon     = sin(long)

        cos_omgom   = cos(time_minutes*(-1*yr_freq + dy_freq))
        sin_omgom   = sin(time_minutes*(-1*yr_freq + dy_freq))

        offset = self._lunar_offset*minutes_in_day
        length = self._lunar_length*minutes_in_day

        ang_velocity = 2*pi/length
        phase = 2*pi*(float(offset)/length)

        # \vec{M} = ( cos( ang*t + phase), sin(ang*t + phase), 0)

        moon     = cos(ang_velocity*time_minutes + phase)*(cos_omgom*cos_lon*self._coax - sin_omgom*sin_lon*self._coax)
        moon    += sin(ang_velocity*time_minutes + phase)*(sin_omgom*cos_lon + cos_omgom*sin_lon )

        if moon<0:
            return(False)
        else:
            return(True)

    def get_time_in_minutes(self):
        time = self._time.minute
        time += self._time.hour*minutes_in_hour
        time += self._time.day*minutes_in_day
        time += self._time.month*minutes_in_month
        time += self._time.year*minutes_in_year
        return(time)

    def __str__(self):
        return("{}\nThe moon is {}".format(self.get_local_time(0), self.get_moon_phase()) )

# utility for signaling 
class Signaler(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)

class MultiHexCalendar(QtWidgets.QWidget):
    """
    This implements a QtWidget for the MultiHex Calendar.
    It creates a little standard grid of days (buttons) below a month and a year switcher. 

    As it is, this doesn't really *do* anything. Later, I'll set it up so that this emits a signal when a day-button is pressed. The signal it emits should include the day the button has on it
    """
    def __init__(self, parent, time):
        """
        Initializes the widget. 

        The arg 'parent' is the widget's parent
        The arg 'time' is the starting time for the calendar. 
        """
        QtWidgets.QWidget.__init__(self, parent)
        if not isinstance(time, Time):
            raise TypeError("Expected {}, got {}".format(Time, type(time)))

        self.time = time

        self.setObjectName("MuliHexCalendar")
        self.layout = QtWidgets.QVBoxLayout(self)

        # define and add the year label and add the buttons beside it
        # TODO: (maybe) swap out the year label for something allowing easier large-scale year changes. 
        self.year_layout = QtWidgets.QHBoxLayout()
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

        # define and add the month combo box and the buttons beside it
        self.month_layout = QtWidgets.QHBoxLayout()
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

        # Add in the labels for hte weekdays
        weekday_lbls ={}
        self.weekday_list = QtWidgets.QHBoxLayout()
        for day in range(len(day_list)):
            weekday_lbls[day] = QtWidgets.QLabel(self)
            weekday_lbls[day].setText(day_list[day][:2])
            weekday_lbls[day].setObjectName(day_list[day])
            weekday_lbls[day].setAlignment(QtCore.Qt.AlignCenter)

            self.weekday_list.addWidget(weekday_lbls[day])
        self.layout.addItem(self.weekday_list)

        # we put all the buttons in place, and disable the ones that aren't needed
        # This way we don't have to add/remove buttons as necessary. Just enable/disable them and change the text 
        self.day_buttons = {}
        self.calendarGrid =  QtWidgets.QGridLayout()
        self.total_rows = int(days_in_month /len(day_list) ) + 1 #  make sure we have enough rows of buttons
        row = 0
        column = 0
        day = 0 # just a button counter...
        while row<=self.total_rows:
            self.day_buttons[day] = QtWidgets.QPushButton(self)
            self.day_buttons[day].setFixedSize(25,25)
            self.day_buttons[day].setText("")
            self.day_buttons[day].setEnabled(False)

            # this is weird, but is a little necessary necessary for scoping...
            # the function takes a day, and returns a function that accesses that day's text. We then connect the returned function to the button 
            def get_func(which):
                def funcy():
                    temp = self.day_buttons[which]
                    return( self.buttonPress(temp.text()) )
                return(funcy)
            # lambda(x : self.buttonPress( self.day_buttons[x]))
            self.day_buttons[day].clicked.connect( get_func(day) )
            #self.day_buttons[day].clicked.connect( lambda x : self.buttonPress( self.day_buttons[x]) )
            self.calendarGrid.addWidget(self.day_buttons[day],row,column)

            column+=1
            day+=1
            if column==(len(day_list)):
                column = 0
                row += 1
        self.days = day
        self.layout.addItem(self.calendarGrid)

        # Use the current time to choose which buttons to enable
        self.fill_days()

        self.month_combo.currentIndexChanged.connect(self.change_month)
        self.leftButton.clicked.connect(self.remove_year)
        self.rightButton.clicked.connect(self.add_year)
        self.leftButtonMon.clicked.connect(self.leftMon)
        self.rightButtonMon.clicked.connect(self.rightMon)

        # create a signal which is emitted when a button is pressed
        # this is the only way I know how to set up a emit - receive signal system. Used the same technique from the MultiThreading 
        # so it'll go //calendar.signals.signal.connect( function )//
        self.signals = Signaler()

    def fill_days(self):
        """
        This updates the buttons to the current year/month

        It scrolls over them until we get to the first day of the month: disabling buttons as it goes.
        It continues along, enabling buttons until it reaches the number of days in the month.
        Then carries on until all the rest of buttons are off. 
        """
        # total days is N

        counting = False
        days_so_far = 0
        day = 0 
        weekday_of_first_of_month = Time(year=self.time.year, month = self.time.month, day=0).get_day_of_week()

        while day < self.days:
            if day==weekday_of_first_of_month and days_so_far==0:
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

    def buttonPress(self, what):
        self.signals.signal.emit(what)


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



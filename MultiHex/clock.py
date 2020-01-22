# this class will be used to keep track of time

# in our fictional universe there are no timezones... no leap anything.
# it's a perfect clockwork universe. Hurray

# prefer the numpy version, but the default one is okay 
try:
    from numpy import floor
except ImportError:
    from math import floor

months = {}

minutes_in_hour = 60
hours_in_day    = 24
days_in_month   = 30
months_in_year  = 12

minutes_in_day   = minutes_in_hour*hours_in_day
minutes_in_month = minutes_in_day*days_in_month
minutes_in_year  = minutes_in_month*months_in_year

month_list = [  "January",
            "February",
            "March",
            "Aprtil",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December" ]

assert( len(month_list) == months_in_year )

class Clock:
    """
    Simple clock class to keep track of the time 
    """

    def __init__(self):
        # this counts the minutes through an entire year
        self._minutes = 0
        
        # this counts the year
        self._cyear     = False
        self._year      = 0
        self._cmonth    = False
        self._month     = 0
        self._cday      = False
        self._day       = 0
        self._chour     = False
        self._hour      = 0

    def month_str(self):
        """
        Returns the current month as a string
        """
        if type(self.month())!=int:
            raise TypeError("That's not right... month is type {}".format(type(self.month)))

        n_month = self.month()
        
        return( month_list[n_month] )

    def year(self):
        if self._cyear:
            pass
        else:
            self._year = int(floor(( self._minutes )/minutes_in_year))
            self._cyear = True
        return( self._year)

    def month(self):
        """
        Given the minutes elapsed in the year so far, return what month it is
        """
        if self._cmonth:
            pass
        else:
            self._month = int(floor((self._minutes - self.year()*minutes_in_year) / minutes_in_month ))
            self._cmonth = True
        return( self._month )


    def day(self):
        """
        Returns the day of the month as an int.
        """
        if self._cday:
            pass
        else:
            self._day   =  int(floor((self._minutes - self.year()*minutes_in_year - self.month()*minutes_in_month) / minutes_in_day ))
            self._cday = True
        return( self._day )

    def hour(self):
        """
        Returns the hour of the day (24 hour format) as an int. 
        """
        if self._chour:
            pass
        else:
            self._hour = int(floor( (self._minutes -self.year()*minutes_in_year - self.month()*minutes_in_month - self.day()*minutes_in_day) / minutes_in_hour ))
            self._chour = True
        return( self._hour )

    def minute(self):
        """
        Returns the current minute of the hour as an int. 
        """
        
        n_minutes =  self._minutes - self.year()*minutes_in_year - self.month()*minutes_in_month - self.day()*minutes_in_day - self.hour()*minutes_in_hour 
        return(n_minutes)
    

    def set_month(self, month): 
        """
        Turns the clock forward until the specified month. Month must be specified as an integer.
        """
        if type(month)!=int:
            raise TypeError("Month must be of type {}, reveived {}.".format(int, type(month)))
        difference = month -self.month()
        if difference<0:
            difference += months_in_year

        self.time_step(months=difference )

    def set_day(self, day ):
        """
        Turns the clock forward to the provided day. Day must be an int.
        """
        if type(day)!=int:
            raise TypeError("Object 'day' must be of type {}, received {}".format(int, type(day)))
        difference = day-self.day()
        if difference<0:
            difference += days_in_month

        self.time_step( days=difference )


    def set_year(self, year ):
        """
        Sets the year to specified year. Year must be provided as an int. 
        """
        if type(year)!=int:
            raise TypeError("Object 'year' must be of type {}, received {}".format(int, type(year)))
        self.time_step( years = year )


    def time_step(self, minutes=0, hours=0, days=0, months=0, years=0):
        """
        Move the current time forward by some number of minutes (or optionally years, months, etc)
        """

        self._minutes += years*minutes_in_year
        self._minutes += months*minutes_in_month
        self._minutes += days*minutes_in_day
        self._minutes += hours*minutes_in_hour
        self._minutes += minutes
        
        # these are no longer accurate! 
        self._cyear = False
        self._cmonth = False
        self._cday = False
        self._chour = False

    def get_moon_phase(self):
        """
        returns the current phase of the moon 
        
        Moon phase simplified to be exactly one month long.
        """

        # just so the moon phase isn't perfectly aligned with the weeks! 
        offset = 3*minutes_in_day
        length = 28*minutes_in_day

        phases = [  "New",
                    "Waxing Crescent",
                    "Waxing Gibbous",
                    "Full",
                    "Wanning Gibbous",
                    "Wanning Crescent"]

        total_days = int(floor((self._minutes/minutes_in_day)))
        days_through_cycle = (total_days - offset) % length 
        
        percent_through = float( days_through_cycle )/length
        which_part = int( percent_through * len(phases) )
        
        return( phases[which_part] )
         
    def __str__(self):
        return("It is {} {}, {}, at {:02d}:{:02d}\nThe moon is {}".format(self.month_str(), self.day(), self.year(), self.hour(), self.minute(), self.get_moon_phase()) )

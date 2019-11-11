# this class will be used to keep track of time

# in our fictional universe there are no timezones... no leap anything.
# it's a perfect clockwork universe. Hurray

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

class Clock:
    """
    Simple clock class to keep track of the time 
    """

    def __init__(self):
        # this counts the minutes through an entire year
        self._minutes = 0
        
        # this counts the year
        self.year   = 0

    def month_str(self):
        if type(self.month())!=int:
            raise TypeError("That's not right... month is type {}".format(type(self.month)))

        n_month = self.month()

        if n_month==0:
            return("January")
        elif n_month==1:
            return("February")
        elif n_month==2:
            return("March")
        elif n_month==3:
            return("April")
        elif n_month==4:
            return("May")
        elif n_month==5:
            return("June")
        elif n_month==6:
            return("July")
        elif n_month==6:
            return("August")
        elif n_month==8:
            return("September")
        elif n_month==9:
            return("October")
        elif n_month==10:
            return("November")
        elif n_month==11:
            return("December")


    def month(self):
        """
        Given the minutes elapsed in the year so far, return what month it is
        """
        n_months = int(floor((self._minutes / minutes_in_month) ))
        return( n_months )


    def day(self):
        n_days   =  int(floor((self._minutes - self.month()*minutes_in_month) / minutes_in_day ))
        return(n_days)

    def hour(self):
        n_hours = int(floor( (self._minutes - self.month()*minutes_in_month - self.day()*minutes_in_day) / minutes_in_hour ))
        return( n_hours )

    def minute(self):
        n_minutes =  self._minutes - self.month()*minutes_in_month - self.day()*minutes_in_day - self.hour()*minutes_in_hour 
        return(n_minutes)
    

    def set_month(self, month): 
        difference = month -self.month()
        if difference<0:
            difference += months_in_year

        self.time_step(months=difference )

    def set_day(self, day ):
        difference = day-self.day()
        if difference<0:
            difference += days_in_month

        self.time_step( days=difference )


    def set_year(self, year ):
        self._year = year


    def time_step(self, minutes=0, hours=0, days=0, months=0, years=0):
        """
        Move the current time forward by some number of minutes (or optionally years, months, etc)
        """
        self.year     += years
        self._minutes += months*minutes_in_month
        self._minutes += days*minutes_in_day
        self._minutes += hours*minutes_in_hour
        self._minutes += minutes
        
        while(self._minutes >= minutes_in_year):
            self.year += 1
            self._minutes -= minutes_in_year

        

    def __str__(self):
        return("It is {} {}, {}, at {:02d}:{:02d}".format(self.month_str(), self.day(), self.year, self.hour(), self.minute()) )

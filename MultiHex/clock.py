# this class will be used to keep track of time

# in our fictional universe there are no timezones... no leap anything.
# it's a perfect clockwork universe. Hurray


from math import pi, abs, floor
from math import cos, sin, arcsin, sqrt

months = {}

degrees = pi/180.

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

class Time:
    """
    Used to pass times around 
    """

    def __init__( self, hour, minute ):
        assert( minute>=0 and minutes<minutes_in_hour)
        assert( hour>=0 and hour<hours_in_day )

        morning = ( hour < hours_in_day/2  )

        self.hour = hour 
        self.minute = minute

    def __str__(self):
        if morning:
            if self.hour == 0:
                out = "12:{} AM".format( self.minute )
            else:
                out = "{}:{} AM".format( self.hour, self.minute )
        else: 
            if self.hour == 12:
                out = "12:{} PM".format( self.minute)
            else:
                out = "{}:{} PM".format( self.hour - hours_in_day/2 , self.minute)

        return( out )

class Clock:
    """
    Simple clock class to keep track of the time 
    """

    def __init__(self):
        # this counts the minutes through an entire year
        self._minute    = 0
        self._hour      = 0
        self._day       = 0
        self._month     = 0
        self._year      = 0

        self._axial_tilt = 17*degrees

    def month_str(self):
        """
        Returns the current month as a string
        """
        if type(self.month())!=int:
            raise TypeError("That's not right... month is type {}".format(type(self.month)))
        
        return( month_list[self._month] )

    def year(self):
        return( self._year )

    def month(self):
        """
        Given the minutes elapsed in the year so far, return what month it is
        """
        return( self._month )


    def day(self):
        """
        Returns the day of the month as an int.
        """
        return( self._day )

    def hour(self):
        """
        Returns the hour of the day (24 hour format) as an int. 
        """
        return( self._hour )

    def minute(self):
        """
        Returns the current minute of the hour as an int. 
        """
        
        return(self._minute)

    def _month_step(self, monthts):
        self._month = months + self._month

        while self._month >= months_in_year:
            self._year += 1
            self._month -= months_in_year

    def _day_step(self, days):
        self._day += days

        while self._day >= days_in_month:
            self._month_step( 1 )
            self._day-= days_in_month

    def _hour_step(self, hours):
        self._hour += hours

        while self._hour >= hours_in_day:
            self._day_step(1)
            self._hour -= hours_in_day


    def _minute_step(self, minutes):
        self._minute += minutes
        
        while self._minute >= minutes_in_hour:
            self._hour_step(1)
            self._minute -= minutes_in_hour

    def minute_of_day(self):
        return( self._minute + self._hour*minutes_in_hour )

    def days_of_year(self):
        return( self._day + self.month*months_in_year )

    def get_next_suntime(self, latitude):
        """
        Implements sunrise algorithm. Returns tuple of this day's (sunrise, sunset).

        @param latitude     - latitude of point for sunrise/set. Should be in RADIANS
        """
        assert( abs(latitude)<=pi )

        # representative of angle around sun
        alpha = 2*pi*float(self.days_of_year())/(days_in_month*months_in_year)
        
        # calculate the constants
        A = cos(alpha)*sin(latitude)
        B = sin(alpha)*cos(self._axial_tilt)*sin(latitude)
        C = sin(alpha)*sin(self._axial_tilt)*cos(latitude)

        under_root = 4*(C**2)*(B**2) + (A**2 + B**2)*(A**2 - C**2)
        
        # check if it's deep winter or summer 
        if under_root<0:
            if (latitude > 0) and ((pi/2)<alpha or alpha<(3*pi/2)):
                return("Sunny") # sunny 
            if (latitude < 0) and not ((pi/2)<alpha or alpha<(3*pi/2)):
                return() # sunny
            
            return() # dark

        soln_1 = arcsin( (2*C*B+sqrt(under_root))/( 2*A**2 + 2*B**2 ) )
        soln_2 = arcsin( (2*C*B-sqrt(under_root))/( 2*A**2 + 2*B**2 ) )

        if (alpha>pi/2) and (alpha<3*pi/2):
            if latitude>0:
                pass
            else:
                pass
        else:
            pass


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

# this class will be used to keep track of time

# it's a perfect clockwork universe. Hurray


from math import pi, floor
from math import cos, sin, sqrt

from numpy import arcsin, arccos

degrees = pi/180.

minutes_in_hour = 60
hours_in_day    = 24
days_in_month   = 35
months_in_year  = 12

minutes_in_day   = minutes_in_hour*hours_in_day
minutes_in_month = minutes_in_day*days_in_month
minutes_in_year  = minutes_in_month*months_in_year

month_list = [ "January",
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


day_list = [ "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"]



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

    def __init__( self , hour=0, minute=0, month=0, day = 0,year = 0,date=True):
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
        new = Time(self.hour, self.minute, self.month, self.day, self.year)
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
        new = Time(self.hour, self.minute, self.month, self.day, self.year)
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
        
        #self.time_step(Time(hour=int(0.5*hours_in_day)))
    
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

    def skip_to_time(self, what_time):
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
            self.time_step(Time( day = (days_to_skip - 1  )))

        # default time is midnight
        # skip to then
        self.skip_to_time( Time() )

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

        self._time.time_step(lapse.minute, lapse.hour, lapse.day, lapse.month, lapse.year)

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
            return( arccos( ll ) )

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

        cos_lat     = cos(lat)
        sin_lat     = sin(lat)
        cos_lon     = cos(long )
        sin_lon     = sin(long )

        light_level     = cos(yr_freq*time_minutes)*(cos_omgom*cos_lat*cos_lon*self._coax - sin_omgom*cos_lat*sin_lon*self._coax - self._siax*sin_lat)
        light_level    += sin(yr_freq*time_minutes)*(sin_omgom*cos_lat*cos_lon + cos_omgom*cos_lat*sin_lon )
        light_level    *= -1

        return(light_level)

    def time_step(self, amount):
        """
        Turns the clock forward by an amount of time.

        amount should be of type Time
        """
        #self._time.time_step( minutes, hours, days, months, years)
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


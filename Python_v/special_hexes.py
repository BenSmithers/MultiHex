from hex import Hex
from point import Point

default_p = Point(0.0,0.0)

def Ocean_Hex(center, radius):
    temp = Hex(center, radius)
    temp.fill = 'powderblue'
    temp._temperature_base = 0.5
    temp._humidity_base    = 1.0
    temp._altitude_base    = 0.0
    temp._is_land          = False
    return(temp) 

def Grassland_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = 'green3'
    return(temp)

def Forest_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = 'forest green'
    return(temp)

def Mountain_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = 'thistle4'
    return(temp)

def Arctic_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = 'snow'
    temp._temperature_base = 0.0
    temp._humidity_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Desert_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = 'goldenrod'
    temp._temperature_base = 1.0
    temp._humidity_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)



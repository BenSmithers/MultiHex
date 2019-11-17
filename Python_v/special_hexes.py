from hex import Hex
from point import Point

default_p = Point(0.0,0.0)

def Ocean_Hex(center, radius):
    temp = Hex(center, radius)
    temp.fill = (91,201,192)
    temp._temperature_base = 0.5
    temp._humidity_base    = 1.0
    temp._biodiversity     = 1.0
    temp._altitude_base    = 0.0
    temp._is_land          = False
    return(temp) 

def Grassland_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = (149,207,68)
    temp._is_land = True
    return(temp)

def Forest_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = (27,110,11)
    return(temp)

def Mountain_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = (158,140,96)
    return(temp)

def Arctic_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = (171,224,224)
    temp._temperature_base = 0.0
    temp._humidity_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Desert_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = (230,178,110)
    temp._temperature_base = 1.0
    temp._humidity_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)



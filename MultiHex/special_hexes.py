from MultiHex.hex import Hex
from MultiHex.point import Point

"""
Defines some presets for drawing hexes. 

For the most part this is just used to set the colors... 
"""

default_p = Point(0.0,0.0)

class hcolor:
    def __init__(self):
        self.ocean = (91,201,192)
        self.grass = (149,207,68)
        self.fores = (36, 94, 25)
        self.arcti = (171,224,224)
        self.mount = (158,140,96)
        self.ridge = (99,88,60)
        self.deser = (230,178,110)
        self.rainf = (22,77,57)
        self.savan = (170, 186, 87)
colors = hcolor()

def Ocean_Hex(center, radius):
    temp = Hex(center, radius)
    temp.fill = colors.ocean
    temp._temperature_base = 0.5
    temp._rainfall_base    = 1.0
    temp._biodiversity     = 1.0
    temp._altitude_base    = 0.0
    temp._is_land          = False
    return(temp) 

def Grassland_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = colors.grass
    temp._is_land = True
    return(temp)

def Forest_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = colors.fores
    return(temp)

def Mountain_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = colors.mount
    temp.genkey = '11000000'
    return(temp)

def Arctic_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = colors.arcti
    temp._temperature_base = 0.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Desert_Hex(center,radius):
    temp = Hex( center, radius )
    temp.fill = colors.deser
    temp._temperature_base = 1.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)




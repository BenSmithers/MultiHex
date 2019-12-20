from MultiHex.core import Hex, Point, Region, Path
from MultiHex.core import RegionMergeError, RegionPopError
from MultiHex.tools import basic_tool, hex_brush

from PyQt5 import QtGui

"""
Implements the overland map type, its brushes, and its hexes 

Objects:
    River           - Path implementation
    Biome           - Region implementation for, well, biomes
    region_brush    - basic tool, makes regions
    hex_brush       - basic tool, makes hexes
    OHex            - Hex implementation for land hexes
"""

class River(Path):
    """
    Implements `Path`
    """
    def __init__(self, start):
        Path.__init__(self, start)
        self.color = (colors.ocean[0]*0.8, colors.ocean[1]*0.8, colors.ocean[2]*0.8)

        self.width = 1

        # by default, should have none
        self.tributaries = None

        self._max_len = 20

    def join_with( self, other ):
        """
        Joins with the other river! 

        Other river must connect to this one 
        """
        if not isinstance( other, River ):
            raise TypeError("Cannot join with object of type {}".format(type(other)))

        # make sure these rivers are join-able. One river needs to have its end point on the other! 
        if other.end() not in self._vertices:
            # try joining with its tributaries 
            if other.tributaries is not None:
                error_code = self.tributaries[0].join_with( other )
                if error_code == 0:
                    return(0)
                error_code = self.tributaries[1].join_with( other )
                if error_code == 0:
                    return(0) 
                
                # failed to join other river with itself or its tributaries 
                return( 1 )
            else:
                return( 1)

        # other one ends in this one
        tributary_1 = other
        # going to define a tributary 
        tributary_2 = River( self.start() )

        # Merge part of the self into the new tributary 
        intersect = self.vertices.index( other.end() )
        
        tributary_2._vertices = self.vertices[: (intersect+1)]
        tributary_2.tributaries = self.tributaries 

        self.trim_at( intersect, keep_upper=False )
 
        # modify the self
        self.tributaries = [ tributary_1, tributary_2 ]
        self.tributaries[0].width = other.width
        self.tributaries[1].width = self.width

        self.width = other.width + self.width 

        # success code 
        return(0)

class Biome(Region):
    """
    Implementation of the region class for regions of similar geography. 

    Biomes! Like forests, deserts, etc...  
    """
    def __init__(self, hex_id, parent):
        Region.__init__(self, hex_id, parent)



default_p = Point(0.0,0.0)

class OHex_Brush( hex_brush ):
    def __init__(self, parent):
        hex_brush.__init__(self, parent)
        self._brush_type = Grassland_Hex

        self._river_drawn = []

    def redraw_rivers( self ):
        """
        all the rivers
        """
        # self._river_drawn

        def draw_river(river):

            if river.tributaries is not None:
                draw_river( river.tributaries[0] )
                draw_river( river.tributaries[1] )

            self.QBrush.setStyle(0)
            self.QPen.setStyle(1)
            self.QPen.setWidth(3 + river.width)
            self.QPen.setColor( QtGui.QColor( river.color[0], river.color[1], river.color[2] ) )
            path = QtGui.QPainterPath()
            outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( river.vertices  ) )
            path.addPolygon(outline)
            self._river_drawn.append(self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush))
            self._river_drawn[-1].setZValue(2)

        for river in self.parent.main_map.paths['rivers']:
            assert( isinstance( river, River) )
            draw_river( river )

    def update_selection(self):
        self.set_sliders( self._selected_id )

    # set the sliders! 
    def set_sliders(self, this_id ):
# set the sliders 
        self.parent.ui.rainfall.setValue(    max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._rainfall_base*100    )))) 
        self.parent.ui.temperature.setValue( max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._temperature_base*100 ))))
        self.parent.ui.biodiversity.setValue(max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._biodiversity*100     ))))

    # these functions will be called to scale a selected hexes' properties using the sliders 
    def rainfall(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self._selected_id]._rainfall_base = float(value)/100.
    def temperature(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self._selected_id]._temperature_base = float(value)/100.
    def biodiversity(self, value):
        if self.selected_id is not None:
            self.parent.main_map.catalogue[self._selected_id]._biodiversity_base = float(value)/100.
    
    # What kind of template to use when drawing 
    def switch_forest(self):
        self._brush_type = Forest_Hex
    def switch_grass(self):
        self._brush_type = Grassland_Hex
    def switch_mountain(self):
        self._brush_type = Mountain_Hex
    def switch_desert(self):
        self._brush_type = Desert_Hex
    def switch_ocean(self):
        self._brush_type = Ocean_Hex
    def switch_arctic(self):
        self._brush_type = Arctic_Hex
    def switch_ridge(self):
        self._brush_type = Ridge_Hex
    
    # DIE
    def drop(self):
        if self.parent.main_map._outline is not None:
            self.parent.scene.removeItem( self._outline_obj )
            self._outline_obj = None
        if self._selected_out is not None:
            self.parent.scene.removeItem( self._selected_out )
            self._selected_out = None
        self._selected_id = None

 


    
class OHex(Hex):
    """
    Overland Hex implementation

    Adds criteria to define how that hex is! 
    """
    def __init__(self, center=default_p, radius=1.0):
        Hex.__init__(self, center, radius)
        
        self._biodiversity     = 1.0
        self._rainfall_base    = 0.0
        self._altitude_base    = 1.0
        self._temperature_base = 1.0
        self._is_land          = True
        self.biome = ""
    
        # CW downstream , CCW downstream, runs through
        self.river_border = [ False ,False , False]

    def rescale_color(self):
        self.fill  = (min( 255, max( 0, self.fill[0]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[1]*( 1.0 + 0.4*(self._altitude_base) -0.2))),
                        min( 255, max( 0, self.fill[2]*( 1.0 + 0.4*(self._altitude_base) -0.2))))


class hcolor:
    """
    Just a utility used to hold a bunch of colors 
    """
    def __init__(self):
        self.ocean = (100,173,209)
        self.grassland = (149,207,68)
        self.forest = (36, 94, 25)
        self.arctic = (171,224,224)
        self.tundra = (47,105,89)
        self.mountain = (158,140,96)
        self.ridge = (99,88,60)
        self.desert = (230,178,110)
        self.rainforest = (22,77,57)
        self.savanah = (170, 186, 87)
        self.wetlands = (30,110,84)
colors = hcolor()


# Tons of hex templates... 
def Ocean_Hex(center, radius):
    temp = OHex(center, radius)
    temp.fill = colors.ocean
    temp._temperature_base = 0.5
    temp._rainfall_base    = 1.0
    temp._biodiversity     = 1.0
    temp._altitude_base    = 0.0
    temp._is_land          = False
    return(temp) 

def Grassland_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.grassland
    temp._is_land = True
    return(temp)

def Forest_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.forest
    temp._is_land = True
    return(temp)

def Mountain_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.mountain
    temp.genkey = '01000000'
    temp._is_land = True
    return(temp)

def Arctic_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.arctic
    temp._temperature_base = 0.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Desert_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.desert
    temp._temperature_base = 1.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Ridge_Hex(center, radius):
    temp = OHex( center, radius )
    temp.fill = colors.ridge
    temp.genkey = '11000000'
    temp._is_land = True
    return(temp)



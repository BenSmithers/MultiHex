from MultiHex.core import Hex, basic_tool, Point, Region, Path
from MultiHex.core import RegionMergeError, RegionPopError

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsDropShadowEffect, QGraphicsItem, QGraphicsPolygonItem

"""
Implements the overland map type, its brushes, and its hexes 

Objects:
    River           - Path implementation
    Biome           - region for, well, biomes
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
        self.color = hcolor.ocean 
        
        self.width = 1

        # by default, should have none
        self.tributaries = None

    def join_with( self, other ):
        """
        Joins with the other river. Makes this object the 'lower' part of the river, with the tributaries higher up

        """
        if not isinstance( other, River ):
            raise TypeError("Cannot join with ")

        # make sure these rivers are join-able. One river needs to have its end point on the other! 
        r_type = None
        if other._vertices[-1] in self._vertices:
            r_type = 1
        elif self._vertices[-1] in other._vertices:
            r_type = 2
        else:
            raise ValueError("One river must end on another one")

        if r_type==1:
            # other one ends in this one
            tributary_1 = other
            # going to define a tributary 
            tributary_2 = River( self._vertices[0]  )

            # Merge part of the self into the new tributary 
            intersect = self._ververtices.index( other._vertices[-1] )
            tributary_2._vertices = self._vertices[: intersect+1]
            tributary_2.tributaries = self.tributaries 

        else:
            intersect = other.index( self._vertices[-1] )

            # use the 'other' object, part of it, to make the tributary 
            tributary_1 = other._vertices[: intersect+1]
            tributary_1.tributaries = other.tributaries

            # now use the former self to make another tributary 
            tributary_2 = River( self.vertices[0] )
            tributary_2._vertices = self._vertices
            tributary_2.tributaries = self.tributaries 


        # modify the self
        self._vertices = other._vertices[intersect:]
        self.tributaries = [ tributary_1, tributary_2 ]

        self.tributaries[0].width = other.width
        self.tributaries[0].width = self.width
        self.width = other.width + self.width 

class Biome(Region):
    """
    Implementation of the region class for regions of similar geography. 

    Biomes! Like forests, deserts, etc...  
    """
    def __init__(self, hex_id, parent):
        Region.__init__(self, hex_id, parent)


class region_brush(basic_tool):
    """
    basic_tool implementation used to draw and register regions on a canvas/hexmap 
    """

    def __init__(self, parent):
        """
        @ param parent - the gui object that will hold this 
        """
        self.start = Point(0.0, 0.0)
        self.selected_rid = None

        self.parent = parent
        self._writing = True
        self._brush_size = 1

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
        self.QBrush.setStyle(6)
        self.QPen.setWidth(3)


        self._outline_obj = None
        self._drawn_regions = {} # map from rid to drawn region
        self._drawn_names = {}

    def _set_color(self, color):
        """
        Sets the brush and pen to a specified color. The brush is only partially opaque 

        @param color    - the specified color. Needs to be an length-3 indexable with integer entries >0 and < 255
        """
        if len(color)<3:
            raise ValueError("")
        for entry in color:
            if type(entry)!=int:
                raise TypeError("For {} in {}, expected type {} but got {}".format(entry, color, int, type(entry)))

            if entry<0 or entry>255:
                raise ValueError("Entry {} in {} should be valued between 0 and 255".format(entry, color))

        self.QBrush.setColor(QtGui.QColor( color[0], color[1], color[2], 60))
        self.QPen.setColor( QtGui.QColor(color[0], color[1], color[2])) 
    def set_brush_size( self, size ):
        if not type(size)==int: 
            raise TypeError("Can't set brush size to type {}, expected {}".format(type(size), int))
        # not actually doing anything...
    
        if size==1:
            self._brush_size = 1
        elif size==2:
            self._brush_size= 2
        else:
            raise ValueError("Can't set brush size to {}".format(size))

    def select(self, event):
        """
        Selects the region under the cursor. If no region is there, deselect whatever region is active 
        """
        here = Point( event.scenePos().x(), event.scenePos().y())        
        this_id = self.parent.main_map.get_id_from_point( here )
        
        if this_id not in self.parent.main_map.id_map:
            self.selected_rid = None
            self.parent.ui.RegEdit.setText("")
        else:
            if self.parent.main_map.id_map[this_id]!=self.selected_rid:

                self.selected_rid = self.parent.main_map.id_map[this_id]
                self.parent.ui.RegEdit.setText(self.parent.main_map.rid_catalogue[self.selected_rid].name)

    def hold(self, event):
        self.activate( event )

    def activate(self, event):
        """
        Right click 
        """
        if self._writing:
            self.reg_add(event)
        else:
            self.reg_remove(event)
    def toggle_mode(self, force=None):
        """
        Switches brush sizes, the region remover only works with brush size 1, so... force the brush size back to 1. 
        """
        if (force is not None) and (type(force)==bool):
            self._writing = force
            if force==False:
                self._brush_size = 1
        else:
            if self._writing:
                self._writing = False
                self._brush_size = 1
            else:
                self._writing = True
    def move(self, event):
        """
        While moving it continuously removes and redraws the outline - reimplimentation of the 'move' function in the hex brush
        """
        # get center, 
        place = Point( event.scenePos().x(), event.scenePos().y())
        center_id = self.parent.main_map.get_id_from_point( place )
        
        self.QPen.setWidth(5)
        self.QPen.setStyle(1)

#        self._brush_size = 1

        if self.parent.main_map._outline == center_id:
            # the mouse hasn't moved, skip this
            pass
        else:
            # new center! 
            self.parent.main_map._outline = center_id

            # get the outline
            outline = self.parent.main_map.get_neighbor_outline( center_id , self._brush_size)

            # if we're writing draw green, if erasing draw red 
            if self._writing:
                self.QBrush.setStyle(6)
                if self.selected_rid is not None:
                    self._set_color( self.parent.main_map.rid_catalogue[ self.selected_rid ].color)
                else:
                    self.QPen.setColor(QtGui.QColor(114,218,232))
            else:
                self.QPen.setColor(QtGui.QColor(220,20,20))
                self.QBrush.setColor(QtGui.QColor(220,20,20,170))
                self.QBrush.setStyle( 14 )


            # remove previous outline object
            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
            # redraw the selection outline

            self.QBrush.setStyle(0)
            self._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )
            self._outline_obj.setZValue( 4 )

    def reg_add(self, event):
        """
        Add to a region. If the brush size is 1, it just tries to add that hex to the active region. If there's no active region, it creates a region there. If the brush size is 2 it makes a temporary region around the cursor and merges the surrounding hexes with the temp region. Then it merges the temp region and active region together. 
        """
        # set up the pen and brush to draw a region
        
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )
        
        if loc_id not in self.parent.main_map.catalogue:
            return


        if self.selected_rid is None:
            # if the hex here is not mapped to a registered region, 
            if (loc_id not in self.parent.main_map.id_map):
                # make a new region here, set it to the active region, and draw it
                new_reg = Region( loc_id, self.parent.main_map )
                                
                # get the newely created rid, set it to active 
                self.selected_rid = self.parent.main_map.register_new_region( new_reg )
                
                # self.parent.main_map.id_map( loc_id )
                
                if self._brush_size == 2:
                    # build a new region around this one
                    for ID in self.parent.main_map.get_hex_neighbors( loc_id ):
                        self.parent.main_map.add_to_region( self.selected_rid, ID )

                self.redraw_region( self.selected_rid )
            else:
                # no active region, but the hex here belongs to a region. 
                # set this hexes' region to the active one 
                self.selected_rid = self.parent.main_map.id_map[ loc_id ]
        else:
            if self._brush_size==1:
                try:
                    # try adding it
                    # if it can't, it raises a RegionMergeError exception
                    other_rid = self.parent.main_map.add_to_region(self.selected_rid, loc_id )
                    
                    if (other_rid!=-1) and (other_rid is not None): 
                        # add_to_region returns an rid if it removes a hex from another region.
                        # it returns -1, it didn't remove anything from anywhere 
                        self.redraw_region( other_rid )
                    self.redraw_region( self.selected_rid )
                except RegionMergeError:
                    pass
                except RegionPopError:
                    pass
            elif self._brush_size==2:
                # This seems to cause some instability...
                # ...
                if loc_id not in self.parent.main_map.id_map:
                    # create and register a region
                    temp_region = Region( loc_id , self.parent.main_map )
                    new_rid = self.parent.main_map.register_new_region( temp_region )

                    for ID in self.parent.main_map.get_hex_neighbors( loc_id ):
                        try:
                            self.parent.main_map.add_to_region( new_rid, ID )
                        except (RegionMergeError, RegionPopError):
                            pass

                    # now merge the regions 
                    self.parent.main_map.merge_regions( self.selected_rid, new_rid )
                    self.redraw_region( self.selected_rid )
                    #for ID in temp_region.ids:
                    #    print("Failed here")
                    #    self.parent.main_map.remove_from_region( ID )

    def reg_remove(self, event):
        """
        Tries to remove the hex under the cursor from its region.
        """
        place   = Point( event.scenePos().x(), event.scenePos().y() )
        loc_id  = self.parent.main_map.get_id_from_point( place )
        if loc_id not in self.parent.main_map.catalogue:
            return

        if loc_id not in self.parent.main_map.id_map:
            # nothing to pop
            return
        else:
            # get this hexes's region id 
            this_rid = self.parent.main_map.id_map[ loc_id ]
            # remvoe this hex from that region
            try:
                self.parent.main_map.remove_from_region( loc_id )
                # redraw that region
                self.redraw_region( this_rid )
            except RegionPopError:
                pass

    def redraw_region(self, reg_id ):
        """
        Redraws the region with the provided region ID.

        @ param reg_id  - region id if region to redraw.
        """

        #self.QBrush.setStyle(6)
        self.QBrush.setStyle(1)
        self.QPen.setWidth(3)
        

        if reg_id in self._drawn_regions:
            self.parent.scene.removeItem( self._drawn_regions[ reg_id ] )
        
        reg_obj = self.parent.main_map.rid_catalogue[ reg_id ]
        self._set_color( reg_obj.color )

        path = QtGui.QPainterPath()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( reg_obj.perimeter + [reg_obj.perimeter[0]] ) )
        path.addPolygon( outline )

        for enclave in reg_obj.enclaves:
            enc_path = QtGui.QPainterPath()
            enc_outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw(enclave+[enclave[0]])) 
            enc_path.addPolygon( enc_outline )
            path = path.subtracted( enc_path )
        
        self._drawn_regions[reg_id] = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush)
        self._drawn_regions[reg_id].setZValue(2)
        self.redraw_region_text( reg_id )

    def redraw_region_text( self, rid ):
        """
        Redraws the name of the region with the provided region id

        @param rid  - region id of region whose name should be redrawn
        """
        reg_obj = self.parent.main_map.rid_catalogue[ rid ]

        if reg_obj.name=="":
            return

        dname = reg_obj.name.split(" ")
        mult_factor = 1
        if len(dname)>=6:
            split = int(len(dname)/2)
            mult_factor = 2
            dname = " ".join(dname[0:split])+"\n"+ " ".join(dname[split:])
        else:
            dname = " ".join(dname)

        if rid in self._drawn_names:
            self.parent.scene.removeItem( self._drawn_names[ rid ] )
        
        drop = QGraphicsDropShadowEffect()
        drop.setOffset(1)
        center, extent = reg_obj.get_center_size()
        font = QtGui.QFont("Fantasy")
        font_size = mult_factor*max( 12, int(extent.magnitude / len(reg_obj.name)))
        font.setPointSize( font_size )

        self._drawn_names[rid] = self.parent.scene.addText( dname, font )
        self._drawn_names[rid].setPos( center.x - 0.5*extent.x, center.y )
        #new_color = QtGui.QColor( 0.5*(255+reg_obj.color[0]), 0.5*(255+reg_obj.color[1]), 0.5*(255+reg_obj.color[0]))
        new_color= QtGui.QColor( 250, 250, 250)
        self._drawn_names[rid].setDefaultTextColor( new_color )
        self._drawn_names[rid].setGraphicsEffect( drop )
        self._drawn_names[rid].setZValue(10)
    
    def drop(self):
        """
        Removes the selection outline for the tool. Called while switching to another tool. 
        """
        if self._outline_obj is not None:
            self.parent.scene.removeItem( self._outline_obj )


class hex_brush(basic_tool):
    """
    Another tool with clicker-control interfacing used to paint hexes on a hexmap. 

    Keeps track of all the canvas objects that it has drawn. Theres are **not** actual Hex's (TM), but just boring ass hexagons. 
    """
    def __init__(self, parent):
        self.writing = True
        self._brush_type = Grassland_Hex
        self._brush_size = 1

        self.pen_style = 0
        self.pen_size = 2

        self.parent = parent

        self.drawn_hexes = {}
        self._outline_obj = None

        self._selected_id = None
        self._selected_out = None 

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()

        # Part of a failed experiment. Leaving in case I pick it up again
        #self.layer = QGraphicsLayer()
        #self.layer.show()
        #self.layer.setVisible(True)
        #self.parent.scene.addItem( self.layer )

    def activate(self, event):
        if self.writing:
            self.write(event)
        else:
            self.erase(event)
    def hold(self, event):
        self.activate(event)
    
    def move(self, event):
        """
        While moving it continuously removes and redraws the outline
        """
        # get center, 
        place = Point( event.scenePos().x(), event.scenePos().y())
        center_id = self.parent.main_map.get_id_from_point( place )
        self.QPen.setWidth(5)
        self.QPen.setStyle(1)

        if self.parent.main_map._outline == center_id:
            # the mouse hasn't moved, skip this
            pass
        else:
            # new center! 
            self.parent.main_map._outline = center_id

            # get the outline
            outline = self.parent.main_map.get_neighbor_outline( center_id , self._brush_size)

            # if we're writing draw green, if erasing draw red 
            if self.writing:
                t_color = self._brush_type(Point(0,0), 1.0).fill
                self.QPen.setColor(QtGui.QColor(t_color[0], t_color[1], t_color[2]))
                self.QBrush.setStyle(1)
                self.QBrush.setColor(QtGui.QColor(t_color[0], t_color[1], t_color[2], 160))
            else:
                self.QBrush.setStyle(0)
                self.QPen.setColor(QtGui.QColor(255,15,15))

            # remove previous outline object
            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
            # redraw the selection outline


            self._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )
            self._outline_obj.setZValue(4)
    
    def erase(self, event):
        """
        First, it tries removing the picture on the canvas, and then unregistering that point's ID from the hex catalog
                obviously there may not be a hex at that ID. So just ignore when that happens 
        
        Then if relevant it does that again to all the neighboring points 
        """
        place = Point(event.scenePos().x(),event.scenePos().y() )
        loc_id = self.parent.main_map.get_id_from_point( place )
        try:
            self.parent.scene.removeItem( self.drawn_hexes[ loc_id ] ) 
            del self.drawn_hexes[loc_id]
            self.parent.main_map.remove_hex(loc_id)
        except KeyError:
            pass 

        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors(loc_id)
            for neighbor in neighbors:
                try:
                    self.parent.scene.removeItem( self.drawn_hexes[neighbor])
                    del self.drawn_hexes[neighbor]
                    self.parent.main_map.remove_hex( neighbor )
                except KeyError:
                    pass

    def write(self, event):
        """
        Like the eraser, but for writing. Gets the ID for the point under the cursor, builds a hex there, and tries registering it. If successfull, it then draws the hex. 

        Same story for larger brush size. Try building and registering hexes for all the IDs neighboring the central ID 

        """
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )

        # calculate the center of a hex that would have that id
        new_hex_center = self.parent.main_map.get_point_from_id( loc_id )
        # create a hex at that point, with a radius given by the current drawscale 
        new_hex= self._brush_type( new_hex_center, self.parent.main_map._drawscale )
        
        
        # register that hex in the hexmap 
        try:
            self.parent.main_map.register_hex( new_hex, loc_id )
            self.redraw_hex( loc_id )
        except NameError: # error registering hex. Das ok 
            pass
        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = self.parent.main_map.get_point_from_id( neighbor )
                new_hex = self._brush_type( new_hex_center, self.parent.main_map._drawscale)
                try:
                    self.parent.main_map.register_hex( new_hex, neighbor )            
                    self.redraw_hex( neighbor )
                except NameError:
                    pass
    def redraw_hex(self, hex_id):
        try:
            # if this hex has been drawn, redraw it! 
            if hex_id in self.drawn_hexes:
                self.parent.scene.removeItem( self.drawn_hexes[hex_id] )

            # get the pen ready (does the outlines)
            # may raise key error 
            this_hex = self.parent.main_map.catalogue[ hex_id ]
            self.QPen.setColor(QtGui.QColor( this_hex.outline[0], this_hex.outline[1], this_hex.outline[2] ))
            self.QBrush.setStyle(1)
 
            self.QPen.setWidth(self.pen_size)
            self.QPen.setStyle(self.pen_style)

            self.QBrush.setColor( QtGui.QColor( this_hex.fill[0], this_hex.fill[1], this_hex.fill[2] ))
            self.drawn_hexes[hex_id] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( this_hex._vertices )), pen=self.QPen, brush=self.QBrush) 
            self.drawn_hexes[hex_id].setZValue(1)

            # Part of a failed experiment. Leaving it here in case I pick it up again. 
            
            #path = QtGui.QPainterPath()
            #this_poly = QtGui.QPolygonF( self.parent.main_map.points_to_draw( this_hex._vertices ))
#            path.addPolygon( this_poly )

            #self.drawn_hexes[hex_id] = self.layer.addPath( path, self.QPen, self.QBrush)

            #self.drawn_hexes[hex_id] = QGraphicsPolygonItem(this_poly , self.layer )
            #self.drawn_hexes[hex_id].setPen( self.QPen )
            #self.drawn_hexes[hex_id].setBrush(self.QBrush)
            #self.layer.addItem( self.drawn_hexes[hex_id] )
        except KeyError: #happens if told to redraw a hex that isn't there 
            #print("key error")
            pass





    def select(self,event):
        self.QBrush.setStyle(0)
        self.QPen.setColor(QtGui.QColor(75,75,245))
        self.QPen.setWidth(4)

        here = Point( event.scenePos().x(), event.scenePos().y())
        this_id = self.parent.main_map.get_id_from_point( here )

        # only bother doing things if this is a new hex we're clicking on
        if self._selected_id != this_id:
            if self._selected_out is not None:
                # so, if there already is an outline (there should be), let's erase it. We're going to draw a new hex
                self.parent.scene.removeItem( self._selected_out )
            
            # okay, now verify that we're clicking on a registered hex 
            if this_id in self.parent.main_map.catalogue:
                # draw a new hex, and select its id 
                self._selected_out = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( self.parent.main_map.catalogue[this_id]._vertices)), pen = self.QPen, brush=self.QBrush )
                self._selected_out.setZValue(4)
                self._selected_id = this_id

                # set the sliders 
                self.parent.ui.rainfall.setValue(    max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._rainfall_base*100    )))) 
                self.parent.ui.temperature.setValue( max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._temperature_base*100 ))))
                self.parent.ui.biodiversity.setValue(max( 0, min( 100, int(self.parent.main_map.catalogue[this_id]._biodiversity*100     ))))
            else:
                # the outline object needs to be purged, otherwise it will later try erasing it again
                # we also undo our selection 
                self._selected_out = None
                self._selected_id = None
            
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

    def toggle_brush_size(self):
        """
        Only here to support the outdated ridge gui 
        """
        if self._brush_size == 2:
            self._brush_size = 1
        else:
            self._brush_size = 2

    def set_brush_size(self, size):
        if type(size)!=int:
            raise TypeError("Invalid size type {}".format(size))

        if (size>0) and (size<3):
            self._brush_size = size
        else:
            raise ValueError("Cannot set brush size to {}".format(size))

    def toggle_mode(self, force= None):
        if (force is not None) and (type(force)==bool):
            self.writing = force
        else:
            if self.writing:
                self.writing = False # erasing 
            else:
                self.writing = True

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
            self.parent.ui.rainfall.setValue( 0 )
            self.parent.ui.temperature.setValue( 0 )
            self.parent.ui.biodiversity.setValue( 0 )
        self._selected_id = None


default_p = Point(0.0,0.0)

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
        self.grass = (149,207,68)
        self.fores = (36, 94, 25)
        self.arcti = (171,224,224)
        self.mount = (158,140,96)
        self.ridge = (99,88,60)
        self.deser = (230,178,110)
        self.rainf = (22,77,57)
        self.savan = (170, 186, 87)
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
    temp.fill = colors.grass
    temp._is_land = True
    return(temp)

def Forest_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.fores
    return(temp)

def Mountain_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.mount
    temp.genkey = '01000000'
    return(temp)

def Arctic_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.arcti
    temp._temperature_base = 0.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Desert_Hex(center,radius):
    temp = OHex( center, radius )
    temp.fill = colors.deser
    temp._temperature_base = 1.0
    temp._rainfall_base    = 0.0
    temp._altitude_base    = 0.0
    temp._is_land          = True
    return(temp)

def Ridge_Hex(center, radius):
    temp = OHex( center, radius )
    temp.fill = colors.ridge
    temp.genkey = '11000000'
    return(temp)



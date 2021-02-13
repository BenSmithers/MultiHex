from PyQt5.QtWidgets import QGraphicsScene, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QMainWindow, QMenu, QGraphicsView, QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5 import QtGui, QtCore, QtWidgets


from MultiHex.core import Point, Region, RegionMergeError, RegionPopError, Path, Hex
from MultiHex.objects import Icons, Entity, Mobile, Settlement
from MultiHex.logger import Logger
# from MultiHex.map_types.overland import Road, River


import os # used for some of the icons

from math import sqrt, pi
rthree =  sqrt(3)

class EntityDialogGUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600,400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")

        self.tabs = []

        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Entity Editor"))

class EntityDialog(QtWidgets.QDialog):
    def __init__(self,parent, config_object):
        super(EntityDialog, self).__init__(parent)
        self.ui = EntityDialogGUI()
        self.ui.setupUi(self)

        if not isinstance(config_object, Entity):
            raise TypeError("Cannot configure {} object!".format(type(config_object)))
        
        # yeah the syntax here is really ugly, but this function is a static method so it can also be called on 
        #  an un-instantiated class 
        
        # this returns a list of widgets, each of which gets its own tab! 
        widget_list = config_object.widget(config_object)
        for entry in widget_list:
            newtab = QtWidgets.QWidget(self)
            
            layout = QtWidgets.QVBoxLayout(newtab)
            this_widg = entry(newtab, config_object)
            newtab.setObjectName( this_widg.objectName() )
            layout.addWidget(this_widg)
            newtab.setLayout(layout)

            self.ui.tabWidget.addTab(newtab, this_widg.objectName())
            self.ui.tabs.append(newtab)


class MultiHexAction(QAction):
    def __init__(self, name, id=None):
        QAction.__init__(self,name)

        self._id = id
    
    @property
    def id(self):
        return(self._id)

class basic_tool:
    """
    Prototype a basic tool. We use this for consistent typing and templated functions. 
    
    So, you know, like why anyone else would use class inheritance 
    """
    def __init__(self, parent=None):
        if not (isinstance(parent, QMainWindow) or (parent is None)):
            raise TypeError("Parent should be of type {}, not {}".format(QMainWindow, type(parent)))
        self.parent = parent

    def primary_mouse_depressed(self,event):
        """
        Called when the right mouse button is depressed 

        @param event 
        """
        pass
    def primary_mouse_released(self, event):
        """
        This is called when the right mouse button is released from a localized click. 

        @param event - location of release
        """
        pass
    def primary_mouse_held(self,event ):
        """
        Called continuously while the right mouse button is moved and depressed 

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def secondary_mouse_held(self, event):
        """
        Called continuously while the right mouse button is moved and depressed 
        """
        pass
    def secondary_mouse_released(self, event ):
        """
        Left click released event, used to select something

        @param event - Qt event object. has where the mouse is
        """
        pass
    def mouse_moved(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass
    def drop(self):
        """
        Called when this tool is being replaced. Cleans up anything it has drawn and should get rid of (like, selection circles). This is needed when closing one of the guis 
        """
        pass
    def toggle_mode(self, force=None):
        """
        Toggles the 'mode' of the tool. Optionally passed a 'corce' argument 
        """
        pass

    def get_context_options(self,event):
        """
        Function called by the clicker control requesting a list of context menu options, from the active tool, at the cursor. 
        The tool returns a list containing a string for each viable option
        """
        return([])
    def do_action(self, action):
        if not isinstance(action, MultiHexAction):
            Logger.Fatal("Expected {} in some kind of brush, got {}".format(MultiHexAction, type(action)), TypeError)


    def clear(self):
        """
        Called when parent window is closing. Clears list of drawn items 
        """
        pass 
    def __str__(self):
        return("BasicTool of type {}".format(type(self)))

class Basic_Brush(basic_tool):
    """
    Adds the basic brushy functionality, like showing a hex outline where the mouse is. 

    This is used by the Region and Hex brushes 
    """
    def __init__(self, parent=None):
        basic_tool.__init__(self, parent)
        self._state = 0

        self._selected_id = None # hex id of where the selection is 
        self._outline_obj = None # qt5 object of the drawn outline 
        
        self._color = (0,0,0)
        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()

        self._selected = None

    @property
    def selected(self):
        return( self._selected )

    def select(self, which = None):
        """
        Selects the hex, sets it as the selected one.

        If no Arg is provided, deselect the hex
        """

        if which is not None:
            if not isinstance(which, int):
                raise TypeError("Expected {}, got {}".format(int, type(which)))

        self._selected = which

        # draw a blue outline around the selected hex

    @property
    def state(self):
        """
        state getter
        """
        return(self._state)

    def set_state(self, new):
        """
        state setter 
        """
        if not isinstance(new, int):
            raise TypeError("Expected arg of type {}, got {}".format(int, type(new)))

        if new not in [0,1]:
            raise ValueError("Invalid state {}".format(new))

        self._state = new

    def mouse_moved(self, event):
        """
        While moving it continuously removes and redraws the outline - reimplimentation of the 'move' function in the hex brush
        """
        
        # the default 0-state represents no drawing of the outline, and no brushing 

        if self._state == 0:
            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
                self._outline_obj = None
            return

        place = Point( event.scenePos().x(), event.scenePos().y())
        center_id = self.parent.main_map.get_id_from_point( place )
        self.QPen.setWidth(5)
        self.QPen.setStyle(1)

        if self._selected_id == center_id:
            pass
        else:
            self._selected_id = center_id
            outline = self.parent.main_map.get_neighbor_outline( center_id , self._brush_size)
            #self.QPen.setColor(QtGui.QColor(self._selected_color[0], self._selected_color[1], self._selected_color[2]))
            self.QBrush.setStyle(0)

            if self._outline_obj is not None:
                self.parent.scene.removeItem( self._outline_obj )
            
            self._outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )
            self._outline_obj.setZValue(10)

    def get_color(self):
        new = self.QPen.color()
        return((new.red(),new.green(),new.blue()))
            
    def set_color( self, color):
        """
        Sets the brush and pen to a specified color. The brush is only partially opaque 

        @param color    - the specified color. Needs to be an length-3 indexable with integer entries >0 and < 255
        """
        if not (isinstance( color, list) or isinstance(color, tuple)):
            raise TypeError("Expected list-like for Arg 'color', got {}".format(type(color)))
        
        if len(color)!=3:
            raise ValueError("Expected length 3 for Arg 'color', got {}".format(len(color)))

        for entry in color:
            if type(entry)!=int:
                raise TypeError("For {} in {}, expected type {} but got {}".format(entry, color, int, type(entry)))

            if entry<0 or entry>255:
                raise ValueError("Entry {} in {} should be valued between 0 and 255".format(entry, color))

        self.QBrush.setColor(QtGui.QColor( color[0], color[1], color[2], 60))
        self.QPen.setColor( QtGui.QColor(color[0], color[1], color[2])) 
        self._color = color

    def drop(self):
        self.set_state(0)
        if self._outline_obj is not None:
            self.parent.scene.removeItem( self._outline_obj )
            self._outline_obj = None
        

    def clear(self):
        self.drop()

class clicker_control(QGraphicsScene):
    """
    Manages the mouse interface for to the canvas.
    """
    def __init__(self, parent=None, master=None):
        QGraphicsScene.__init__(self, parent)

        if not isinstance(master, QMainWindow):
            raise TypeError("Clicker control master must be {}, got {}".format(QMainWindow, type(master)))
        if not isinstance(parent, QGraphicsView):
            raise TypeError("Clicker control parent must be {}, got {}".format(QGraphicsView, type(parent)))

        self._active = None #basic_tool object
        self._primary_held = False
        self._secondary_held = False

        self.parent = parent #QGraphicsView
        self.master = master #MainMap

        self._alt_held = False

        self._primary = QtCore.Qt.LeftButton
        self._secondary = QtCore.Qt.RightButton

    def keyPressEvent(self, event):
        event.accept()
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_held = True
    def keyReleaseEvent(self, event):
        event.accept()
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_held = False

        if event.key() == QtCore.Qt.Key_Plus or event.key()==QtCore.Qt.Key_PageUp or event.key()==QtCore.Qt.Key_BracketRight:
            self.parent.scale( 1.05, 1.05 )

        if event.key() == QtCore.Qt.Key_Minus or event.key()==QtCore.Qt.Key_PageDown or event.key()==QtCore.Qt.Key_BracketLeft:
            self.parent.scale( 0.95, 0.95 )


    def mousePressEvent(self, event):
        """
        Called whenever the mouse is pressed within its bounds (The drawspace)
        """
        if event.button()==self._primary:
            event.accept() # accept the event
            self._primary_held = True # say that the mouse is being held 
            self._active.primary_mouse_depressed( event )
        elif event.button()==self._secondary:
            event.accept()
            self._secondary_held = True

    def mouseReleaseEvent( self, event):
        """
        Called when a mouse button is released 
        """
        if event.button()==self._primary:
            # usually a brush event 
            event.accept()
            self._primary_held = False
            self._active.primary_mouse_released(event)

        elif event.button()==self._secondary:
            # usually a selection event
            event.accept()
            self._secondary_held = False
            self._active.secondary_mouse_released( event )

   #mouseMoveEvent 
    def mouseMoveEvent(self,event):
        """
        called continuously as the mouse is moved within the graphics space. The "held" boolean is used to distinguish between regular moves and click-drags 
        """
        event.accept()
        if self._primary_held:
            self._active.primary_mouse_held( event )
        if self._secondary_held:
            self._active.secondary_mouse_held( event )
 
        self._active.mouse_moved( event )

    @property
    def active(self):
        return(self._active)

    def contextMenuEvent(self, event):
        """
        Here we ask the active tool for a list of appropriate actions, then let the user chose one of those, and then we do that action.

        This way we can push the contextMenu implementation down onto the swappable tools
        """

        # list of (name, id) tuples
        opts = self.active.get_context_options(event)
        if not isinstance(opts, list):
            return
        if len(opts)==0:
            return
        contextMenu = QMenu(self.parent)
        actions = {}
        for option in opts:
            if not isinstance(option, tuple):
                raise TypeError("Expected {}, got {}".format(tuple, type(option)))
            if not len(option)==2:
                raise ValueError("Expected length-2 tuple, got length-{}".format(len(option)))

            actions[option] = MultiHexAction(option[0], option[1])
            contextMenu.addAction(actions[option])

        action = contextMenu.exec_(self.master.mapToGlobal(QtCore.QPoint(int(event.scenePos().x()), int(event.scenePos().y()))))
        if action is not None:
            self.active.do_action(action)

    def select(self,which_tool):
        if not isinstance(which_tool, basic_tool):
            raise TypeError("Cannot use tool of type {}!".format(type(which_tool)))
        self._active.drop()
        self._active = which_tool

    def drop(self):
        self._active.drop()
        self._active=basic_tool()

class path_brush(basic_tool):
    """
    Basic tool implementation for drawing Path objects like rivers and roads
    """
    def __init__(self, parent, vertex_mode=False):
        basic_tool.__init__(self, parent)

        # state variable! 
        # state 0 - not doing anything
        #       1 - preparing to draw a road or river. Showing the river/road icon
        #       2 - currently adding to a new road or river. 
        #       3 - adding to existing path's end
        #       4 - adding to existing path's start
        self._state = 0

        self._drawn_icon = None
        self._vertex_mode = vertex_mode
        self._creating = Path
        self._qtpath_type = QtGui.QPainterPath

        self._path_key = "generic"

        # load in the appropriate icon! 
        self._icon_size = 24
        if self._vertex_mode:
            self._icon = QtGui.QPixmap( os.path.join(os.path.dirname(__file__), 'Artwork','buttons', 'river_icon.svg' )).scaledToWidth( self._icon_size )
        else: # road mode
            self._icon = QtGui.QPixmap( os.path.join(os.path.dirname(__file__), 'Artwork','cursors', 'road_cursor.svg' )).scaledToWidth( self._icon_size )

        self._selected_pid = None
        self._selected_color = QtGui.QColor( 255, 100, 100 )

        self._wip_path = None #path object
        self._wip_path_object = None #drawn object on map

        self._step_object = None

        # for drawing
        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
        self.QBrush.setStyle(0)
        self.QPen.setStyle(1)

        self._drawn_paths = { }

        self._extra_states = []

        self._drawing = True

    @property 
    def drawing(self):
        return(self._drawing)
    
    @property
    def selected_pid(self):
        copy = self._selected_pid
        return(copy)

    def select_pid(self, pID = None ):
        if pID is not None:
            if not isinstance(pID, int):
                raise TypeError("Expected type {}, got {}".format( int, type(pID)))

        previous = self._selected_pid


        self._selected_pid = pID
        self.draw_path( pID )

        self.draw_path( previous )

    def pop_selected_start(self):
        if self._selected_pid is not None:
            if self._selected_pid in self.parent.main_map.path_catalog[self._path_key]:
                self.parent.main_map.path_catalog[self._path_key][self._selected_pid].trim_at(1, False )

                if len( self.parent.main_map.path_catalog[self._path_key][self._selected_pid].vertices)==1:
                    self.delete_selected()
        
            self.draw_path( self._selected_pid )

    def pop_selected_end(self):
        if self._selected_pid is not None:
            if self._selected_pid in self.parent.main_map.path_catalog[self._path_key]:
                self.parent.main_map.path_catalog[self._path_key][self._selected_pid].trim_at( -1, True )
                
                if len( self.parent.main_map.path_catalog[self._path_key][self._selected_pid].vertices)==1:
                    self.delete_selected()
            
            self.draw_path( self._selected_pid )
    
    def delete_selected( self ):
        try:
            self.parent.main_map.unregister_path( self._selected_pid , self._path_key )
            self.draw_path(self._selected_pid)
        except ValueError:
            pass

        self.select_pid( None )

    def prepare(self, setting):
        assert( isinstance(setting, int))

        self._state = setting

    def get_alt_from_point(self, event):
        raise NotImplementedError("This method should be reimplemented in a derived class")

    def where_to_from(self, event):
        # the stepsize is dependent on whether we're going center to center
        # or vertex to vertex
        if self._vertex_mode:
            step_size = self.parent.main_map.drawscale
        else:
            step_size = rthree*self.parent.main_map.drawscale

        # figure out from where we're adding
        if self._state ==2:
            from_point = self._wip_path.end()
        elif self._state==3:
            # we should have a river selected, in this state we're going from its end
            try:
                from_point = self.parent.main_map.path_catalog[self._path_key][self._selected_pid].end()
            except KeyError:
                self._state = 0
                self.select_pid( None )
        elif self._state==4:
            # should have a river selected, going from its start 
            try:
                from_point = self.parent.main_map.path_catalog[self._path_key][self._selected_pid].start()
            except KeyError:
                self._state = 0
                self.select_pid( None )
        elif self._state in self._extra_states:
            from_point = self.get_alt_from_point(event)
            if from_point is None:
                self._state = 0
                self.select_pid( None )

        else:
            raise NotImplementedError("Unexpected state {}".format(self._state))
            
        # we need to get the relative distance 
        small_step = Point( event.scenePos().x(), event.scenePos().y()) - from_point
        small_step.normalize()
        small_step = small_step * step_size
        small_step = small_step + from_point

        if self._vertex_mode:
            # it's possible the vertex most in-line with the mouse position is not at a valid neighbor
            # get the valid neighbors
            possible = self.parent.main_map.get_vertices_beside( from_point )
                
            # initialize temporary data structures 
            distance = None
            where = Point()
            # loop over the possibilities and find the closest
            for each in possible:
                if distance == None:
                    where = each
                    distance = ( each - small_step )**2 # looking at distance-squared so no sqrt
                    continue
                temp = (each - small_step)**2
                if temp<distance:
                    where = each
                    distance = temp
       
                
        else:
            where = self.parent.main_map.get_point_from_id(self.parent.main_map.get_id_from_point( small_step ))

        return(where, from_point)

    def mouse_moved( self, event ):
        if self._state==0:
            # not doing anything. Make sure no icon is there
            if self._drawn_icon is not None:
                self.parent.scene.removeItem( self._drawn_icon )
                self._drawn_icon = None

            if self._step_object is not None:
                self.parent.scene.removeItem( self._step_object )
                self._step_object = None

        elif self._state==1:
            # we are placing a new river/road. If it hasn't been drawn, draw the hex
            if self._drawn_icon is None:
                self._drawn_icon = self.parent.scene.addPixmap( self._icon )
                self._drawn_icon.setZValue(20)

            if self._vertex_mode:
                where = self.parent.main_map.get_vert_from_point(Point(event.scenePos().x(),event.scenePos().y() ))
                
            else:
                where = self.parent.main_map.get_point_from_id(self.parent.main_map.get_id_from_point( Point(event.scenePos().x(),event.scenePos().y() )))
                

            self._drawn_icon.setX( where.x )
            self._drawn_icon.setY( where.y ) 
        elif (self._state==2 or self._state==3 or self._state==4):
            if self._drawn_icon is None:
                self._drawn_icon = self.parent.scene.addPixmap( self._icon )
                self._drawn_icon.setZValue(20)

            self._drawn_icon.setX( event.scenePos().x() )
            self._drawn_icon.setY( event.scenePos().y() )

            where, from_point = self.where_to_from(event)

            if self._step_object is not None:
                self.parent.scene.removeItem( self._step_object )
            
            path = self._qtpath_type()
            path.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw([ from_point, where])) )
            self._step_object = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )
                 
        elif self._state in self._extra_states:
            pass
        else:
            raise NotImplementedError("{} Reached unexpected state {}".format(self, self._state))
    # update the position of the river icon

    def primary_mouse_released(self, event):
        if self._state==0:
            # clicked on the map in a do-nothing state. Deselect any selected hex 
            self.select_pid( None )
        elif self._state==1:
            # get the location and make a new path

            if self._vertex_mode:
                where = self.parent.main_map.get_vert_from_point(Point(event.scenePos().x(),event.scenePos().y() ))

            else:
                where = self.parent.main_map.get_point_from_id(self.parent.main_map.get_id_from_point( Point(event.scenePos().x(),event.scenePos().y() )))
            
            if self._path_key not in self.parent.main_map.path_catalog:
                self.parent.main_map.path_catalog[self._path_key] = {}

            # we check if this is the end of an existing path of this type, if it is, we start adding to the end of that one. Nice QOL feature 
            for pID in self.parent.main_map.path_catalog[self._path_key]:
                if where==self.parent.main_map.path_catalog[self._path_key][pID].end():
                    self.select_pid(pID)
                    self._state = 3
                    return

            self._wip_path = self._creating(where)
            self._state = 2

            self.QPen.setWidth( 2 +  self._wip_path.width)
            self.QPen.setColor( self._selected_color )

        # if we're currently drawing on a river
        elif self._state==2 or self._state==3 or self._state==4:
            
            where, from_point = self.where_to_from(event)

            if self._state==2:
                self._wip_path.add_to_end( where )
                if self._wip_path_object is not None:
                    self.parent.scene.removeItem( self._wip_path_object )
                    self._wip_path_object = None
                path = self._qtpath_type()
                self.QPen.setColor(self._selected_color)
                path.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( self._wip_path.vertices )))
                self._wip_path_object = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )
                # draw the WIP Path ontop of the Path layer (2-4) 
                self._wip_path_object.setZValue( 4 )


            elif self._state==3:
                self.parent.main_map.path_catalog[self._path_key][self._selected_pid].add_to_end( where )
                self.draw_path( self._selected_pid)
            else: #state is 4
                self.parent.main_map.path_catalog[self._path_key][self._selected_pid].add_to_start( where )
                self.draw_path( self._selected_pid)

        elif self._state in self._extra_states:
            pass
        else:
            raise NotImplementedError("Reached unexpected state {}".format(self._state))

    def secondary_mouse_released(self, event):

        if self._state==0:
            pass
        elif self._state==1:
            self._state = 0
        elif self._state==2:
            # finish up I guess
            # clear out the erased one

            if self._wip_path_object is not None:
                self.parent.scene.removeItem( self._wip_path_object )
                self._wip_path_object = None


            # no river is added if there aren't at least 2 vertices to make a river
            if len(self._wip_path.vertices)<=1:
                self._wip_path = None
            else:
                pID = self.parent.main_map.register_new_path( self._wip_path, self._path_key )
                self.parent.main_map.path_catalog[ self._path_key][pID].name = "Path {}".format( pID )
                self._wip_path = None
                self.draw_path( pID )
            self._state = 0
        elif self._state==3 or self._state==4:
            self.draw_path( self._selected_pid )
            self.select_pid(None )
            self._state = 0

        elif self._state in self._extra_states:
            pass
        else:
            raise NotImplementedError("Reached unexpected state {}".format(self._state))

        

    def draw_path( self, pID, ignore_color=False):
        """
        Re-draws the path with given PathID. If no such path is found, it instead just erases any associated map item
        """
        
        if pID is None:
            return
        else:
            assert(isinstance(pID, int ))

        if pID in self._drawn_paths:
            self.parent.scene.removeItem( self._drawn_paths[pID])
            del self._drawn_paths[pID]

        if not self.drawing:
            return

        if pID in self.parent.main_map.path_catalog[self._path_key]:
            this_path = self.parent.main_map.path_catalog[self._path_key][pID]
        else:
            return

        self.QBrush.setStyle(0)
        self.QPen.setStyle(1)
        self.QPen.setWidth( 3 + this_path.width )

        # we use this here so the correct type of Scene object is used for derived paths 
        path = self._qtpath_type()
        
        # if we're drawing the selected path, use red
        # otherwise use the path's color 
        if (pID==self._selected_pid) and not ignore_color:
            self.QPen.setColor(self._selected_color)
        else:
            self.QPen.setColor( QtGui.QColor(this_path.color[0], this_path.color[1], this_path.color[2] ))


        path.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( this_path.vertices )))
        self._drawn_paths[pID] = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )
        self._drawn_paths[pID].setZValue( this_path.z_level )

    def drop(self):
        self._state = 0
        self._wip_path = None 

        # remove the WIP river drawing
        if self._wip_path_object is not None:
            self.parent.scene.removeItem( self._wip_path_object )
        self._wip_path_object = None

        # remove the 'next step' segment at the end of the river 
        if self._step_object is not None:
            self.parent.scene.removeItem( self._step_object )
        self._step_object = None

        # remove the icon, if it's drawn 
        if self._drawn_icon is not None:
            self.parent.scene.removeItem( self._drawn_icon )
        self._drawn_icon = None 

        temp = self.selected_pid
        self.select_pid(None)
        self.draw_path(temp)
        
    def clear(self):
        for pID in self._drawn_paths:
            self.parent.scene.removeItem( self._drawn_paths[pID])
        self._drawn_paths = {}

class QEntityItem(QtGui.QStandardItem):
    """
    Item object to be used with the entity lists in the GUI. These things are the same, but also carry around an eID attribute.
    """
    def __init__(self, value, eID):
        super(QEntityItem, self).__init__( value)
        assert( isinstance(eID, int))
        assert( eID >= 0)
        self._eID = eID

    @property
    def eID(self):
        copy = self._eID
        return(copy)

class entity_brush(basic_tool):
    """
    Basic tool implementaion for adding and editing entities on the map! 
    """
    def __init__(self, parent):
        basic_tool.__init__(self, parent)

        # list of drawn Qt Items. objects indexed with relevant eID
        self._drawn_entities = {}

        # are we in the process of placing a thingy
        # -1 no
        #  0 yes, entity
        #  1 yes, Town
        self._placing = -1 
        
        # which menu is open
        self._menu = 0
        # 0 - locations
        # 1 - settlements 

        # eID of the selected entity 
        self._selected_eid = None
        
        # HexID of the selected Hex, and its object 
        self._selected_hex = None
        self._selected_hex_outline = None

        # these are used for the ghosted prospective placement icon of a new entity
        self._ghosted_placement = None
        self._icon_size = None

        # whether or not assets have been loaded
        self._loaded = False
        # where the assets are loaded
        self._all_icons = None
        # icon we are writing with
        self._icon = None 

        self.draw_entities = True
        self.draw_settlements = True

        self.dialog = None

        self._settlement = Settlement
    
    def configure_icon_size(self):
        self._icon_size = int(self.parent.main_map._drawscale*2)

    def select_hex(self, which):
        if not isinstance( which, int):
            raise TypeError("")
        self._selected_hex = which

    @property
    def selected_hex(self):
        copy = self._selected_hex
        return(copy)

    @property
    def selected(self):
        copy = self._selected_eid
        return(copy)
    def select_entity(self, eID):
        """
        Function exposing the selected eID. Allows it to be set by non-member functions
        """
        assert( isinstance( eID, int ))
        if not eID in self.parent.main_map.eid_catalog:
            raise ValueError("eID {} not registered, but is being selected?".format(eID))
        self._selected_eid = eID

    def prep_new(self, ent_type = 0):
        """
        Prepares this object to place a new Entity. Optional argument to specify /which/ kind of entity to place. Creates a ghost outline to show where the new Entity will be 
        """
        assert( isinstance(ent_type, int))
        self._placing = ent_type 

        if not self._loaded:
            self.load_assets()

        if self._ghosted_placement is not None:
            self.parent.scene.removeItem(self._ghosted_placement)
            self._ghosted_placement = None 

        if ent_type == 0 or ent_type == 1:
            if ent_type==0:
                self._icon = self._all_icons.pixdict['location']
            else:
                self._icon = self._all_icons.pixdict['village']
            self._ghosted_placement = self.parent.scene.addPixmap( self._icon )
            self._ghosted_placement.setZValue(20)
            
        else:
            pass

    def unprepare_new(self):
        """
        Yeah cancel that
        """
        self._placing = -1
        if self._ghosted_placement is not None:
            self.parent.scene.removeItem(self._ghosted_placement)
            self._ghosted_placement = None 

    def mouse_moved(self, event):
        """
        All this really does is move the ghost around. If it turns out that we aren't placing things then get rid of the ghosts 
        """
        if not self._loaded:
            self.load_assets()

        # this is the case when the user is placing a Location  ( 0 )
        if self._placing in [0, 1]:
            if self._ghosted_placement is None:
                raise Exception("This shouldn't happen")
            else:
                self._ghosted_placement.setX( event.scenePos().x() -(self._icon_size)/2 )
                self._ghosted_placement.setY( event.scenePos().y() -(self._icon_size)/2 )
        else:
            if self._ghosted_placement is not None:
                self.parent.scene.removeItem( self._ghosted_placement )
                self._ghosted_placement = None 

    def deselect_hex(self):
        """
        Called when this is no longer looking at any Hex
        """
        self._selected_hex = None
        self.update_wrt_new_hex()

    def update_wrt_new_hex(self):
        """
        Called when a new hex is selected, OR this hex has changed (like new entities). Updates the GUI based on the hex selected: draws an outline around the selected Hex and updates the list of entities 
        """
        
        self._menu = self.parent.ui.contextPane.currentIndex()

        if self._selected_hex_outline is not None:
            self.parent.scene.removeItem( self._selected_hex_outline )
            self._selected_hex_outline = None

        self._selected_eid = None

        if self._menu == 0:
            # tell the gui to update the proper menu
            self.parent.extra_ui.loc_update_selection( self._selected_hex )
        elif self._menu==1:
            # get eIDs at this hex
            settlement_eid = None

            if self._selected_hex in self.parent.main_map.eid_map:
                eIDs_here = self.parent.main_map.eid_map[ self._selected_hex ]
                for eID in eIDs_here:
                    if isinstance( self.parent.main_map.eid_catalog[eID] , self._settlement ):
                        settlement_eid = eID
            self._selected_eid = settlement_eid
            self.parent.extra_ui.set_update_selection( settlement_eid )
        else:
            pass


    def update_wrt_new_eid(self):
        """
        Called when a new /entity/ is selected. Chooses and updates the proper menu
        """
        self._menu = self.parent.ui.contextPane.currentIndex()

        if self._menu == 0:
            self.parent.extra_ui.loc_update_name_text( self._selected_eid )
        elif self._menu==1:
            self.parent.extra_ui.set_update_selection( self._selected_eid )

    def primary_mouse_released( self, event ):
        """
        Select the hex that was clicked on. If we're placing, create the Entity and place it. Then update the menus
        """
        place = Point( event.scenePos().x(), event.scenePos().y() ) 
        loc_id = self.parent.main_map.get_id_from_point( place )
        
        if loc_id!=self._selected_hex:
            self._selected_hex = loc_id 
            self.update_wrt_new_hex()



        if self._placing in [ 0, 1 ]:
            # we are going to create 
            if self._ghosted_placement is not None:
                self.parent.scene.removeItem( self._ghosted_placement )
                self._ghosted_placement = None   
            
            if self._placing == 0:
                new_ent = Entity( "temp" , loc_id )
                new_ent.icon = "location"
                self._selected_eid = self.parent.main_map.register_new_entity( new_ent )
                self.parent.main_map.eid_catalog[self._selected_eid].name = "Entity {}".format(self._selected_eid)
            else: #placing is 1
                new_ent = self._settlement("temp", loc_id )
                new_ent.icon = "village"
                self._selected_eid = self.parent.main_map.register_new_entity( new_ent )
                self.parent.main_map.eid_catalog[self._selected_eid].name = "Town {}".format(self._selected_eid)
            
            self.update_wrt_new_eid()
            self.redraw_entities_at_hex( loc_id )

            if self._placing == 0:
                self.update_wrt_new_hex()

            self._placing = -1 

        else:
            pass


    def get_context_options(self, event):
        if self._placing==-1:
            place = Point( event.scenePos().x(), event.scenePos().y())
            loc_id = self.parent.main_map.get_id_from_point( place )
            if loc_id in self.parent.main_map.eid_map:
                return([ (self.parent.main_map.eid_catalog[entry].name, entry) for entry in self.parent.main_map.eid_map[loc_id]])
    
    def do_action(self, action):
        self.select_entity( action.id )

        # now we need to open up that dialog 
        print("eid {}".format(action.id))
        self.dialog = EntityDialog(self.parent, self.parent.main_map.eid_catalog[action.id])
        self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def load_assets(self):
        """
        Loads all the artwork into an Icon object held 
        """
        self._all_icons = self.parent.icons
        self._loaded = True
    
    def redraw_entities_at_hex(self, hID):
        """
        Redraws the entities at the hexID provided. This function decides which entity to draw. 
        """

        if hID == -1:
            return
        if hID not in self.parent.main_map.eid_map:
            raise ValueError("HexID {} has no entry in eID map: {}".format(hID, self.parent.main_map.eid_map[hID]))

        eIDs = self.parent.main_map.eid_map[hID]
        
        # make sure none of these have been drawn
        for eID in eIDs:
            if eID in self._drawn_entities:
                self.parent.scene.removeItem( self._drawn_entities[eID])
                del self._drawn_entities[eID]

        if not self.draw_entities:
            return
        
        which_eID = None
        for eID in eIDs:
            is_set = isinstance( self.parent.main_map.eid_catalog[eID], self._settlement)
            
            if is_set and (not self.draw_settlements):
                continue

            if which_eID is None:
                which_eID = eID 
                continue
            
            other_is_set = isinstance( self.parent.main_map.eid_catalog[which_eID], self._settlement )

            is_mob = isinstance( self.parent.main_map.eid_catalog[eID], Mobile )
            if is_mob:
                print("Don't know how to draw a mob")
                continue

            

            # if the chosen one is a settlement and this one isn't, skip
            if other_is_set and (not is_set):
                continue
            # otherwise, if this one is a settlement and the other isn't, swap to this one. 
            elif is_set and ( not other_is_set ):
                which_eID = eID
            # if they /both/ are settlements
            elif other_is_set and is_set:
                # choose the one with the higher population
                if self.main_map.eid_catalog[eID].population > self.main_map.eid_catalog[which_eID].population:
                    which_eID = eID

        if which_eID is None:
            return

        self.draw_entity( which_eID )    

    def draw_entity(self, eID):
        """
        Draws the entity with eID provided. 
        """

        if not self._loaded:
            self.load_assets()

        if (eID not in self.parent.main_map.eid_catalog) and (eID not in self._drawn_entities):
            raise ValueError("eID {} not registered in catalog".format(eID))

        # delete old drawing if it exists
        if eID in self._drawn_entities:
            self.parent.scene.removeItem( self._drawn_entities[ eID ] )
            del self._drawn_entities[ eID ]

        if eID in self.parent.main_map.eid_catalog:
            self._drawn_entities[eID] = self.parent.scene.addPixmap( self._all_icons.pixdict[self.parent.main_map.eid_catalog[ eID ].icon] )
            self._drawn_entities[eID].setZValue(5)
            location = self.parent.main_map.get_point_from_id( self.parent.main_map.eid_catalog[eID].location)
            self._drawn_entities[eID].setX( location.x - self._all_icons.shift)
            self._drawn_entities[eID].setY( location.y - self._all_icons.shift)


    def drop(self):
        self.deselect_hex()
       
        if self._selected_hex_outline is not None:
            self.parent.scene.removeItem( self._selected_hex_outline )

        if self._ghosted_placement is not None:
            self.parent.scene.removeItem( self._ghosted_placement )

    def clear(self):
        self.drop() 
        self._drawn_entities = {}

class Map_Use_Tool(basic_tool):
    """
    The tool used in the map use mode. It's used to place and edit mobiles in addition to accessing information on all map entities. 
    """
    def __init__(self, parent):
        basic_tool.__init__(self,parent)

        self._state = 0
        self._valid_states = [0,1]
        # 0 - Idle. Open to selecting a new Mobile or Entity  
        # 1 - Entity selected

        self._from_id = None
        self._route = None

        self._drawn_route_obj = None

        self.QBrush = QtGui.QBrush()
        self.QBrush.setStyle(0)
        self.QPen   = QtGui.QPen()
        self.QPen.setStyle(2)
        self.QPen.setWidth(5)
        self.QPen.setColor(QtGui.QColor(20, 200, 200))

    @property
    def state(self):
        return(self._state)

    def set_state(self, state):
        if state not in self._valid_states:
            raise ValueError("{} not in list of valid states: {}".format(state, self._valid_states))
        self._state = state

    def select(self, eid=None):
        if eid is None:
            self.set_state(0)
            self._selected = None
        else:
            if eid in self.parent.main_map.eid_catalog:
                self._selected = eid
                self.set_state(1)
            else:
                self._selected = None
                self.set_state(0)

    def primary_mouse_released(self, event):
        place = Point( event.scenePos().x(), event.scenePos().y())
        loc_id = self.parent.main_map.get_id_from_point( place )

        if self.state==0:
            if loc_id in self.parent.main_map.eid_map:
                eids_here = self.parent.main_map.eid_map[loc_id]
            else:
                return

            if len(eids_here)==1:
                self.select(eids_here[0])
            else:
                self.special_context_event(event)

        if False: # I don't want this activated atm, but I want to reuse this code later
            if self.state==0:
                self._from_id = loc_id
                self.set_state(1)
            elif self.state==1:
                # get the route! 
                self._route = self.parent.main_map.get_route_a_star(self._from_id, loc_id)
                self.set_state(0)
                self.draw_route( self._route )

    def mouse_moved(self, event):
        place = Point( event.scenePos().x(), event.scenePos().y())
        loc_id = self.parent.main_map.get_id_from_point( place )

        if False:
            if loc_id==self._from_id:
                return
            if self.state==1:
                # get the route! 
                self._route = self.parent.main_map.get_route_a_star(self._from_id, loc_id)
                self.draw_route( self._route )

    def secondary_mouse_released(self, event):
        pass

    def special_context_event(self, event):
        opts = self.get_context_options(event)
        if not isinstance(opts, list):
            return
        if len(opts)==0:
            return
        contextMenu = QMenu(self.parent)
        actions = {}
        for option in opts:
            if not isinstance(option, tuple):
                raise TypeError("Expected {}, got {}".format(tuple, type(option)))
            if not len(option)==2:
                raise ValueError("Expected length-2 tuple, got length-{}".format(len(option)))

            actions[option] = MultiHexAction(option[0], option[1])
            contextMenu.addAction(actions[option])

        action = contextMenu.exec_(self.parent.mapToGlobal(QtCore.QPoint(int(event.scenePos().x()), int(event.scenePos().y()))))
        if action is not None:
            self.do_action(action)

    def do_action(self, action):
        if not isinstance(action, MultiHexAction):
            raise TypeError("Somehow got a {}, not a {}".format(type(action), MMultiHexAction))

        if action.id is not None:
            self.select(action.id)

    def get_context_options(self, event):
        if self.state==0:
            place = Point( event.scenePos().x(), event.scenePos().y())
            loc_id = self.parent.main_map.get_id_from_point( place )
            if loc_id in self.parent.main_map.eid_map:
                return([ (self.parent.main_map.eid_catalog[entry].name, entry) for entry in self.parent.main_map.eid_map[loc_id]])
        elif self.state==1:
            # move here
            return("Move Here")

    def draw_route(self, route):
        if self._drawn_route_obj is not None:
            self.parent.scene.removeItem( self._drawn_route_obj )

        positions = [self.parent.main_map.get_point_from_id(id) for id in route]

        # we use this here so the correct type of Scene object is used for derived paths 
        path = QtGui.QPainterPath()

        path.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( positions )))
        self._drawn_route_obj = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )
        self._drawn_route_obj.setZValue( 30 )

    def drop(self):
        pass



class hex_brush(Basic_Brush):
    """
    Another tool with clicker-control interfacing used to paint hexes on a hexmap. 

    Keeps track of all the canvas objects that it has drawn. Theres are **not** actual Hexes (TM), but just boring ass hexagons. 
    """
    def __init__(self, parent):
        Basic_Brush.__init__(self,parent)
        # what type of Hex does this brush draw
        self._brush_type = Hex
        # parameters (like rainfall, temperature, etc) and their defaults 
        self._brush_params = {}
        # which of these to skip when overwriting an existing hex 
        self._skip_params = []

        self._brush_size = 1

        self.pen_style = 0
        self.pen_size = 2

        self.drawn_hexes = {}

        # are we overwriting hexes while we draw? 
        self.overwrite = True

        self._activated = False
        # start it out as transparent until we actually choose a color/param
        self.QPen.setColor(QtGui.QColor(0,0,0,0))

        self.use_param_as_color=''

        # outline object for which hex is selected
        self._selection_outline_obj = None 

    def set_params( self, obj ):
        assert( isinstance(obj, dict) )

        if not self._activated:
            self._activated = True
        self._brush_params = obj


    def _make_hex(self, where, radius):
        """
        Creates a new hex with the given center and radius (drawsize).

        Assigns it all the defaults, as specified by the brush_params attribute 
        """
        if not isinstance(where, Point):
            raise TypeError("Arg 'where' must be {}, got {}".format(Point, type(where)))
        if not (isinstance(radius, int) or isinstance(radius, float)):
            raise TypeError("Expected number-like for 'radius', got {}".format(type(radius)))

        new = self._brush_type(where, radius)
        self.adjust_hex( new )
        return(new)

    def adjust_hex( self, which, params=None ):
        """
        Adjust the given hex to the configured parameters (or a set of given parameters)
        """
        if not isinstance(which, Hex):
            raise TypeError("Expected {}, got {}.".format(Hex, type(which)))

        if params is None:
            use = self._brush_params
            skip = self._skip_params
            which.fill = self.get_color()
        else:
            if not isinstance(params, dict):
                raise TypeError("'params', if used, should be {}, not {}".format(dict, type(params)))
            use = params
            skip = []

        for param in use:
            if param in skip:
                continue
            else:
                setattr( which, param, use[param])

    def primary_mouse_released(self, event):
        if self._state==0:
            self.select_evt(event)
        elif self._state == 1:
            self.write(event)

    def primary_mouse_held(self, event):
        if self._state==0:
            pass
        elif self._state == 1:
            self.primary_mouse_released(event)

    def secondary_mouse_held(self, event):
        if self._state==0:
            pass
        elif self._state==1:
            self.secondary_mouse_released(event)
    
    def secondary_mouse_released(self,event):
        if self._state==0:
            self.deselect_evt(event)
        elif self._state == 1:
            self.erase(event)

    def select(self, loc_id=None ):
        Basic_Brush.select(self, loc_id)

        # remove any selection outline
        if self._selection_outline_obj is not None:
            self.parent.scene.removeItem(self._selection_outline_obj)

        if (loc_id is not None) and (loc_id in self.parent.main_map.catalog):
            temp = self.get_color()
            self.QPen.setColor(QtGui.QColor(0, 220,220))
            self.QPen.setStyle(1)
            self.QBrush.setStyle(0)
            outline = self.parent.main_map.get_neighbor_outline( loc_id , self._brush_size)

            self._selection_outline_obj = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( outline )), pen = self.QPen, brush=self.QBrush )
            self._selection_outline_obj.setZValue(10)

    def select_evt(self, event):
        place = Point(event.scenePos().x(),event.scenePos().y() )
        loc_id = self.parent.main_map.get_id_from_point( place )
        try:
            self.parent.extra_ui.det_show_selected(loc_id)
        except AttributeError:
            pass
        self.select( loc_id ) #select


    def deselect_evt(self, event):
        self.parent.extra_ui.det_show_selected()
        self.select() # deselect
    
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
        
        if not self._activated:
            # Brush hasn't been configured with any parameters yet! 
            return

        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )

        # calculate the center of a hex that would have that id
        new_hex_center = self.parent.main_map.get_point_from_id( loc_id )
        
        # register that hex in the hexmap 
        try:
            if (loc_id in self.parent.main_map.catalog) and self.overwrite:
                # if we're overwriting, delete any hex that exists here
                self.adjust_hex( self.parent.main_map.catalog[loc_id])
                self.parent.main_map.catalog[loc_id].rescale_color()
            else:
                # create a hex at that point, with a radius given by the current drawscale 
                new_hex= self._make_hex( new_hex_center, self.parent.main_map._drawscale )
                self.parent.main_map.register_hex( new_hex, loc_id )
            self.redraw_hex( loc_id )
        except NameError:
            # if we aren't overwriting, the register_hex function will raise a NameError. That's okay 
            pass

        if self._brush_size ==2:
            neighbors = self.parent.main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = self.parent.main_map.get_point_from_id( neighbor )
                try:
                    if (neighbor in self.parent.main_map.catalog) and self.overwrite:
                        self.adjust_hex( self.parent.main_map.catalog[neighbor])
                        self.parent.main_map.catalog[neighbor].rescale_color()
                    else:
                        new_hex = self._brush_type( new_hex_center, self.parent.main_map._drawscale)
                        self.parent.main_map.register_hex( new_hex, neighbor )            
                    self.redraw_hex( neighbor )
                except NameError:
                    pass

    def get_color_for_param_overwrite(self, parameter_name, parameter_value):
        """
        This is to be used for the heatmaps

        It returns a QColor for a given parameter and its name. This should be implemented in derived classes! 
        """
        raise NotImplementedError("Use a derived class!")
        return( QtGui.QColor(0,0,0) )

    def erase_hex(self, hex_id):
        # if this hex has been drawn, redraw it! 
        if hex_id in self.drawn_hexes:
            self.parent.scene.removeItem( self.drawn_hexes[hex_id] )
            del self.drawn_hexes[hex_id]

    def draw_hex(self, hex_id):
        try:
            this_hex = self.parent.main_map.catalog[ hex_id ]
        except KeyError:
            return

        if self.use_param_as_color=='':
            self.QPen.setColor(QtGui.QColor( this_hex.outline[0], this_hex.outline[1], this_hex.outline[2] ))
            self.QBrush.setColor( QtGui.QColor( this_hex.fill[0], this_hex.fill[1], this_hex.fill[2] ))
        else:
            self.QPen.setColor(self.get_color_for_param_overwrite(self.use_param_as_color, getattr(this_hex, self.use_param_as_color)))
            self.QBrush.setColor(self.get_color_for_param_overwrite(self.use_param_as_color, getattr(this_hex, self.use_param_as_color)))

        self.QBrush.setStyle(1)
        self.QPen.setWidth(self.pen_size)
        self.QPen.setStyle(self.pen_style)

        
        self.drawn_hexes[hex_id] = self.parent.scene.addPolygon( QtGui.QPolygonF( self.parent.main_map.points_to_draw( this_hex.vertices )), pen=self.QPen, brush=self.QBrush) 
        self.drawn_hexes[hex_id].setZValue(-1)

    def redraw_hex(self, hex_id):
        self.erase_hex(hex_id)
        self.draw_hex(hex_id)


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

    def clear(self):
        self.drop()
        self.drawn_hexes = {}
        


class region_brush(Basic_Brush):
    """
    basic_tool implementation used to draw and register regions on a canvas/hexmap 
    """

    def __init__(self, parent, layer):
        Basic_Brush.__init__(self, parent)
        """
        @ param parent - the gui object that will hold this 
        """
        self.start = Point(0.0, 0.0)

        # parent should be a pointer to the gui object that has this brush 
        self.parent = parent
        self._writing = True
        self._brush_size = 1

        self.QBrush = QtGui.QBrush()
        self.QPen   = QtGui.QPen()
        self.QBrush.setStyle(6)
        self.QPen.setWidth(3)

        self.r_layer = layer

        self._drawn_regions = {} # map from rid to drawn region
        self._drawn_names = {}

        self.draw_borders = False
        self.draw_names = True 

        self._type = Region

        self._state = 0

        self.small_font = False
        self.default_name = "Region"

    def select(self, event):
        """
        Extends the parent class `select' function to apply the Brush color appropriately. 
        """
        Basic_Brush.select(self, event)

        if self.selected is not None:
            self.set_color(self.parent.main_map.rid_catalog[self.r_layer][self.selected].color)
        else:
            self.set_color((255,255,255))

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

    def secondary_mouse_held(self, event):
        """
        Do the same thing as if the mouse was released
        """
        self.secondary_mouse_released(event)

    def secondary_mouse_released(self, event):
        """
        If in mode 1, and a region is selected, remove the region under the cursor

        if no region is selected, return to state 0
        """

        if self.state==0:
            return
        else:
            if self.selected is None:
                self.set_state(0)
            else:
                self.reg_remove( event )

    def primary_mouse_held(self, event):
        self.primary_mouse_released( event )

    def primary_mouse_released(self, event):
        """
        Draws or Erases, depending on the mode 
        """
        if self.r_layer not in self.parent.main_map.rid_catalog:
            self.parent.main_map.rid_catalog[self.r_layer] = {}
        if self.r_layer not in self.parent.main_map.id_map:
            self.parent.main_map.id_map[self.r_layer] = {}

        if self.state==0:
            here = Point( event.scenePos().x(), event.scenePos().y())
            this_id = self.parent.main_map.get_id_from_point( here )

            if this_id not in self.parent.main_map.id_map[self.r_layer]:
                self.select(None)
            else:
                self.select(self.parent.main_map.id_map[self.r_layer][this_id])
                    

        else:
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

    def reg_add(self, event):
        """
        Add to a region. If the brush size is 1, it just tries to add that hex to the active region. If there's no active region, it creates a region there. If the brush size is 2 it makes a temporary region around the cursor and merges the surrounding hexes with the temp region. Then it merges the temp region and active region together. 
        """
        # set up the pen and brush to draw a region
        
        place = Point( event.scenePos().x() , event.scenePos().y() )
        # get the nearest relevant ID
        loc_id = self.parent.main_map.get_id_from_point( place )
        
        if loc_id not in self.parent.main_map.catalog:
            return


        if self.selected is None:
            # if the hex here is not mapped to a registered region, 
            if (loc_id not in self.parent.main_map.id_map[self.r_layer]):
                # make a new region here, set it to the active region, and draw it
                new_reg = self._type( loc_id, self.parent.main_map )
                                
                # get the newely created rid, set it to active 
                self.select( self.parent.main_map.register_new_region( new_reg, self.r_layer ) )
                new_reg.name = self.default_name +" "+ str( self.selected )

                # self.parent.main_map.id_map( loc_id )
                
                if self._brush_size == 2:
                    # build a new region around this one
                    for ID in self.parent.main_map.get_hex_neighbors( loc_id ):
                        self.parent.main_map.add_to_region( self.selected, ID, self.r_layer )

                self.redraw_region( self.selected )
            else:
                # no active region, but the hex here belongs to a region. 
                # set this hexes' region to the active one 
                self.select( self.parent.main_map.id_map[self.r_layer][ loc_id ] )
        else:
            if self._brush_size==1:
                try:
                    # try adding it
                    # if it can't, it raises a RegionMergeError exception
                    other_rid = self.parent.main_map.add_to_region(self.selected , loc_id, self.r_layer )
                    
                    if (other_rid!=-1) and (other_rid is not None): 
                        # add_to_region returns an rid if it removes a hex from another region.
                        # it returns -1, it didn't remove anything from anywhere 
                        self.redraw_region( other_rid )
                    self.redraw_region( self.selected )
                except RegionMergeError:
                    pass
                except RegionPopError:
                    pass
            elif self._brush_size==2:
                # This seems to cause some instability...
                # ...
                if loc_id not in self.parent.main_map.id_map[self.r_layer]:
                    # create and register a region
                    temp_region = self._type( loc_id , self.parent.main_map )
                    new_rid = self.parent.main_map.register_new_region( temp_region, self.r_layer )

                    for ID in self.parent.main_map.get_hex_neighbors( loc_id ):
                        try:
                            self.parent.main_map.add_to_region( new_rid, ID , self.r_layer )
                        except (RegionMergeError, RegionPopError):
                            pass

                    # now merge the regions
                    try: 
                        self.parent.main_map.merge_regions( self.selected , new_rid , self.r_layer)
                        self.redraw_region( self.selected )
                    except RegionMergeError:
                        # delete that region, remove it
                        self.parent.main_map.remove_region( new_rid , self.r_layer )

    def reg_remove(self, event):
        """
        Tries to remove the hex under the cursor from its region.
        """
        place   = Point( event.scenePos().x(), event.scenePos().y() )
        loc_id  = self.parent.main_map.get_id_from_point( place )
        if loc_id not in self.parent.main_map.catalog:
            return

        if loc_id not in self.parent.main_map.id_map[self.r_layer]:
            # nothing to pop
            return
        else:
            # get this hexes's region id 
            this_rid = self.parent.main_map.id_map[self.r_layer][ loc_id ]
            # remvoe this hex from that region
            try:
                self.parent.main_map.remove_from_region( loc_id, self.r_layer )
                # redraw that region
                self.redraw_region( this_rid )
            except RegionPopError:
                pass

    def redraw_region(self, reg_id ):
        """
        Redraws the region with the provided region ID.

        @ param reg_id  - region id if region to redraw.
        """

        self.redraw_region_text( reg_id )


        #self.QBrush.setStyle(6)
        self.QBrush.setStyle(1)
        self.QPen.setWidth(3)
        

        if reg_id in self._drawn_regions:
            self.parent.scene.removeItem( self._drawn_regions[ reg_id ] )
            del self._drawn_regions[reg_id]

        if not self.draw_borders:
            return()
        
        try:
            reg_obj = self.parent.main_map.rid_catalog[self.r_layer][ reg_id ]
        except KeyError:
            return

        self.set_color( reg_obj.color )

        path = QtGui.QPainterPath()
        outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw( reg_obj.perimeter + [reg_obj.perimeter[0]] ) )
        path.addPolygon( outline )

        for enclave in reg_obj.enclaves:
            enc_path = QtGui.QPainterPath()
            enc_outline = QtGui.QPolygonF( self.parent.main_map.points_to_draw(enclave+[enclave[0]])) 
            enc_path.addPolygon( enc_outline )
            path = path.subtracted( enc_path )
        
        self._drawn_regions[reg_id] = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush)
        self._drawn_regions[reg_id].setZValue(9)


    def redraw_region_text( self, rid ):
        """
        Redraws the name of the region with the provided region id

        @param rid  - region id of region whose name should be redrawn
        """
        

        if rid in self._drawn_names:
            self.parent.scene.removeItem( self._drawn_names[ rid ] )
            del self._drawn_names[ rid ]

        if not self.draw_names:
            return

        if rid not in self.parent.main_map.rid_catalog[self.r_layer]:
            return

        reg_obj = self.parent.main_map.rid_catalog[self.r_layer][ rid ]

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


        
        drop = QGraphicsDropShadowEffect()
        drop.setOffset(1)
        center, extent = reg_obj.get_center_size()
        font = QtGui.QFont("Fantasy")
        new_color= QtGui.QColor( 250, 250, 250)
        if self.small_font:
            font_size = 10
        else:
            font_size = mult_factor*max( 12, int(extent.magnitude / len(reg_obj.name)))

        font.setPointSize( font_size )
        self._drawn_names[rid] = self.parent.scene.addText( dname, font )
        self._drawn_names[rid].setPos( center.x - 0.5*extent.x, center.y )
        self._drawn_names[rid].setDefaultTextColor( new_color )
        if not self.small_font:
            self._drawn_names[rid].setGraphicsEffect( drop )
            self._drawn_names[rid].setZValue(15)
        else:
            self._drawn_names[rid].setZValue(14)
    
    def drop(self):
        Basic_Brush.drop(self)
        pass

    def clear(self):
        Basic_Brush.clear(self)
        self._drawn_names = {}
        self._drawn_regions = {}


## #!/usr/bin/python3.6m

from point import Point
from hex import Hex
from hexmap import Hexmap
from hexmap import save_map, load_map
from special_hexes import *

import tkinter as tk
import tkinter.font as tkfont

import sys # basic command line interface 
import os  # basic file-checking

master = tk.Tk()
font = tkfont.Font(family="Consolas", size=10, weight="normal")
screen_ratio = 0.8

import os # use the os module to discern the OS
#it's stupid that I have to do this
if os.name == 'nt':
    photo1 = tk.PhotoImage(file= "hexes\hex_deepgreen.gif").subsample(8,8)
    photo2 = tk.PhotoImage(file= "hexes\hex_lightgreen.gif").subsample(8,8)
    photo3 = tk.PhotoImage(file= "hexes\hex_orange.gif").subsample(8,8)
    photo4 = tk.PhotoImage(file= "hexes\hex_blue.gif").subsample(8,8)
    photo5 = tk.PhotoImage(file= "hexes\hex_gray.gif").subsample(8,8)
    photo6 = tk.PhotoImage(file= "hexes\hex_beige.gif").subsample(8,8)
    draw_one = tk.PhotoImage(file= "hexes\draw_one.gif").subsample(8,8)
    draw_several = tk.PhotoImage(file= "hexes\draw_several.gif").subsample(8,8)
    hex_add = tk.PhotoImage(file= "hexes\hex_add.gif").subsample(8,8)
    hex_remove = tk.PhotoImage(file= "hexes\hex_remove.gif").subsample(8,8)

else:
    photo1 = tk.PhotoImage(file= "hexes/hex_deepgreen.gif").subsample(8,8)
    photo2 = tk.PhotoImage(file= "hexes/hex_lightgreen.gif").subsample(8,8)
    photo3 = tk.PhotoImage(file= "hexes/hex_orange.gif").subsample(8,8)
    photo4 = tk.PhotoImage(file= "hexes/hex_blue.gif").subsample(8,8)
    photo5 = tk.PhotoImage(file= "hexes/hex_gray.gif").subsample(8,8)
    photo6 = tk.PhotoImage(file= "hexes/hex_beige.gif").subsample(8,8)
    draw_one = tk.PhotoImage(file= "hexes/draw_one.gif").subsample(8,8)
    draw_several = tk.PhotoImage(file= "hexes/draw_several.gif").subsample(8,8)
    hex_add = tk.PhotoImage(file= "hexes/hex_add.gif").subsample(8,8)
    hex_remove = tk.PhotoImage(file= "hexes/hex_remove.gif").subsample(8,8)

# loaded maps need to be drawn
need_to_draw = False
if len(sys.argv) > 1:
    in_file = sys.argv[1]
    if in_file.split(".")[-1]=="hexmap":
        if os.path.exists( in_file ):
            print("Loading "+in_file)
            main_map = load_map( in_file )
            need_to_draw = True
        else:
            main_map = Hexmap() 
    else:
        main_map = Hexmap() 
else:
    main_map = Hexmap() 


def savesave():
    save_map(main_map, "saves/test.hexmap")

class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self):
        pass
    def press(self,event):
        """
        Called when the mouse is pressed

        @param event 
        """
        pass
    def activate(self, event):
        """
        This is called when the mouse is released from a localized click. 

        @param event - location of release
        """
        pass
    def hold(self,event, step):
        """
        Called continuously while the mouse is held

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def move(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass

class hand(basic_tool):
    """
    Scroller 
    """
    def __init__(self):
        pass
    def activate(self,event):
        try:
            loc_id = main_map.get_id_from_point( Point( event.x, event.y) )
            main_map.set_active_hex( loc_id )
        except KeyError:
            pass

    def hold(self, event, step):
        move_by = Point(event.x - step.x, event.y - step.y)  
        main_map.draw_relative_to += Point( event.x - step.x, event.y -step.y )
        # move canvas by draw_relative to
#        for obj in main_map.drawn_hexes:
         
        #main_map.draw( event.widget )
        event.widget.move( 'all', event.x-step.x, event.y-step.y)
        #event.widget.update()

class selector(basic_tool):
    def __init__(self):
        self.start = Point(0.0,0.0)
    def press(self, place):
        self.start = place 
    def activate(self, place):
        pass


class hex_brush(basic_tool):
    """
    Writes hexes.
    """
    def __init__(self):
        self.writing = True
        self._brush_type = Grassland_Hex
        self._brush_size = 2

    def activate(self, event):
        if self.writing:
            self.write(event)
        else:
            self.erase(event)
    def hold(self, event, step):
        
        self.move(event)
        self.activate(event)
    
    def move(self, event):
        place = Point( event.x, event.y)
        # show an outline of where we are going to write
        center_id = main_map.get_id_from_point( place )
        outline = main_map.get_neighbor_outline( center_id , self._brush_size)
        main_map._outline = outline
        main_map.draw_outline( event.widget )

        # redraw the selection outline

    def erase(self, event):
        place = Point(event.x,event.y)
        loc_id = main_map.get_id_from_point( place )
        main_map.remove_hex(event.widget, loc_id)
        if self._brush_size ==2:
            neighbors = main_map.get_hex_neighbors(loc_id)
            for neighbor in neighbors:
                main_map.remove_hex( event.widget, neighbor )

    def write(self, event):
        place = Point( event.x , event.y )
        # get the nearest relevant ID
        loc_id = main_map.get_id_from_point( place )

        # calculate the center of a hex that would have that id
        new_hex_center = main_map.get_point_from_id( loc_id )
        # create a hex at that point, with a radius given by the current drawscale 
        new_hex= self._brush_type( new_hex_center, main_map._drawscale )
        #print(self._brush_type)
        # register that hex in the hexmap 
        try:
            main_map.register_hex( new_hex, loc_id )
            main_map.draw_one_hex( event.widget, loc_id )
        except NameError:
            # don't actually want this
            # main_map.set_active_hex( loc_id )
            # if there is already a hex there, just set that hex as the active one
            pass
        if self._brush_size ==2:
            neighbors = main_map.get_hex_neighbors( loc_id )
            for neighbor in neighbors:
                new_hex_center = main_map.get_point_from_id( neighbor )
                new_hex = self._brush_type( new_hex_center, main_map._drawscale)
                try:
                    main_map.register_hex( new_hex, neighbor )
                    main_map.draw_one_hex( event.widget, neighbor )
                except NameError:
                    pass

    def set_brush_small(self):
        self._brush_size = 1
    def set_brush_large(self):
        self._brush_size = 2
    def set_write(self):
        self.writing = True
    def set_erase(self):
        self.writing = False
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


writer_control = hex_brush()
hand_control = hand()


class clicker_control:
    """
    Manages the mouse interface for to the canvas 
    """
    def __init__(self):
        self.start = Point(0.0, 0.0)
        self.step = Point(0.0, 0.0)
        self.end   = Point(0.0, 0.0)

        self._active = writer_control
        
    def press(self, event):
        self.step =  Point( event.x, event.y)
        self.start = Point( event.x, event.y)
        self._active.press( event )

    def release( self, event):
        self.end = Point(event.x, event.y)
        diff = self.start - self.end
        if diff.magnitude <=5.0:
            self._active.activate(event)
        else:
            #event.widget.create_line(self.start.x, self.start.y, self.end.x, self.end.y)
            #main_map.draw_relative_to = self.end - self.start
            # self._active.hold(self.end, self.step)
            pass

    def held(self, event):
        self._active.hold(event, self.step)
        self.step = Point( event.x, event.y )

    def scroll(self, event):
        #print("change: {}".format(event.delta))
        
        main_map.draw_relative_to += (main_map.origin_shift - Point(event.x,event.y) )*(1./main_map._zoom)
        main_map.origin_shift = Point(event.x, event.y)
        main_map._zoom += (event.delta/120.)*0.05
        main_map.draw( event.widget )

    def move(self,event):
        self._active.move( event )

    def to_brush(self):
        writer_control.set_brush_small()
        self._active = writer_control

    def to_hand(self):
        main_map._outline = None
        self._active = hand_control
    
controller = clicker_control()

def draw_buttons(frame):
    frame.update()

    hex_selector = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, background='white',width=frame.winfo_width(),height=int(0.22*frame.winfo_height() ) )
    write_type      = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, background='white',width=frame.winfo_width(),height=int(0.22*frame.winfo_height() ) )
    brushes      = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, background='white',width=frame.winfo_width(),height=int(0.22*frame.winfo_height() ) )
    tools        = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, background='white',width=frame.winfo_width(),height=int(0.22*frame.winfo_height() ) )

    hex_selector.grid(row=0, column=0)
    write_type.grid(row=1, column=0)
    brushes.grid(row=2, column=0)
    tools.grid(row=3, column=0)

    quit_button = tk.Button( frame, text = "Quit", command=master.destroy,width=int(0.95*frame.winfo_width()/font.measure("0")) )
    quit_button.grid(row=4, column=0)

    hex_selector.update()

    #master.destroy 

    master.update()

    button1 = tk.Button( hex_selector, text="Forest",     image = photo1, command=writer_control.switch_forest, width=0.45*hex_selector.winfo_width(), height=0.28*hex_selector.winfo_height())
    button2 = tk.Button( hex_selector, text="Grasslands", image = photo2, command=writer_control.switch_grass, width=0.45*hex_selector.winfo_width(), height=0.28*hex_selector.winfo_height())
    button3 = tk.Button( hex_selector, text="Desert",     image = photo3, command=writer_control.switch_desert, width=0.45*hex_selector.winfo_width(), height=0.28*hex_selector.winfo_height()) 
    button4 = tk.Button( hex_selector, text="Ocean",      image = photo4, command=writer_control.switch_ocean, width=0.45*hex_selector.winfo_width(), height=0.28*hex_selector.winfo_height()) 
    button5 = tk.Button( hex_selector, text="Arctic",     image = photo5, command=writer_control.switch_arctic, width=0.45*hex_selector.winfo_width(), height=0.28*hex_selector.winfo_height()) 
    button6 = tk.Button( hex_selector, text="Mountains",  image = photo6, command=writer_control.switch_mountain, width=0.45*hex_selector.winfo_width(), height=0.28*hex_selector.winfo_height())
    button1.grid(row=0,column=0)
    button2.grid(row=1,column=0)
    button3.grid(row=2,column=0)
    button4.grid(row=0,column=1)
    button5.grid(row=1,column=1)
    button6.grid(row=2,column=1)

    button_write      = tk.Button( write_type, text="add",   image = hex_add,    command=writer_control.set_write, width=0.45*write_type.winfo_width())
    button_erase      = tk.Button( write_type, text="remove",image = hex_remove, command=writer_control.set_erase, width=0.45*write_type.winfo_width())
    button_write.grid(row=0,column=0)
    button_erase.grid(row=0,column=1)

    button_one      = tk.Button( brushes, text="small", image = draw_one,     command=writer_control.set_brush_small, width=0.45*brushes.winfo_width())
    button_many      = tk.Button( brushes, text="large", image = draw_several, command=writer_control.set_brush_large, width=0.45*brushes.winfo_width())
    button_one.grid(row=0,column=0)
    button_many.grid(row=0,column=1)

     # define buttons 
    tools.update()
    draw_button     = tk.Button( tools, text="Draw",     command=controller.to_brush, width=int(0.29*frame.winfo_width()/font.measure("0")))
    select_button   = tk.Button( tools, text="Selector", command=savesave,  width=int(0.29*frame.winfo_width()/font.measure("0")))
    hand_button     = tk.Button( tools, text="Hand",     command=controller.to_hand,  width=int(0.29*frame.winfo_width()/font.measure("0")))
    draw_button.grid(row=0,column=0)
    select_button.grid(row=0,column=1)
    hand_button.grid(row=0,column=2)


     # get_flattened_points
    # redraw 
    # check active tool
    # act accordingly 
    #print(" click @ ({},{})".format(event.x, event.y))


    
# get screen information, create variables to use for the window size
screen_width  = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
gui_width = int(screen_ratio*screen_width)
gui_height= int(screen_ratio*screen_height)

# create window with specified size
master.title("Ben's HexMap")
master.resizable(width= False, height=False)
master.geometry('{}x{}'.format(gui_width, gui_height))

#put a frame on the left to hold the map
left_frame = tk.Frame( master, background='white', height=gui_height, width=int(0.8*gui_width))
left_frame.pack(side='left')
right_frame = tk.Frame( master, background='white', height=gui_height, width=int(0.2*gui_width))
right_frame.pack(side='right')
master.update()

draw_buttons(right_frame)

# put a frame on the right to hold buttons
#buttons = tk.Frame(lower_right, background='gray', height=gui_height, width=int(0.2*gui_width))
#buttons.pack(side='right')

# update the master object
master.update()

# put a canvas on the left so that we can draw
canvas = tk.Canvas(left_frame, background='white', height=left_frame.winfo_height(), width=left_frame.winfo_width())
canvas.bind("<Button-1>", controller.press)
canvas.bind("<ButtonRelease-1>", controller.release)
canvas.bind("<B1-Motion>",controller.held)
canvas.bind("<MouseWheel>",controller.scroll)
canvas.bind("<Motion>",controller.move)
canvas.pack()

if need_to_draw:
    for ID in main_map.catalogue:
        main_map.draw_one_hex( canvas, ID )

#update again
master.update()


master.mainloop()

# frame.destroy()

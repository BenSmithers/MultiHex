## #!/usr/bin/python3.6m

from point import Point
from hex import Hex
from hexmap import Hexmap
import tkinter as tk

master = tk.Tk()

screen_ratio = 0.8

main_map = Hexmap() 

class clicker_control:
    """
    Manages the mouse interface for to the canvas 
    """
    def __init__(self):
        self.start = Point(0.0, 0.0)
        self.step = Point(0.0, 0.0)
        self.end   = Point(0.0, 0.0)
    def press(self, event):
        self.step =  Point( event.x, event.y)
        self.start = Point( event.x, event.y)
    def release( self, event):
        self.end = Point(event.x, event.y)
        diff = self.start - self.end
        if diff.magnitude <=5.0:
            # get the nearest relevant ID
            loc_id = main_map.get_id_from_point( self.end )
            # calculate the center of a hex that would have that id
            new_hex_center = main_map.get_point_from_id( loc_id )
            # create a hex at that point, with a radius given by the current drawscale 
            new_hex= Hex( new_hex_center, main_map._drawscale )
            # register that hex in the hexmap 
            try:
                main_map.register_hex( new_hex, loc_id )
            except NameError:
                # if there is already a hex there, just set that hex as the active one
                main_map.set_active_hex( loc_id )
        else:
            #event.widget.create_line(self.start.x, self.start.y, self.end.x, self.end.y)
            #main_map.draw_relative_to = self.end - self.start
            pass

        main_map.draw(event.widget)

    def held(self, event): 
        move_by = Point(event.x - self.step.x, event.y - self.step.y)  
        main_map.draw_relative_to += Point( event.x - self.step.x, event.y - self.step.y )
        self.step = Point( event.x, event.y )
        main_map.draw( event.widget )   
    def scroll(self, event):
        #print("change: {}".format(event.delta))
        main_map._zoom += (event.delta/120.)*0.05
        main_map.draw( event.widget )

     # get_flattened_points
    # redraw 
    # check active tool
    # act accordingly 
    #print(" click @ ({},{})".format(event.x, event.y))

controller = clicker_control()
    
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

# put a frame on the right to hold buttons
buttons = tk.Frame(master, background='gray', height=gui_height, width=int(0.2*gui_width))
buttons.pack(side='right')

# update the master object
master.update()

# put a canvas on the left so that we can draw
canvas = tk.Canvas(left_frame, background='white', height=left_frame.winfo_height(), width=left_frame.winfo_width())
canvas.bind("<Button-1>", controller.press)
canvas.bind("<ButtonRelease-1>", controller.release)
canvas.bind("<B1-Motion>",controller.held)
canvas.bind("<MouseWheel>",controller.scroll)
canvas.pack()

#update again
master.update()

# define buttons 
draw_button = tk.Button( buttons, text="Draw Hex",     width=buttons.winfo_width(), command=None)
remove_button = tk.Button(buttons, text="Remove Data", width=buttons.winfo_width(), command=None)
quit_button   = tk.Button( buttons, text="Quit", width=buttons.winfo_width(), command = master.destroy )

draw_button.pack(side='top')
remove_button.pack(side='top')
quit_button.pack(side='bottom')

master.mainloop()

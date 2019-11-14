from point import Point
from hex import Hex
from hexmap import Hexmap, save_map, load_map

import random.random as rnd 

def make_basic_hex(arg1, arg2):
    new_one = Hex(arg1, arg2)
    new_one.biodiversity = 0.0
    new_one.humidity_base = 0.0
    new_one.temperature_base = 0.0


size = 'small'
out_file = './saves/generated.hexmap'

if size=='small':
    dimensions = [1080, 1920]
    n_peaks = 5
elif size=='large':
    dimensions = [2160, 3840]
    n_peaks = 20
else:
    raise Exception("'{}' size not implemented".format(size))

main_map = Hexmap()

#                Generate Mountain Peaks 
# ======================================================

for i in range( n_peaks ):
    while True:
        place = Point( rnd()*dimensions[0], rnd()*dimensions[1] )
        loc_id = main_map.get_id_from_point( place )
        new_hex_center = main_map.get_point_from_id( loc_id )
        
        new_hex = make_basic_hex( new_hex_center, main_map._drawscale)

        # it's unlikely, but possible that we sampled the same point multiple times 
        try:
            main_map.register_hex( new_hex, loc_id )
            # if it doesn't, break out of the while loop! 
            break 
        except NameError:
            # if that happens, just run through this again
            continue

#                Spread Land Around Peaks
# ======================================================


tile_creation = True
while tile_creation:

       pass  


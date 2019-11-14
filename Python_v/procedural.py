from point import Point
from hex import Hex
from hexmap import Hexmap, save_map, load_map
from special_hexes import *


import random as rnd 

def make_basic_hex(arg1, arg2):
    new_one = Hex(arg1, arg2)
    new_one.biodiversity = 0.0
    new_one.humidity_base = 0.0
    new_one.temperature_base = 0.0
    return( new_one )

size = 'small'
out_file = './saves/generated.hexmap'

if size=='small':
    dimensions = [1920, 1080]
    n_peaks = 25
elif size=='large':
    dimensions = [3840, 2160]
    n_peaks = 50
else:
    raise Exception("'{}' size not implemented".format(size))

main_map = Hexmap()

#                Generate Mountain Peaks 
# ======================================================

ids_to_propagate = []

for i in range( n_peaks ):
    while True:
        place = Point( rnd.random()*dimensions[0], rnd.random()*dimensions[1] )
        loc_id = main_map.get_id_from_point( place )
        new_hex_center = main_map.get_point_from_id( loc_id )
        
        new_hex = make_basic_hex( new_hex_center, main_map._drawscale)

        # it's unlikely, but possible that we sampled the same point multiple times 
        try:
            main_map.register_hex( new_hex, loc_id )
            ids_to_propagate.append( loc_id )
            # if it doesn't, break out of the while loop! 
            break 
        except NameError:
            # if that happens, just run through this again
            continue

#                Spread Land Around Peaks
# ======================================================

def point_is_in( point ):
    return( point.x < dimensions[0] and point.x > 0 and point.y < dimensions[1] and point.y>0)


# while there are still more to propagate! 
while len(ids_to_propagate)!=0:
    neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )
    
    # oceans generate oceans
    working_alt = main_map.catalogue[ids_to_propagate[0]]._altitude_base
    gen_ocean = not main_map.catalogue[ ids_to_propagate[0] ]._is_land
    for neighbor in neighbors:
        # get the neighbor's center
        place = main_map.get_point_from_id( neighbor )

        if not point_is_in(place):
            # if they aren't in the generation region, skip
            continue
            # now check, is the ID already in the catalogue ? 
        elif not neighbor in main_map.catalogue:
            
            # oceans only make new ocean
            if gen_ocean:
                new_hex = Ocean_Hex( place, main_map._drawscale )
            else:
                new_alt = working_alt - rnd.gauss(0.10,0.02)
                if new_alt<=0:
                    new_hex = Ocean_Hex(place,main_map._drawscale)
                else:
                    new_hex = make_basic_hex(place, main_map._drawscale)
                    new_hex._altitude_base = new_alt 
                    new_hex.fill = '#'+(hex(int(16-new_hex._altitude_base*16))[-1])+'b0'
            
            # if this throws an exception, I did something wrong and I want to know 
            main_map.register_hex( new_hex, neighbor )
            
            # we need to propagate the new neighbor too
            ids_to_propagate.append( neighbor )
        else:
            # that neighbor is just already registered
            continue
    # great, the neighbors are now there - let's pop this hex
    ids_to_propagate.pop(0)


#                      Add Noise! 
# ======================================================

for tile in main_map.catalogue.values():
    tile._altitude_base *= 0.90+ 0.2*( rnd.random() - 0.5 )


save_map( main_map, out_file )

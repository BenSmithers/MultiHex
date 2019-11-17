from point import Point
from hex import Hex
from hexmap import Hexmap, save_map, load_map
from special_hexes import *

import sys

import random as rnd 

def make_basic_hex(arg1, arg2):
    new_one = Hex(arg1, arg2)
    new_one.biodiversity = 0.0
    new_one.humidity_base = 0.0
    new_one.temperature_base = 0.0
    return( new_one )

size = 'large'
out_file = './saves/generated.hexmap'

if size=='small':
    dimensions = [1920, 1080]
    n_peaks = 15
elif size=='large':
    dimensions = [3840, 2160]
    n_peaks = 25
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
        new_hex.genkey = '11000000'
        new_hex.fill = (99,88,60)
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

def generate_hex(parent, center, radius):
    droll = rnd.random()
    #  ------------------ check if this is ridgeline. If so generate mountains and ridge 
    
    this = '0'
    try:
        this = parent.genkey
    except AttributeError:
        print( type(parent))
        print(parent)
        sys.exit()
    
    if parent.genkey[0]=='1':
        # ridgeline
        if droll > 0.62: 
            new_hex = Mountain_Hex(center, radius)
            new_hex.genkey = '11000000'
            new_hex.fill = (99,88,60)
            new_hex._altitude_base = 1.0
            return( new_hex , True)
        elif droll > 0.05: # plain old mountain
            new_hex = Mountain_Hex(center, radius)
            new_hex._altitude_base = parent._altitude_base - rnd.gauss(0.05,0.02)
            new_hex.genkey = '01000000'
            return( new_hex, False )
        elif droll > 0.01:
            new_hex = Forest_Hex(center, radius )
            new_hex._altitude_base = parent._altitude_base - rnd.gauss(0.25,0.02)
            new_hex.genkey = '01010100'
            return(new_hex,True)
        else:
            new_hex = Grassland_Hex(center, radius )
            new_hex._altitude_base = parent._altitude_base - rnd.gauss(0.25,0.02)
            new_hex.genkey = '01110100'
            return(new_hex, False)
    # ------------------------- okay, now is this ocean?? Generate small islands every so often
    if parent.genkey[-2:]=='01':
        # this is ocean, but not island
        if droll <0.01:
            new_hex = Grassland_Hex( center, radius )
            new_hex.genkey = '00000011'
            new_hex._altitude_base = 0.0
            return( new_hex, True )
        else:
            new_hex = Ocean_Hex( center, radius )
            new_hex.genkey = '00000001'
            return( new_hex, True )
    elif parent.genkey[-2:]=='11': # island hexes have a small chance of being two-fers 
        if droll > 0.995:
            new_hex = Grassland_Hex(center, radius)
            new_hex.genkey = '00000011'
            new_hex._altitude_base = 0.0
            return(new_hex, False)
        elif droll > 0.97:
            new_hex = Forest_Hex(center, radius)
            new_hex.genkey = '00000011'
            new_hex._altitude_base = 0.0
            return(new_hex, False)
        else:
            new_hex = Ocean_Hex(center,radius)
            new_hex.genkey = '00000001'
            return( new_hex, False)

    # now doing normal generation 
    if parent.genkey[1]=='1': ## for any mountainous terrain
        new_alt = parent._altitude_base - rnd.gauss(0.10,0.02)
        if new_alt < 0: #woah! Dropped to the ocean
            new_hex = Ocean_Hex(center, radius)
            new_hex.genkey = '00000001'
            new_hex._altitude_base = new_alt
            return(new_hex, True)
        elif new_alt > 0.5:
            # standard mountain generation
            if droll > 0.65:
                new_hex = Mountain_Hex(center, radius)
                new_hex.genkey = '01000100'
                new_hex._altitude_base = new_alt
                return(new_hex,False)
            elif droll > 0.30:
                new_hex = Forest_Hex(center, radius)
                new_hex.genkey = '00010100'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
            elif droll > 0.05:
                new_hex = Grassland_Hex(center, radius)
                new_hex.genkey = '00110100'
                new_hex._altitude_base = new_alt
                return( new_hex, False)
            else:
                new_hex = Ocean_Hex(center, radius)
                new_hex.genkey = '00110010'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
        else:
            # falling down to a lower altitude 
            if droll > 0.66:
                new_hex = Forest_Hex(center, radius)
                new_hex.genkey = '00010100'
                new_hex._altitude_base = new_alt
                return( new_hex, False )
            elif droll > 0.33:
                new_hex = Grassland_Hex(center, radius)
                new_hex.genkey = '00110100'
                new_hex._altitude_base = new_alt
                return(new_hex, True)
            else:
                new_hex = Ocean_Hex(center, radius)
                new_hex.genkey = '00110010'
                new_hex._altitude_base = new_alt
                return(new_hex, True)
    # this exa
    if parent.genkey[2:] == '110100': # grassland
        new_alt = parent._altitude_base - rnd.gauss(0.05, 0.02)
        if new_alt < 0.0:
            new_hex = Ocean_Hex(center, radius)
            new_hex.genkey = '00000001'
            new_hex._altitude_base = 0.0
            return(new_hex, False)
        else:
            if droll>0.10:
                new_hex = Grassland_Hex(center,radius)
                new_hex.genkey = '00110100'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
            elif droll > 0.09:
                new_hex = Forest_Hex(center, radius)
                new_hex.genkey = '00010100'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
            elif droll > 0.005:
                new_hex = Desert_Hex(center, radius)
                new_hex.genkey = '00100000'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
            else:
                new_hex = Ocean_Hex(center, radius)
                new_hex.genkey = '00110010'
                new_hex._altitude_base = new_alt
                return(new_hex, False)

    if parent.genkey[2:] == '010100': # forest
        new_alt = parent._altitude_base - rnd.gauss(0.10, 0.03)
        if new_alt < 0.0:
            new_hex = Ocean_Hex(center, radius)
            new_hex.genkey = '00000001'
            new_hex._altitude_base = 0.0
            return(new_hex, True)
        else:
            if droll>0.24:
                new_hex = Forest_Hex(center, radius)
                new_hex.genkey = '00010100'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
            elif droll > 0.235:
                new_hex = Ocean_Hex(center, radius)
                new_hex.genkey = '00110010'
                new_hex._altitude_base = new_alt
                return( new_hex, False)
            else:
                new_hex = Grassland_Hex(center, radius)
                new_hex.genkey = '00110100'
                new_hex._altitude_base = new_alt
                return(new_hex, False)

    if parent.genkey[2:] == '110010': # lake 
        if droll >0.99:
            new_hex = Ocean_Hex(center, radius)
            new_hex.genkey = '00110010'
            new_hex._altitude_base = parent._altitude_base
            return(new_hex, False)
        elif droll >0.80:
            new_hex = Forest_Hex(center,radius) 
            new_hex._altitude_base = parent._altitude_base + rnd.gauss(0.05, 0.02)
            new_hex.genkey = '00010100'
            return(new_hex, False)
        else:
            new_hex = Grassland_Hex(center,radius)
            new_hex._altitude_base = parent._altitude_base+rnd.gauss(0.05, 0.02)
            new_hex.genkey = '00110100'
            return(new_hex, False)

    if parent.genkey[2:] == '100000': # desert
        new_alt = parent._altitude_base - rnd.gauss(0.1, 0.05)
        if new_alt < 0:
            new_hex = Ocean_Hex(center, radius)
            new_hex.genkey = '00000001'
            new_hex._altitude_base = 0.0
            return(new_hex ,False)
        else:
            if droll > 0.10:
                new_hex = Desert_Hex(center, radius)
                new_hex.genkey = '00100000'
                new_hex._altitude_base = new_alt
                return(new_hex, True)
            else:
                new_hex = Grassland_Hex(center, radius)
                new_hex.genkey = '00110100'
                new_hex._altitude_base = new_alt
                return(new_hex, False)
    
    # not sure how I got here, so I'll just make a random hex
    print( "warning: default hex!")
    print( parent.genkey )
    new_hex = Grassland_Hex(center, radius)
    new_hex.genkey = '00110100'
    new_hex._altitude_base = parent._altitude_base - rnd.gauss(0.10,0.05)
    return(new_hex, False)

# while there are still more to propagate! 
while len(ids_to_propagate)!=0:
    neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )
    
    # oceans generate oceans
    
    for neighbor in neighbors:
        # get the neighbor's center
        place = main_map.get_point_from_id( neighbor )

        if not point_is_in(place):
            # if they aren't in the generation region, skip
            continue
            # now check, is the ID already in the catalogue ? 
        elif not neighbor in main_map.catalogue:
            new_hex, start = generate_hex(main_map.catalogue[ids_to_propagate[0]],place, main_map._drawscale )    
            # if this throws an exception, I did something wrong and I want to know 
            main_map.register_hex( new_hex, neighbor )
            
            # we need to propagate the new neighbor too
            #if start:
            #    ids_to_propagate.insert(0, neighbor)
            #else:
            ids_to_propagate.append( neighbor )
        else:
            # that neighbor is just already registered
            continue
    # great, the neighbors are now there - let's pop this hex
    ids_to_propagate.pop(0)


#                      Add Noise! 
# ======================================================

for tile in main_map.catalogue.values():
 #   tile._altitude_base *= 0.90+ 0.2*( rnd.random() - 0.5 )
    if tile._altitude_base !=0:
        tile.fill = ( 255- int(255*tile._altitude_base), 180, 0)

save_map( main_map, out_file )

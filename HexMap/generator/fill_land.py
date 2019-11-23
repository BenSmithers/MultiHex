from HexMap.point import Point
from HexMap.hex import Hex
from HexMap.hexmap import Hexmap, save_map, load_map
from HexMap.special_hexes import *
from HexMap.generator.util import *

from numpy import arccos 
from numpy import histogram
from math import exp, floor, sqrt, e, pi

import random as rnd
import os
import json

def generate(size, sim = '../saves/generated.hexmap' ):

    # load the config file
    file_object = open( 'config.json', 'r' )
    config  = json.load( file_object )
    file_object.close()

    # check to make sure it uses a supported preset 
    if not (size in config):
        raise Exception("Unsupported size: {}".format(size) )
    else:
        dimensions = config[size]['mountains']['dimensions']
        config = config[size]['land']

    
    land_spread     = config['land_spread']
    land_width      = config['land_width']
    mnt_thicc       = config['mnt_thicc']
    water_spread    = config['water_spread']
    water_width     = config['water_width']
    

    main_map = load_map( sim )
          
    #         Add mountainous terrain around Ridgelines
    # ======================================================
    print("Spreading Mountains")
    
    ids_to_propagate = list( main_map.catalogue.keys())

    # average thickness of the mountains

    print("    average mountain thickness {}".format( mnt_thicc ))

    while len(ids_to_propagate) != 0:
        
        parent = main_map.catalogue[ids_to_propagate[0]]
        
        if parent.genkey[0]=='1':
            perc = 0. 
        else:
            if mnt_thicc <= 1.:
                perc = 1.
            else:
                perc = 1.0/mnt_thicc
        

        if rnd.random() > (1. - perc):
            ids_to_propagate.pop(0)
        else:
            # equal probability of spreead
            neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )
            
            sanitized_neighbors = []
            for index in range(len(neighbors)):
                if neighbors[index] not in main_map.catalogue:
                    sanitized_neighbors.append( neighbors[index] )

            # now we have a sanitized list of ids guaranted to be uninstantiated
            if len(sanitized_neighbors)==0:
                ids_to_propagate.pop(0)
                continue
            else:
                which = int(floor( len(sanitized_neighbors )*rnd.random() ))
                if which >= len(sanitized_neighbors):
                    raise Exception("wtf??? {}".format(which))
                center = main_map.get_point_from_id( sanitized_neighbors[which] )

                if not point_is_in(center, dimensions):
                    ids_to_propagate.pop(0)
                    continue

                new_hex = Mountain_Hex( center, main_map._drawscale)
                new_hex.genkey = '01000000'
                
                alt_shift = parent._altitude_base - rnd.gauss(0.25, 0.05)
                if alt_shift < 0.2:
                    new_hex._altitude_base = 0.2
                else:
                    new_hex._altitude_base = alt_shift

                # register the hex, add it to the appendables. 
                # if this throws an error, don't catch. That means I made logic mistakes 
                main_map.register_hex( new_hex, sanitized_neighbors[which] )
                ids_to_propagate.append( sanitized_neighbors[which] )
                ids_to_propagate.pop(0)


    print("Spread Land Out")

    print("    Land Spread Factor  {} +/- {}".format(land_spread, land_width))
    print("    Ocean Spread Factor {} +/- {}".format(water_spread, water_width))

    ids_to_propagate = list( main_map.catalogue.keys())

    while len(ids_to_propagate)!=0:
        parent = main_map.catalogue[ids_to_propagate[0]]
        if parent.genkey[0]=='1': # can pretty much guarantee these aren't exposed
            ids_to_propagate.pop(0)
            continue
        else:
            neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )

            sanitized_neighbors = []
            for neighbor in neighbors:
                if neighbor not in main_map.catalogue:
                    sanitized_neighbors.append( neighbor )
            
            if len(sanitized_neighbors)==0:
                ids_to_propagate.pop(0)
                continue
            else:
                # okay, so now we need to create the neighbors... 
                for neighbor in sanitized_neighbors:
                    center = main_map.get_point_from_id( neighbor )
                    if not point_is_in(center, dimensions):
                        continue

                    if parent._is_land:
                        new_alt = parent._altitude_base - rnd.gauss(land_spread, land_width)
                    else:
                        new_alt = parent._altitude_base - rnd.gauss(water_spread, water_width)

                    if new_alt > 0:
                        new_hex = Grassland_Hex( center,main_map._drawscale )
                        new_hex._is_land = True
                    else:
                        new_hex = Ocean_Hex( center, main_map._drawscale)
                        new_hex._is_land = False

                    new_hex._altitude_base = new_alt 
                    main_map.register_hex( new_hex, neighbor )
                    ids_to_propagate.append( neighbor )
                ids_to_propagate.pop(0)


    if not os.path.isdir("../saves"):
        os.mkdir("../saves")

    save_map( main_map, sim )
    
    n_rounds = 2
    print("Performing {} rounds of smoothing".format(n_rounds))
    
    for i in range( n_rounds ):
        smooth( ['alt'], sim )

if __name__=='__main__':
    generate('cont')

from MultiHex.core import Point, Hexmap, save_map, load_map, Region
from MultiHex.map_types.overland import *
from MultiHex.generator.util import *

from numpy import arccos 
from numpy import histogram
from math import exp, floor, sqrt, e, pi

import random as rnd
import os
import json
import sys

"""
Uses some simple thresholds to determine what kind of Hex a given Hex is

Is it a forest? A Desert? Let's find out! 
"""

def generate(size, sim = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap')):

    # load the config file
    file_object = open( os.path.join( os.path.dirname(__file__), 'config.json'), 'r' )
    config  = json.load( file_object )
    file_object.close()

    # check to make sure it uses a supported preset 
    if not (size in config):
        raise Exception("Unsupported size: {}".format(size) )
    else:
        dimensions = config[size]['mountains']['dimensions']
        config = config[size]['regions']


    # these aren't used, obviously. 
    # will want to swap these out for the threshholds used 
    n_regions       = config['n_regions']
    reg_size        = config['reg_size']
    

    main_map = load_map( sim )
    
    #                     Set Arctic Circle
    # ===========================================================

    # if tempterature < 0.1 --> arctic circle

    colors = hcolor()

    for ID in main_map.catalogue:
        # most important, arctic circle! 
        this_hex = main_map.catalogue[ID]
        if not this_hex._is_land:
            continue
        if this_hex.genkey[0] == '1':
            main_map.catalogue[ID].fill = colors.mount
            main_map.catalogue[ID].biome = "mountain"
            continue
        elif this_hex.genkey[1] == '1':
            main_map.catalogue[ID].fill = colors.ridge
            main_map.catalogue[ID].biome = "mountain"
            continue

        if this_hex._temperature_base<0.08:
            # this is very cold. It's an arctic hex
            main_map.catalogue[ID].fill = colors.arcti
            main_map.catalogue[ID].biome = "arctic"
        elif this_hex._temperature_base < 0.92:
            if this_hex._altitude_base < 0.6:
                # lowlands 
                # we in the the temperate regions
                if this_hex._rainfall_base < 0.4:
                    # arid - desert
                    main_map.catalogue[ID].fill = colors.deser
                    main_map.catalogue[ID].biome = "desert"
                elif this_hex._rainfall_base < 0.7:
                    # temperate - grass
                    main_map.catalogue[ID].fill = colors.grass
                    main_map.catalogue[ID].biome = "grassland"
                else:
                    # rainy - forest
                    main_map.catalogue[ID].fill = colors.fores
                    main_map.catalogue[ID].biome = "forest"
            else:
                if this_hex._rainfall_base < 0.3:
                    main_map.catalogue[ID].fill = colors.deser
                    main_map.catalogue[ID].biome = "desert"
                elif this_hex._rainfall_base < 0.4:
                    main_map.catalogue[ID].fill = colors.grass
                    main_map.catalogue[ID].biome = "grassland"
                else:
                    main_map.catalogue[ID].fill = colors.fores
                    main_map.catalogue[ID].biome = "forest"
        else:
            # within the tropics
            if this_hex._rainfall_base < 0.2:
                main_map.catalogue[ID].fill = colors.deser
                main_map.catalogue[ID].biome = "desert"
            elif this_hex._rainfall_base < 0.4:
                main_map.catalogue[ID].fill = colors.savan
                main_map.catalogue[ID].biome = "grassland"
            elif this_hex._rainfall_base < 0.6:
                main_map.catalogue[ID].fill = colors.grass
                main_map.catalogue[ID].biome = "grassland"
            else:
                main_map.catalogue[ID].fill = colors.rainf
                main_map.catalogue[ID].biome = "forest"
        
        main_map.catalogue[ID].rescale_color()

    # seed region generation. Just put them out randomly
    while len(main_map.rid_catalogue.keys()) < n_regions:
        # pick a point
        spot = Point( dimensions[0]*rnd.random(), dimensions[1]*rnd.random() )

        this_id = main_map.get_id_from_point( spot )
        this_hex = main_map.catalogue[ this_id ]

        if not this_hex._is_land:
            # Not making regions in ocean... that's boring
            continue

        new_region = Region( this_id , main_map )
        main_map.register_new_region( new_region )

    # grow each region
    from collections import deque
    for rid in main_map.rid_catalogue:
        this_region = main_map.rid_catalogue[rid]
        ids_to_propagate = deque(this_region.ids)

        reg_type = main_map.catalogue[ ids_to_propagate[0] ].biome
        this_region.name = create_name( reg_type )

        # reg_size 
        while len(ids_to_propagate)!=0:
            # if this thing is too big, we have a 50/50 chance to just skip this part entirely 
            if len(this_region.ids)>reg_size and rnd.random()>0.50:
                ids_to_propagate.popleft()
                continue

            # grab the first ID, get its neighbors
            neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )
            for neighbor in neighbors:
                # add the neighbor to this region if it matches the biome and isn't in a region
                if neighbor in main_map.id_map:
                    continue
                if neighbor not in main_map.catalogue:
                    continue
                if main_map.catalogue[neighbor].biome==reg_type:
                    main_map.add_to_region( rid, neighbor )
                    ids_to_propagate.append( neighbor )
            ids_to_propagate.popleft()


    
    # loop over the arctic hexes and spread them a little bit


    save_map( main_map, sim )
    

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

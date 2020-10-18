from MultiHex.core import Point, Hexmap, save_map, load_map, Region, RegionMergeError, Hex
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
        dimensions = [config[size]['mountains']['values']['dimx'], config[size]['mountains']['values']['dimy']]
        config = config[size]['regions']['values']

    
    # load the HexMap
    main_map = load_map( sim )
    
    #                  ASSIGN COLORS AND CLIMATE 
    # ===========================================================

    # explicitly setting tileset to keep up appearances 
    this_climatizer = Climatizer(tileset="standard")

    for ID in main_map.catalog:
        if main_map.catalog[ID].genkey[0]=='1':
            main_map.catalog[ID].fill = (99,88,60)
            main_map.catalog[ID].biome = "mountain"
            continue
        if main_map.catalog[ID].genkey[1]=='1':
            main_map.catalog[ID].fill = (158,140,96)
            main_map.catalog[ID].biome = "mountain"
            continue
      
        this_climatizer.apply_climate_to_hex( main_map.catalog[ID] )
        main_map.catalog[ID].rescale_color()


    #                      MAKE BIOMES (REGIONS)
    # ===========================================================

    n_regions       = config['n_regions']
    reg_size        = config['reg_size']

    # are faster at adding things to the sides 
    from collections import deque
    r_layer = 'biome'
    main_map.rid_catalog[r_layer] = {}
    main_map.id_map[r_layer] = {}

    # seed region generation. Just put them out randomly
    while len(main_map.rid_catalog[r_layer].keys()) < n_regions:
        # pick a point
        spot = Point( dimensions[0]*rnd.random(), dimensions[1]*rnd.random() )

        this_id = main_map.get_id_from_point( spot )
        try:
            if this_id in main_map.id_map[r_layer]:
                continue
        except KeyError:
            pass

        try:
            this_hex = main_map.catalog[ this_id ]
        except KeyError:
            continue 

        if not this_hex._is_land:
            # Not making regions in ocean... that's boring
            continue

        this_region  = Region( this_id , main_map )
        rid = main_map.register_new_region( this_region, r_layer )


        ids_to_propagate = deque(this_region.ids)

        if main_map.catalog[ids_to_propagate[0]].river_border[0] or main_map.catalog[ids_to_propagate[0]].river_border[1]:
            reg_type = 'river'
        else:
            reg_type = main_map.catalog[ ids_to_propagate[0] ].biome
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
                if neighbor in main_map.id_map[r_layer]:
                    continue
                if neighbor not in main_map.catalog:
                    continue
                try:
                    if reg_type=='river':
                        if main_map.catalog[neighbor].river_border[0] or main_map.catalog[neighbor].river_border[1]:
                            main_map.add_to_region( rid, neighbor, r_layer )
                            ids_to_propagate.append( neighbor )
                    elif main_map.catalog[neighbor].biome==reg_type:
                        main_map.add_to_region( rid, neighbor, r_layer )
                        ids_to_propagate.append( neighbor )
                except RegionMergeError:
                    pass
            ids_to_propagate.popleft()


    
    # loop over the arctic hexes and spread them a little bit

    save_map( main_map, sim )
    

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

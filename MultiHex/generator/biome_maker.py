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

colors = hcolor()

# each entry has endcaps: 0.0 and 1.0
# arctic, temperate, hot
temperature_thresholds = [0.0 , 0.08, 0.92, 1.0]
# arid, temperate, wet 
rainfall_thresholds = [0.0, 0.3, 0.7 , 1.0]
# no dependence 
altitude_thresholds = [0.0, 0.5, 1.0 ]

#        temp: cold ---> hot 
#       dry 
#         |
# Rain:   |
#         V
#       Rainy
#
# Plus one extra dimension for the altitude dependence 

names = [ # lowlands
        [[ "arctic", "grassland", "desert"],
         [ "arctic", "grassland",    "savanah"],
         [ "tundra", "forest",  "rainforest"]],
          # highlands
        [[ "arctic", "grassland","grassland"],
         [ "tundra", "forest", "grassland"],
         [ "tundra", "tundra", "forest"]]
        ]
assert( len(names)      == ( len(altitude_thresholds)-1 ) )
assert( len(names[0])   == ( len(rainfall_thresholds)-1 ) )
assert( len(names[0][0])== ( len(temperature_thresholds)-1))

def apply_biome( target ):
    """
    Assigns a hex its biome and its color. Requires an entry in the 'hcolor' object in the overland map type script with an attribute name corresponding to the biome name in the 'names' table above

    @param target   - the hex
    """
   
    # oceans, ridges, and mountains aren't restricted to the same rules
    if not target._is_land:
        target.fill = colors.ocean
        target.biome= "ocean"
        return
    if target.genkey[0]=='1':
        target.fill = colors.ridge
        target.biome = "mountain"
        return
    if target.genkey[1]=='1':
        target.fill = colors.mountain
        target.biome = "mountain"
        return

    def get_index( target, thresholds, hex_quantity):
        """
        Takes a hex and one of the thresholds (rain, altitude, or temperature). Returns which range the hex falls in

        @param target       - the Hex
        @param thresholds   - the set of thresholds
        @param hex_quantity - the string name of the Hexes quantity to test against
        """

        index = 0
        if target._rainfall_base <= thresholds[0]:
            index = 0
        elif target._rainfall_base >= thresholds[-1]:
            index = -1 
        else:
            while (thresholds[index] < getattr( target, hex_quantity) ):
                index += 1
            index -= 1
        return( index )

    rain_index          = get_index( target, rainfall_thresholds, "_rainfall_base" )
    temperature_index   = get_index( target, temperature_thresholds, "_temperature_base" )
    altitude_index      = get_index( target, altitude_thresholds, "_altitude_base" )
    
    target.biome = names[ altitude_index ][rain_index][temperature_index]
    try:
        target.fill = getattr( colors, target.biome )
    except AttributeError:
        target.fill = (0.0, 0.0, 0.0 )

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



    for ID in main_map.catalogue:
        apply_biome( main_map.catalogue[ID] )
        main_map.catalogue[ID].rescale_color()

    from collections import deque
    r_layer = 'biome'
    main_map.rid_catalogue[r_layer] = {}
    main_map.id_map[r_layer] = {}

    # seed region generation. Just put them out randomly
    while len(main_map.rid_catalogue[r_layer].keys()) < n_regions:
        # pick a point
        spot = Point( dimensions[0]*rnd.random(), dimensions[1]*rnd.random() )

        this_id = main_map.get_id_from_point( spot )
        try:
            if this_id in main_map.id_map[r_layer]:
                continue
        except KeyError:
            pass

        try:
            this_hex = main_map.catalogue[ this_id ]
        except KeyError:
            continue 

        if not this_hex._is_land:
            # Not making regions in ocean... that's boring
            continue

        this_region  = Region( this_id , main_map )
        rid = main_map.register_new_region( this_region, r_layer )


        ids_to_propagate = deque(this_region.ids)

        if main_map.catalogue[ids_to_propagate[0]].river_border[0] or main_map.catalogue[ids_to_propagate[0]].river_border[1]:
            reg_type = 'river'
        else:
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
                if neighbor in main_map.id_map[r_layer]:
                    continue
                if neighbor not in main_map.catalogue:
                    continue
                try:
                    if reg_type=='river':
                        if main_map.catalogue[neighbor].river_border[0] or main_map.catalogue[neighbor].river_border[1]:
                            main_map.add_to_region( rid, neighbor, r_layer )
                            ids_to_propagate.append( neighbor )
                    elif main_map.catalogue[neighbor].biome==reg_type:
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

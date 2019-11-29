from MultiHex.point import Point
from MultiHex.hex import Hex
from MultiHex.hexmap import Hexmap, save_map, load_map
from MultiHex.special_hexes import *
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
        config = config[size]['land']


    # these aren't used, obviously. 
    # will want to swap these out for the threshholds used 
    land_spread     = config['land_spread']
    land_width      = config['land_width']
    mnt_thicc       = config['mnt_thicc']
    water_spread    = config['water_spread']
    water_width     = config['water_width']
    

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
            continue
        elif this_hex.genkey[1] == '1':
            main_map.catalogue[ID].fill = colors.ridge
            continue

        if this_hex._temperature_base<0.08:
            # this is very cold. It's an arctic hex
            main_map.catalogue[ID].fill = colors.arcti
        elif this_hex._temperature_base < 0.92:
            if this_hex._altitude_base < 0.6:
                # lowlands 
                # we in the the temperate regions
                if this_hex._rainfall_base < 0.4:
                    # arid - desert
                    main_map.catalogue[ID].fill = colors.deser
                elif this_hex._rainfall_base < 0.7:
                    # temperate - grass
                    main_map.catalogue[ID].fill = colors.grass
                else:
                    # rainy - forest
                    main_map.catalogue[ID].fill = colors.fores
            else:
                if this_hex._rainfall_base < 0.3:
                    main_map.catalogue[ID].fill = colors.deser
                elif this_hex._rainfall_base < 0.4:
                    main_map.catalogue[ID].fill = colors.grass
                else:
                    main_map.catalogue[ID].fill = colors.fores
        else:
            # within the tropics
            if this_hex._rainfall_base < 0.4:
                main_map.catalogue[ID].fill = colors.savan
            elif this_hex._rainfall_base < 0.6:
                main_map.catalogue[ID].fill = colors.grass
            else:
                main_map.catalogue[ID].fill = colors.rainf
        
        main_map.catalogue[ID].rescale_color()
    # loop over the arctic hexes and spread them a little bit

    save_map( main_map, sim )
    

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

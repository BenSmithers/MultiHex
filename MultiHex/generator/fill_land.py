from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.map_types.overland import *
from MultiHex.generator.util import *
from MultiHex.generator.noise import perlinize
from MultiHex.logger import Logger

from numpy import arccos 
from numpy import histogram
from math import exp, floor, sqrt, e, pi

import random as rnd
import os
import json

def generate(size, sim = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap'), **kwargs):
    """
    Follows the ridge spawning.

    Spreads land and ocean around those ridges until the world is filled up 
    """
    known_kwargs = [ 
        "temp_range",
        "rain_range",
        "sea_level"
    ]

    # load the config file
    file_object = open( os.path.join( os.path.dirname(__file__), 'config.json'), 'r' )
    config  = json.load( file_object )
    file_object.close()

    # check to make sure it uses a supported preset 
    if not (size in config):
        raise Exception("Unsupported size: {}".format(size) )
    else:
        dimensions = [ config[size]['mountains']['values']['dimx'], config[size]['mountains']['values']['dimy']]
        config = config[size]['land']['values']

    
    # avearge decrease in altitude from one regular land tile to another
    land_spread     = config['land_spread']
    # standard deviation 
    land_width      = config['land_width']

    # average thickness of mountainness around ridgeline 
    mnt_thicc       = config['mnt_thicc']

    # average decrease in elevation from water tile to another Plus its standard deviatino
    water_spread    = config['water_spread']
    water_width     = config['water_width']
    

    main_map = load_map( sim )
          
    #         Add mountainous terrain around Ridgelines
    # ======================================================
    Logger.Log("Spreading Mountains")
    
    ids_to_propagate = list( main_map.catalog.keys())

    # average thickness of the mountains

    Logger.Log("    average mountain thickness {}".format( mnt_thicc ))

    while len(ids_to_propagate) != 0:
        
        parent = main_map.catalog[ids_to_propagate[0]]
        
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
                if neighbors[index] not in main_map.catalog:
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

                new_hex = OHex( center, main_map._drawscale)
                new_hex.genkey = '01000000'
                new_hex._altitude_base = 1.0
                
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


    Logger.Log("Spread Land Out")

    Logger.Log("    Land Spread Factor  {} +/- {}".format(land_spread, land_width))
    Logger.Log("    Ocean Spread Factor {} +/- {}".format(water_spread, water_width))

    ids_to_propagate = list( main_map.catalog.keys())

    while len(ids_to_propagate)!=0:
        parent = main_map.catalog[ids_to_propagate[0]]
        if parent.genkey[0]=='1': # can pretty much guarantee these aren't exposed
            ids_to_propagate.pop(0)
            continue
        else:
            neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )

            sanitized_neighbors = []
            for neighbor in neighbors:
                if neighbor not in main_map.catalog:
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
                        new_hex = OHex( center,main_map._drawscale )
                        new_hex._is_land = True
                    else:
                        new_hex = OHex( center, main_map._drawscale)
                        new_hex._is_land = False
                        new_hex.name = "ocean"

                    new_hex._altitude_base = new_alt 
                    main_map.register_hex( new_hex, neighbor )
                    ids_to_propagate.append( neighbor )
                ids_to_propagate.pop(0)

    if not os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'saves')):
        os.mkdir(os.path.join( os.path.dirname(__file__), '..','saves'))

    save_map( main_map, sim )
    
    n_rounds = 2
    print("Performing {} rounds of smoothing".format(n_rounds))
        
    # this process usually leaves the map super gross looking, so I do some smoothing where I just average the elevation around the hex
    for i in range( n_rounds ):
        smooth( ['alt'], sim )

    perlinize(sim)

    if "sea_level" in kwargs:
        main_map = load_map( sim )
        scale = kwargs["sea_level"][0]
        shift = kwargs["sea_level"][1]

        def rescale(alt):
            return (alt-1.0)*scale + shift +1.0

        for ID in main_map.catalog.keys():
            main_map.catalog[ID].set_altitude( rescale(main_map.catalog[ID].altitude) )
            if main_map.catalog[ID].altitude>0:
                main_map.catalog[ID]._is_land = True
            else:
                main_map.catalog[ID]._is_land = False

        save_map( main_map, sim )

if __name__=='__main__':
    generate('cont')

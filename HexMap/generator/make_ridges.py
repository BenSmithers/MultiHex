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

def make_basic_hex(arg1, arg2):
    new_one = Hex(arg1, arg2)
    new_one._biodiversity = 0.0
    new_one._rainfall_base = 0.0
    new_one._temperature_base = 0.0
    return( new_one )

def generate(size, sim = '../saves/generated.hexmap'):

    # load the config file
    file_object = open( 'config.json', 'r' )
    config  = json.load( file_object )
    file_object.close()

    # check to make sure it uses a supported preset 
    if not (size in config):
        raise Exception("Unsupported size: {}".format(size) )
    else:
        config = config[size]['mountains']


    # load presets 
    dimensions = config['dimensions']
    n_peaks = config['n_peaks']
    if size=='cont':
        zones = config['zones']

    main_map = Hexmap()

    #                Generate Mountain Peaks 
    # ======================================================
    print("Seeding Mountain Peaks")

    distribution_mean   = 0.65*dimensions[0]
    distribution_width  = 0.20*dimensions[0]
    print("    Y-Centered at {} +/- {}".format( distribution_mean, distribution_width))
    print("    Uniform Y Distribution")

    ids_to_propagate = []


    if size=='small' or size=='large':
        for i in range( n_peaks ):
            while True:
                place = Point( rnd.gauss(distribution_mean, distribution_width), rnd.random()*dimensions[1] )
                if not point_is_in( place , dimensions ):
                    # try again... 
                    continue
                
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

    if size=='cont':
        for i in range(zones):
            x_center = 0.80*rnd.random()*dimensions[0] + 0.10*dimensions[0]
            y_cos  = 1.8*rnd.random() - 0.9
            y_center = arccos( y_cos )*dimensions[1]/( pi )
            for j in range(n_peaks):
                while True:
                    place = Point( rnd.gauss( x_center, 300), rnd.gauss( y_center, 300) )
                    if not point_is_in(place, dimensions):
                        continue 
                    loc_id = main_map.get_id_from_point( place )
                    new_hex_center = main_map.get_point_from_id( loc_id )

                    new_hex = make_basic_hex(new_hex_center, main_map._drawscale)
                    new_hex.genkey = '11000000'
                    new_hex.fill = (99,88,60)
                    try:
                        main_map.register_hex( new_hex, loc_id )
                        ids_to_propagate.append( loc_id )
                        break
                    except NameError:
                            continue
    
    
    #                  Create ridgelines 
    # =====================================================
    print("Forking Ridglines")

    # choose a direction the ridgeline will preferably go, and spread around that direction

    direction = 360*rnd.random()
    sigma       = config['sigma']
    avg_range   = config['avg_range']


    # build the neighbor function
    distribution = get_distribution( direction, sigma)
    print("    Ridgeline Direction: {} +/- {}".format(direction, sigma))


    print("    Ridgline Avg Length: {}".format(avg_range))

    angles = [ 90., -90., 30., -30., 150., -150.]
    neighbor_weights = [ distribution( angle ) for angle in angles]

    # calculate CDF of neighbor weights 
    neighbor_cdf = [0. for weight in neighbor_weights]
    for index in range(len(neighbor_weights)):
        if index == 0:
            neighbor_cdf[0] = neighbor_weights[0]
        else:
            neighbor_cdf[index] = neighbor_cdf[index - 1] + neighbor_weights[index]


    #print("Using neighbor weights {}".format(neighbor_weights))
    #print("and neighbor cdf {}".format(neighbor_cdf))

    while len(ids_to_propagate)!=0:
        if rnd.random()>(1.-(1./avg_range)):
            #terminate this ridgeline
            ids_to_propagate.pop(0)
            continue
        else:
            index =0 
            die_roll = rnd.random()
            while neighbor_cdf[index]<die_roll:
                index += 1
            # scan over until you find the one corresponding to this die roll

            target_id = main_map.get_hex_neighbors( ids_to_propagate[0] )[index]
            place = main_map.get_point_from_id( target_id )
            if not point_is_in(place, dimensions):
                ids_to_propagate.pop(0)
                continue
            
            new_hex = make_basic_hex( place , main_map._drawscale)
            new_hex.genkey = '11000000'
            new_hex.fill = (99,88,60)
            
            try:
                main_map.register_hex( new_hex, target_id)
                ids_to_propagate.append( target_id)
                ids_to_propagate.pop(0)
                continue 
            except NameError:
                # let's try this again... 
                continue

          

    if not os.path.isdir("../saves"):
        os.mkdir("../saves")

    save_map( main_map, sim )

if __name__=='__main__':
    generate('cont')

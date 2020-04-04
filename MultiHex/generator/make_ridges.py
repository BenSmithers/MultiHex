from MultiHex.core import Point, Hexmap, save_map, load_map
from MultiHex.map_types.overland import *
from MultiHex.generator.util import *

from numpy import arccos 
from numpy import histogram
from math import exp, floor, sqrt, e, pi

import random as rnd
import os
import json

def make_basic_hex(arg1, arg2):
    new_one = OHex(arg1, arg2)
    new_one._biodiversity = 0.0
    new_one._rainfall_base = 0.0
    new_one._temperature_base = 0.0
    return( new_one )


def generate(size, sim = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap')):

    # load the config file
    file_object = open( os.path.join(os.path.dirname(__file__), 'config.json'), 'r' )
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
    main_map.dimensions = ( dimensions[0], dimensions[1] )

    #                Generate Mountain Peaks 
    # ======================================================


    ids_to_propagate = []

    def make_continent():
        ids_to_propagate = []
        x_center = 0.80*rnd.random()*dimensions[0] + 0.10*dimensions[0]
        y_cos  = 1.8*rnd.random() - 0.9
        y_center = arccos( y_cos )*dimensions[1]/( pi )
        print("Making New Continent at ({:.2f},{:.2f})".format(x_center, y_center))
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
                    new_hex = None
                    break
                except NameError:
                        continue

        direction = 360*rnd.random()
        sigma       = config['sigma']
        avg_range   = config['avg_range']


        # build the neighbor function
        distribution = get_distribution( direction, sigma)
        print("    Ridgeline Direction: {} +/- {}".format(direction, sigma))
        print("    Ridgline Avg Length: {}".format(avg_range))

        angles = [150., 90., 30., 330., 270., 210.]
        neighbor_weights = [ distribution( angle ) for angle in angles]

        # calculate CDF of neighbor weights 
        neighbor_cdf = [0. for weight in neighbor_weights]
        for index in range(len(neighbor_weights)):
            if index == 0:
                neighbor_cdf[0] = neighbor_weights[0]
            else:
                neighbor_cdf[index] = neighbor_cdf[index - 1] + neighbor_weights[index]

        while len(ids_to_propagate)!=0:
            if rnd.random()>(1.-(1./avg_range)):
                #terminate this ridgeline
                ids_to_propagate.pop()
                continue
            else:
                index = 0 
                die_roll = rnd.random()
                while neighbor_cdf[index]<die_roll:
                    index += 1
                # scan over until you find the one corresponding to this die roll

                target_ids = main_map.get_hex_neighbors( ids_to_propagate[-1] )
                target_id = target_ids[index]

                place = main_map.get_point_from_id( target_id )
                if not point_is_in(place, dimensions):
                    ids_to_propagate.pop(0)
                    continue
            
                new_hex = make_basic_hex( place , main_map._drawscale)
                new_hex.genkey = '11000000'
                new_hex.fill = (99,88,60)
            

                try:
                    main_map.register_hex( new_hex, target_id)
                    ids_to_propagate.pop()
                    ids_to_propagate.append( target_id )
                    new_hex = None
                    continue 
                except NameError:
                    # let's try this again... 
                    continue


    if size=='cont':
        for i in range(zones):
            make_continent()
    else:
        raise NotImplementedError()

    # choose a direction the ridgeline will preferably go, and spread around that direction




    
            

          

    if not os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'saves')):
        os.mkdir(os.path.join( os.path.dirname(__file__), '..','saves'))

    save_map( main_map, sim )

if __name__=='__main__':
    generate('cont')

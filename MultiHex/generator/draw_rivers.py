from MultiHex.core import Path, Hex
from MultiHex.map_types.overland import *
from MultiHex.generator.util import *

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
        config = config[size]['rivers']
    
    n_rivers = config["n_rivers"]
    max_len  = config["max_len"]


    main_map = load_map( sim )

    def make_river():
        # choose start point - mountain or ridge!
        while True:
            # choose a mountain or ridge to start this river 
            # which = int( rnd.random()*len(main_map.catalogue.keys()) )
            # this_hex = main_map.catalogue[ list(main_map.catalogue.keys())[which] ]
            place = Point( rnd.random()*dimensions[0], rnd.random()*dimensions[1])
            loc_id = main_map.get_id_from_point( place )
            try:
                this_hex = main_map.catalogue[ loc_id ]
            except KeyError:
                continue

            this_center = main_map.get_point_from_id( loc_id )

            if not(this_hex.genkey[0]=='1' or this_hex.genkey[1]=='1'):
                # not a mountain
                continue 
            start_point = int( rnd.random()*6 )

            
            new_river = River(Point( this_hex.vertices[start_point].x, this_hex.vertices[start_point].y) )
            if (start_point)%2==0:
                v_type = 2
            else:
                v_type = 1

#                v_type = int( ((start_point + 1)% 2) + 1 )

            break
        # river has now started! 
        while True:
            if len(new_river.vertices)>new_river._max_len:
                break

            loc_id = None
            this_hex = None
            if v_type==1 or v_type==2:
                # get the neighbors immediately around the vertex
                im_neighbors = main_map.get_ids_around_vertex( new_river.end(), v_type )

                # check if one of these is an ocean or the end of the map, if so, stop! 
                coastal = False
                for each in im_neighbors:
                    try:
                        coastal = not main_map.catalogue[ each ]._is_land
                    except KeyError:
                        coastal = True # edge of map, let's just end this

                if coastal: # river has reached ocean! 
                    break

                # we have six possible directions:
                #   + to a hex center 
                #   + to another vertex
                
                # get the weights for going to a center
                dir_weights = [ 0.0 for i in range(3) ]

                
                # get the weights for going to another vertex 
                verts = main_map.get_vertices_beside( new_river.end(), v_type )
                for it in range(3):
                    # for each of the possible vertices, get its surrounding IDs
                    if v_type==1:
                        these_hexes = main_map.get_ids_around_vertex( verts[it], 2)
                    else:
                        these_hexes = main_map.get_ids_around_vertex( verts[it], 1)
                    
                    # add to the weight/altitude
                    for ID in these_hexes:
                        try:
                            # adding 3 so we skip the 'center' ones
                            dir_weights[it] = dir_weights[it] + main_map.catalogue[ID]._altitude_base
                        except KeyError:
                            pass
                    # divide by 3 to get the average 
                    dir_weights[it] = dir_weights[it]/3. 
                
                which_index = dir_weights.index( min(dir_weights) )
                if v_type==1:
                    v_type = 2
                else:
                    v_type = 1
                new_river.add_to_end( verts[which_index] )


            else:
                raise ValueError("Unexpected vertex type found? {} of type {}".format(v_type, type(v_type)))
        return( new_river )

    main_map.paths['rivers'] = []
    for i in range( n_rivers ):
        this_riv = make_river()
        main_map.paths['rivers'].append( this_riv )

    save_map( main_map, sim )
    

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

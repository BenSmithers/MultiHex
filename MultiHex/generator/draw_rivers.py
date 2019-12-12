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
            new_river._max_len = max_len 
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

                # set river border types
                cw_id, ccw_id = main_map.get_ids_beside_edge( new_river.end(), verts[which_index])
                try:
                    main_map.catalogue[cw_id].river_border[0] = True
                except KeyError:
                    pass
                try:
                    main_map.catalogue[ccw_id].river_border[1] = True
                except KeyError:
                    pass

                # check if this new point is already on the river, if it is, we realized we have completed a loop. Snip the river and make some lakes  
                if verts[which_index] in new_river.vertices:
                    
                    all_verts = new_river.vertices 
                    which = all_verts.index( verts[which_index] )
                    
                    for it in range(len(all_verts[which:])):
                        ids = main_map.get_ids_beside_edge( all_verts[which+it-1], all_verts[which+it] )
                        for ID in ids:
                            main_map.catalogue[ID].fill = colors.ocean
                            main_map.catalogue[ID]._altitude_base = 0.0
                            main_map.catalogue[ID]._is_land = False
    
                    new_river.trim_at( which )
                    break
                

                new_river.add_to_end( verts[which_index] )

                # check if we're now at a border and on another river

                # right side, left side 
                cw, ccw = main_map.get_ids_beside_edge( new_river.end(1), new_river.end() )
                
                if (cw not in main_map.catalogue) or (ccw not in main_map.catalogue):
                    continue 

                # both the hexes to my left and right are on the same side of a river 
                
                if (main_map.catalogue[ccw].river_border[0] and  main_map.catalogue[cw].river_border[0]) or (main_map.catalogue[ccw].river_border[1] and main_map.catalogue[cw].river_border[1]):
                    # this means that the river has now reached another river 

                    # search through the other rivers, find the one with my end on it
                    # fortunately, this river hasn't been registered yet
                    error_code = 1 
                    for river in range(len(main_map.paths['rivers'])):
                        # recursively tries to join rivers with their tributaries 
                        error_code = main_map.paths['rivers'][river].join_with( new_river )
                        if error_code == 0:
                            break
                        # if it's 1, continue 
                    if error_code == 0:
                        return(None)
                    # if error_code = 1, there was no merge 

            else:
                raise ValueError("Unexpected vertex type found? {} of type {}".format(v_type, type(v_type)))
        if len(new_river.vertices)!=0:
            return( new_river )
        else:
            return( None )

    main_map.paths['rivers'] = []
    print("Making Rivers",end='')
    for i in range( n_rivers ):
        if i%3==0:
            print('.',end='')
        this_riv = make_river()
        if this_riv is not None:
            main_map.paths['rivers'].append( this_riv )

    save_map( main_map, sim )
    print(" done!")

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

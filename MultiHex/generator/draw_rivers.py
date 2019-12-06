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
        config = config[size]['regions']



    main_map = load_map( sim )

    def make_river():
        # choose start point - mountain or ridge!
        while True:
            # choose a mountain or ridge to start this river 
            which = int( rnd.random()*len(main_map.catalogue.keys()) )
            this_hex = main_map.catalogue[ main_map.catalogue.keys()[which] ]
            if not(this_hex.genkey[0]=='1' or this_hex.genkey[1]=='1'):
                # not a mountain
                continue 
            start_point = int( rnd.random*7 )

            
            v_type = 0
            if start_point == 0:
                new_river = River( this_hex._center )
                v_type = 0
            else:
                new_river = River( this_hex._vertices[start_point] )
                v_type = int( ((start_point + 1)% 2) + 1 )

            break
        
        # river has now started! 
        while True
            if v_type == 0:
                loc_id = main_map.get_id_from_point( self.end() )
                try:
                    this_hex = main_map.catalogue[ loc_id ]
                except KeyError:
                    break # river exited map! 
                
                # list of neighbors 
                neighbors = main_map.get_hex_neighors( loc_id )
                
                # calculate average altitudes around possible subsequent river directions
                which_neighbors = []
                dir_weights = [0.0 for i in range(6)]
                for it in range( 6 ):
                    try:
                        weight = main_map.catalogue[ neighbors[it] ]._altitude_base + main_map.catalogue[neighbors[ (it+1)%6 ]]._altitude_base
                        weight *= 0.5
                    except KeyError:
                        weight = this_hex._altitude_base 

                    dir_weights[it] = weight 
                
                # chose the direction to go based on which direction is the lowest in altitude 
                which_index = dir_weights.index(min(dir_weights))
                # update the vertex type int to reflect where we are now 
                if which_index%2==0:
                    v_type=2 
                else:
                    v_type=1
                self.add_to_end( this_hex._vertices[ which_index ] )
            elif v_type==1 or v_type==2:
                im_neighbors = main_map.get_ids_around_vertex( self.end() )
                coastal = False
                for each in im_neighbors:
                    try:
                        coastal = not main_map.catalogue[ each ]._is_land
                    except KeyError:
                        coastal = True # edge of map, let's just end this

                if coastal: # river has reached ocean! 
                    break
            
            else:
                raise ValueError("Unexpected vertex type found? {} of type {}".format(v_type, type(v_type)))




    save_map( main_map, sim )
    

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

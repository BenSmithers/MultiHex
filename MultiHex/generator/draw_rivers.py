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
    
    def set_banks( river ):
        vertices = river.vertices

        for counter in range(len( vertices) - 1):
            # get the ids beside a segment of the river
            cw_id, ccw_id = main_map.get_ids_beside_edge( vertices[counter], vertices[counter + 1])

            # set those hexes to river borders 
            try:
                main_map.catalogue[cw_id].river_border[0] = True
                main_map.catalogue[cw_id]._rainfall_base = min([ 1.0, main_map.catalogue[cw_id]._rainfall_base*1.1] )
            except KeyError:
                pass
            try:
                main_map.catalogue[ccw_id].river_border[1] = True
                main_map.catalogue[ccw_id]._rainfall_base = min( [1.0, main_map.catalogue[ccw_id]._rainfall_base*1.1 ])
            except KeyError:
                pass

        # now we need to call this on the tributaries of this river (yay recursion!) 
        if river.tributaries is not None:
            set_banks( river.tributaries[0] )
            set_banks( river.tributaries[1] )


    def point_hits_source( point, river ):
        """
        returns a bool specifying whether or not the object 'point' is the source of the river 
        """

        assert( isinstance( point, Point))
        assert( isinstance( river, River))

        if river.tributaries is not None:
            return( point==river.start() or point_hits_source(point, river.tributaries[0]) or point_hits_source(point, river.tributaries[1] ))
        else:
            return( point==river.start() )
    
    def point_on_river( point, river ):
        """
        returns whether or not the Point `point` is somewhere on the River object `river`

        @param point    - the Point...
        @param river    - the River... 
        """

        assert( isinstance( point, Point))
        assert( isinstance( river, River))

        if river.tributaries is not None:
            # see if the point is on the river body, or one of the tributaries. Call this function on each of the tributaries 
            return( (point in river.vertices) or (point_on_river( point, river.tributaries[0])) or (point_on_river( point, river.tributaries[1] )))
        else:

            return( point in river.vertices )
        

    def make_river():
        # choose start point - mountain or ridge!
        while True:
            # choose a mountain or ridge to start this river 
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

            # set the vertex type, this is used for stepping the river along. 
            if (start_point)%2==0:
                v_type = 2
            else:
                v_type = 1
            
            # need to make sure this isn't on another river
            try_again = False
            for pID in main_map.path_catalog['rivers']:
                # recursively check a river and its vertices... this is super expensive, so we wait until the very end
                if point_on_river( this_hex.vertices[start_point] , main_map.path_catalog['rivers'][pID] ):
                    try_again = True
                    break
            # if it is, let's try again
            if try_again:
                continue

            break

        # river has now started! 
        while True:
            if len(new_river.vertices)>new_river._max_len:
                break

            if v_type==1 or v_type==2:
                #                   Get Surrounding Tiles. Check for Ocean
                # ========================================================================

                # get the neighbors immediately around the vertex
                im_neighbors = main_map.get_ids_around_vertex( new_river.end(), v_type )

                # check if one of the hexes immediately beside the river end is an ocean or the end of the map, if so, stop! 
                coastal = False
                for each in im_neighbors:
                    try:
                        coastal = not main_map.catalogue[ each ]._is_land
                        if coastal:
                            break
                    except KeyError:
                        coastal = True # edge of map, let's just end this
                        break

                if coastal: # river has reached ocean! 
                    break

                #               Look at surrounding tiles. Decide Direction
                # ========================================================================

                                
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
               

                #                   Check if hiting START of other river
                # ========================================================================

                
                # before setting the river border bools, we should see if we're about to hit the end of another river...
                bad = False
                for pID in main_map.path_catalog['rivers']:
                    # check if the new point is the source of this river 
                    if point_hits_source( verts[which_index], main_map.path_catalog['rivers'][pID] ):
                        bad = True
                        break
                if bad:
                    # if it did, we just give up on this river. 
                    return(None) 


                
                #                    Check if river loops back on self
                # ========================================================================

                # check if this new point is already on the river, if it is, we realized we have completed a loop. Snip the river and make some lakes  
                if verts[which_index] in new_river.vertices:
                    odds = rnd.random()


                    all_verts = new_river.vertices 
                    which = all_verts.index( verts[which_index] )
                    
                    # total length is len(all_verts)
                    # we just want the ones after 'which',
                    if odds>0.75:
                        # make a lake
                        for it in range(len(all_verts) - which):
                            ids = main_map.get_ids_beside_edge( all_verts[which+it-1], all_verts[which+it] )
                            for ID in ids:
                                main_map.catalogue[ID].fill = colors.ocean
                                main_map.catalogue[ID]._altitude_base = 0.0
                                main_map.catalogue[ID]._is_land = False
                                main_map.catalogue[ID].biome = "lake"
                                main_map.catalogue[ID].river_border = [False, False, False]
        
                        new_river.trim_at( which-1, True )
                        break
                    else:
                        for it in range(len(all_verts)-which):
                            ids = main_map.get_ids_beside_edge( all_verts[which+it-1], all_verts[which+it])
                            for ID in ids:
                                main_map.catalogue[ID]._altitude_base = min( [1.0, 1.2*main_map.catalogue[ID]._altitude_base])
                                main_map.catalogue[ID].river_border = [False, False, False]
                                
                                neighbors = main_map.get_hex_neighbors( ID )
                                for neighbor in neighbors:
                                    main_map.catalogue[neighbor]._altitude_base = min([ 1.0, 1.1*main_map.catalogue[neighbor]._altitude_base])
                                    main_map.catalogue[neighbor].river_border = [False, False, False]
                        return( None )

                                    

                #                    Append Point to River, Vertex Type
                # ========================================================================


                new_river.add_to_end( verts[which_index] )
                # update the vertex type
                if v_type==1:
                    v_type = 2
                else:
                    v_type = 1

                
                #                   Check for other River Collisions
                # ========================================================================

                # formerly used the river bools to avoid doing this unnecessarily, but that lead to issues with rivers not merging properly...

                # search through the other rivers, find the one with my end on it
                # fortunately, this river hasn't been registered yet
                error_code = 1 
                for pID in main_map.path_catalog['rivers']:
                    # recursively tries to join rivers with their tributaries 
                    # Codes:
                    #   0 - merged
                    #   1 - couldn't merge 
                    
                    error_code = main_map.path_catalog['rivers'][pID].join_with( new_river )
                    if error_code == 0:
                        break
                    # if it's 1, continue 
                if error_code == 0:
                    return(None)
                # if error_code = 1, there was no merge 

            else:
                raise ValueError("Unexpected vertex type found? {} of type {}".format(v_type, type(v_type)))
        if (len(new_river.vertices)!=0) or (new_river.tributaries is not None):
            return( new_river )
        else:
            return( None )

    print("Making Rivers",end='')
    main_map.path_catalog['rivers'] = {}
    
    counter = 0
    while len(main_map.path_catalog['rivers'].keys())<n_rivers:
        if counter%3==0:
            print('.',end='')
        this_riv = make_river()
        if this_riv is not None:
            set_banks( this_riv )
            main_map.register_new_path( this_riv , 'rivers')
            counter += 1

    save_map( main_map, sim )
    print(" done!")

if __name__=='__main__':
    if len(sys.argv)>1:
        generate( 'cont', sys.argv[1])
    else:
        generate('cont')

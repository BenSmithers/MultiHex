from MultiHex.core import Point, Hexmap, save_map, load_map
from MultiHex.map_types.overland import *
from MultiHex.generator.util import *
from MultiHex.generator.noise import perlinize

from numpy import arccos, histogram, linspace
from math import exp, floor, sqrt, e, pi, sin

import random as rnd
import os
import json
import sys

from collections import deque

"""
Runs a toy weather model to get a rainfall map of the world

Ues basic geometry for a spherical planet to determine relative sunlight exposure, and stores that as the hexes' temperature_base criteria.
"""

def generate(size, sim = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap')):
    # load the config file
    file_object = open( os.path.join(os.path.dirname(__file__), 'config.json'), 'r' )
    config  = json.load( file_object )
    file_object.close()

    # check to make sure it uses a supported preset 
    if not (size in config):
        raise Exception("Unsupported size: {}".format(size) )
    else:
        dimensions = [config[size]['mountains']['values']['dimx'], config[size]['mountains']['values']['dimy']]
        config = config[size]['weather']['values']

    diffusion       = config['diffusion']
    pres_weight     = config['pres_weight']
    rain_rate       = config['rain_rate']
    reservoir_init  = config['reservoir_init']
    resr_weight     = config['resr_weight']
    plotting        = False
    
    main_map = load_map( sim )

    #                Establish Rainfall
    # ======================================================

    print("Simulating Weather")

    rthree = sqrt(3)
    if size=='cont':
        n_cloud_units = int(    dimensions[1] / (main_map._drawscale*rthree) )
    else:
        n_cloud_units = int( 2.*dimensions[1] / ( main_map._drawscale*rthree) )

    x_step          = 0.2*main_map._drawscale
    evap_rate       = 10.*rain_rate*e

    def get_rate( reservoir , pressure ):
        """
        
        @ param pressure - (0,1)
        @ param reservoir - (0 , infty)
        """
        # pressure is like an approaching mountain, 
        # reservoir is how much water is in the clouds

        if reservoir<5:
            return(0.0)

        rate = rain_rate * exp(pres_weight*pressure)*exp(resr_weight*reservoir/reservoir_init)
        return( rate )

    def index_to_y( index, eastern=False ):
        if size=='cont': 
            if eastern:
                return( 0.5*dimensions[0] + 1.05*index*main_map._drawscale*rthree + 0.42*main_map._drawscale)
            else:
                return( 1.05*index*main_map._drawscale*rthree + 0.42*main_map._drawscale )
        else:
            return( index*main_map._drawscale*rthree/2. + 0.42*main_map._drawscale )



    # create cloud object. Reser
    clouds = [ [reservoir_init, 0.0] for i in range( n_cloud_units ) ]
    if size=='cont':
        clouds_east = [ [reservoir_init, dimensions[0]] for i in range( n_cloud_units ) ]


    def step():
        # just so it knows we're modifying this thing! 
      #  global clouds 
        #if size=='cont':
        #    global clouds_east
       # global main_map

        # copy the clouds object 
        new_cloud = [ [clouds[i][0], clouds[i][1]] for i in range(len( clouds )) ]
        if size=='cont':
            new_cloud_east = [ [clouds_east[i][0], clouds_east[i][1]] for i in range(len( clouds_east )) ]


        for index in range(len(clouds)):
            here_id  = main_map.get_id_from_point( Point( clouds[index][1], index_to_y(index)))
            neigh_id = main_map.get_id_from_point( Point( clouds[index][1]+2.7*main_map._drawscale, index_to_y(index)))
            
            pressure = 0.0
            try:
                here = main_map.catalog[here_id]
                skip_some = False
            except KeyError:
                skip_some = True

            if not skip_some:
                # get the pressure factor 
                try:
                    neigh = main_map.catalog[neigh_id]
                    pressure = neigh._altitude_base - here._altitude_base 
                except KeyError:
                    pressure = 0.0

                if pressure < 0.0:
                    pressure = 0.0

                rain = get_rate( clouds[index][0], pressure)*x_step
                if not here._is_land:
                    new_cloud[index][0] += evap_rate
                
                # drop rain from the reservoir into the thing beneath it
                new_cloud[index][0] -= rain
                main_map.catalog[here_id]._rainfall_base += rain

            # diffuse
            if index!=(len(clouds)-1):
                diff = new_cloud[index+1][0] - new_cloud[index][0]
                new_cloud[index][0]   += diff*diffusion
                new_cloud[index+1][0] -= diff*diffusion
           
            # cloud moves forward
            new_cloud[index][1] += (1.0-pressure)*x_step
            
            if size=='cont':
                here_id  = main_map.get_id_from_point( Point( clouds_east[index][1], index_to_y(index, True)))
                neigh_id = main_map.get_id_from_point( Point( clouds_east[index][1]-2.7*main_map._drawscale, index_to_y(index, True)))
                
                pressure = 0.0
                try:
                    here = main_map.catalog[here_id]
                    skip_some = False
                except KeyError:
                    skip_some = True

                if not skip_some:
                    # get the pressure factor 
                    try:
                        neigh = main_map.catalog[neigh_id]
                        pressure = neigh._altitude_base - here._altitude_base 
                    except KeyError:
                        pressure = 0.0

                    if pressure < 0.0:
                        pressure = 0.0

                    rain = get_rate( clouds_east[index][0], pressure)*x_step
                    if not here._is_land:
                        new_cloud_east[index][0] += evap_rate
                    
                    # drop rain from the reservoir into the thing beneath it
                    new_cloud_east[index][0] -= rain
                    main_map.catalog[here_id]._rainfall_base += rain

                # diffuse
                if index!=(len(clouds_east)-1):
                    diff = new_cloud_east[index+1][0] - new_cloud_east[index][0]
                    new_cloud_east[index][0]   += diff*diffusion
                    new_cloud_east[index+1][0] -= diff*diffusion
               
                # cloud moves forward
                new_cloud_east[index][1] -= (1.0-pressure)*x_step

        for index in range(len(clouds)):
            clouds[index] = [new_cloud[index][0], new_cloud[index][1]]
            if size=='cont':
                clouds_east[index] = [new_cloud_east[index][0], new_cloud_east[index][1]]

    # maintain a %complete notice in the CLI while stepping the clouds forward
    percentages = [False for i in range(9)] 

    # keep going until the farthest back cloud traverses the world
    while( min( [ i[1] for i in clouds] )<= dimensions[0] or (size=='cont' and min([i[1] for i in clouds_east])>=0) ):
        perc = int( 100.*clouds[0][1]/dimensions[0] )
        
        for test in range(len(percentages)):
            if percentages[test]:
                continue
            else:
                if perc > (test+1)*10:
                    print("{}% done".format((1.+test)*10.))
                    percentages[test] = True

        # step the cloud forward
        step()


    #               Calculate Rainfal Statistics
    # ======================================================

    

    rains = deque([])

    # set rainy thing
    for ID in main_map.catalog.keys():
        
        # we're not collecting statistics on the ocean. It's all very rainy
        this_hex = main_map.catalog[ID]
        if not this_hex._is_land:
            continue
       
        rains.append( main_map.catalog[ID]._rainfall_base )

    
    # do some statistics with fiiine bins
    summ = len(rains)
    weights = [ 1./summ for i in rains]
    from numpy import linspace
    bins = list( linspace(0,1,100, endpoint=False)) + list( linspace(1,10,100))
    occupation, edges = histogram( rains, normed=False, bins=bins, weights = weights)
    del summ
    del weights

    percentiles = [oc for oc in occupation]
    for i in range(len(occupation)):
        if i==0:
            percentiles[i]=occupation[i]
        else:
            percentiles[i]=occupation[i]+percentiles[i-1]
    
    # the hex _rainfall_base is is 1/100 the rainfall percentile 
    for ID in main_map.catalog.keys():
        this_hex = main_map.catalog[ID]

        # don't set the rainfall in the ocean
        if not this_hex._is_land:
            continue

        which = 0
        while this_hex._rainfall_base > edges[which]:
            which+=1
            if which==len(edges):
                break

        if which==len(edges):
            main_map.catalog[ID]._rainfall_base = 1.0
        elif which==0:
            # somehow this is beneath the binned region. Should be impossible
            main_map.catalog[ID]._rainfall_base = 0.0
        else: 
            which -= 1
            try:        
                main_map.catalog[ID]._rainfall_base = percentiles[which]
            except IndexError:
                print( "ID: {}".format(ID))
                print( "which: {} of {}".format(which, len(percentiles)))
                sys.exit()        

    print("Applying Sunlight Gradient")
    for ID in main_map.catalog:
        point_y = main_map.catalog[ID]._center.y
        # sine arg goes from 0->pi
        # so the temperature goes from 0->1
        
        # 0 at arg=0 or pi, 1 at pi/2
        temperature = sin( (pi*point_y/dimensions[1]) )
        main_map.catalog[ID]._temperature_base = temperature 

    
    save_map( main_map, sim )

    n_rounds = 2
    print("Performing {} round of Rainfall Smoothing".format(n_rounds))
    for i in range(n_rounds):
        smooth(['rain'], sim)

    perlinize(attr='_temperature_base')


    

if __name__=='__main__':
    generate('cont')

from point import Point
from hex import Hex
from hexmap import Hexmap, save_map, load_map
from special_hexes import *

from math import exp, floor, sqrt, e

import os
import sys

import time
import random as rnd 

def make_basic_hex(arg1, arg2):
    new_one = Hex(arg1, arg2)
    new_one._biodiversity = 0.0
    new_one._rainfall_base = 0.0
    new_one._temperature_base = 0.0
    return( new_one )

plotting        = False ### warning!! Slow!!
do_weather = True
size = 'cont'
out_file = './saves/generated.hexmap'

if size=='small':
    dimensions = [1920, 1080]
    n_peaks = 15
elif size=='large':
    dimensions = [3840, 2160]
    n_peaks = 25
elif size=='cont':
    dimensions = [6000, 3000]
    zones = 4
    n_peaks = 9
else:
    raise Exception("'{}' size not implemented".format(size))

main_map = Hexmap()

#                Generate Mountain Peaks 
# ======================================================
print("Seeding Mountain Peaks")

distribution_mean   = 0.65*dimensions[0]
distribution_width  = 0.20*dimensions[0]
print("    Y-Centered at {} +/- {}".format( distribution_mean, distribution_width))
print("    Uniform Y Distribution")

ids_to_propagate = []


# check if point is in the map
def point_is_in(point):
    return( point.x < dimensions[0] and point.x > 0 and point.y < dimensions[1] and point.y>0)

if size=='small' or size=='large':
    for i in range( n_peaks ):
        while True:
            place = Point( rnd.gauss(distribution_mean, distribution_width), rnd.random()*dimensions[1] )
            if not point_is_in( place ):
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
        x_center = 0.60*rnd.random()*dimensions[0] + 0.18*dimensions[0]
        y_center = 0.60*rnd.random()*dimensions[1] + 0.18*dimensions[1]
        for j in range(n_peaks):
            while True:
                place = Point( rnd.gauss( x_center, 300), rnd.gauss( y_center, 300) )
                if not point_is_in(place):
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

#                  Prepare Utilities
# =====================================================


# calculate the difference between two angles... sorta 
# returned angle is always less than 180 degrees
def angle_difference( theta_1, theta_2 ):
    if not (theta_1 > 0 and theta_1<360):
        raise Exception("bad angle {}".format(theta_1))
    if not (theta_2 > 0 and theta_2<360):
        raise Exception("bad angle {}".format(theta_2))
    
    # return minimum of distance between theta_2 and theta2+180
    theta_2_rotate = (theta_2 + 180.) % 360.
    
    distance1 = 0
    distance2 = 0

    phi = abs( theta_1 - theta_2) % 360.
    if phi>180.:
        distance1 = 360.-phi
    else:
        distance1 = phi
    phi = abs(theta_1 - theta_2_rotate)
    if phi>180.:
        distance2 = 360.-phi
    else:
        distance2 = phi

    return(distance1)


# prepares a discrete distribution so that 
#   mountains are preferentially made in a certain direction

# neighbors  = [ 90, 270, 30, 330, 150, 210 ]
def get_distribution( direction, variance=20. ):
    normalization = 0
#    variance = 20.
    angles = [ 90, -90, 30, -30, 150, -150 ]

    # calculate normalization
    for angle in angles:
        normalization += exp( -1.*(angle_difference(angle+180., direction)**2)/(2*variance**2))

    def distribution(angle): 
        return( (1./normalization)*exp(-1*(angle_difference(angle+180., direction)**2)/(2*variance**2)))

    return( distribution )


#                  Create ridgelines 
# =====================================================
print("Forking Ridglines")

# choose a direction the ridgeline will preferably go, and spread around that direction
direction = 360*rnd.random()

if size=='cont':
    sigma = 60
    avg_range = 15.
else:
    sigma = 60
    avg_range = 30.

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
        if not point_is_in(place):
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


#         Add mountainous terrain around Ridgelines
# ======================================================
print("Spreading Mountains")

# recalculate the weighting function

ids_to_propagate = list( main_map.catalogue.keys())

# average thickness of the mountains
mnt_thicc = 2.3

print("    average mountain thickness {}".format( mnt_thicc ))

while len(ids_to_propagate) != 0:
    
    parent = main_map.catalogue[ids_to_propagate[0]]
    
    if parent.genkey[0]=='1':
        perc = 0. 
    else:
        perc = 1.0/mnt_thicc

    if rnd.random() > (1. - perc):
        ids_to_propagate.pop(0)
    else:
        # equal probability of spreead
        neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )
        
        sanitized_neighbors = []
        for index in range(len(neighbors)):
            if neighbors[index] not in main_map.catalogue:
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

            if not point_is_in(center):
                ids_to_propagate.pop(0)
                continue

            new_hex = Mountain_Hex( center, main_map._drawscale)
            new_hex.genkey = '01000000'
            
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


#               Smooth Drop to Ocean level
# ======================================================
print("Spread Land Out")

if size=='cont':
    land_spread  = 0.060
    land_width   = 0.03
    water_spread = 0.02
    water_width  = 0.01
else:
    land_spread  = 0.03
    land_width   = 0.015
    water_spread = 0.10
    water_width  = 0.05


print("    Land Spread Factor  {} +/- {}".format(land_spread, land_width))
print("    Ocean Spread Factor {} +/- {}".format(water_spread, water_width))

ids_to_propagate = list( main_map.catalogue.keys())

while len(ids_to_propagate)!=0:
    parent = main_map.catalogue[ids_to_propagate[0]]
    if parent.genkey[0]=='1': # can pretty much guarantee these aren't exposed
        ids_to_propagate.pop(0)
        continue
    else:
        neighbors = main_map.get_hex_neighbors( ids_to_propagate[0] )

        sanitized_neighbors = []
        for neighbor in neighbors:
            if neighbor not in main_map.catalogue:
                sanitized_neighbors.append( neighbor )
        
        if len(sanitized_neighbors)==0:
            ids_to_propagate.pop(0)
            continue
        else:
            # okay, so now we need to create the neighbors... 
            for neighbor in sanitized_neighbors:
                center = main_map.get_point_from_id( neighbor )
                if not point_is_in(center):
                    continue

                if parent._is_land:
                    new_alt = parent._altitude_base - rnd.gauss(land_spread, land_width)
                else:
                    new_alt = parent._altitude_base - rnd.gauss(water_spread, water_width)

                if new_alt > 0:
                    new_hex = Grassland_Hex( center,main_map._drawscale )
                    new_hex._is_land = True
                else:
                    new_hex = Ocean_Hex( center, main_map._drawscale)
                    new_hex._is_land = False

                new_hex._altitude_base = new_alt 
                main_map.register_hex( new_hex, neighbor )
                ids_to_propagate.append( neighbor )
            ids_to_propagate.pop(0)

#                   Do Some Smoothing 
# ======================================================
n_rounds = 2

print("Performing {} rounds of smoothing".format(n_rounds))

# this is used to get some land color based off of the altitude of the point and also whether or not it's land
def new_color(is_land, altitude):
    """
    generalize this for a any hex
    """

    deep_ocean = ( 8,   32,  59)
    shallows   = (100, 173, 209)

    high_lands = (181, 179, 132)
    low_lands  = (119, 163,  57)
    
    if is_land:
        if altitude >1:
            altitude=1.
        elif altitude<0:
            altitude = 0
        return( ( (high_lands[0]-low_lands[0])*altitude + low_lands[0] ,    
                    (high_lands[1]-low_lands[1])*altitude + low_lands[1], 
                    (high_lands[2]-low_lands[2])*altitude + low_lands[2]) )
    else:
        if altitude < -2:
            altitude = -2.
        elif altitude > 0:
            altitude = 0
        return( ( -1*(deep_ocean[0] - shallows[0])*altitude*0.5 + shallows[0] ,
                     -1*(deep_ocean[1] - shallows[1])*altitude*0.5 + shallows[1] ,
                    -1*(deep_ocean[2] - shallows[2])*altitude*0.5 + shallows[2] ) )

def smooth(what = ['alt'] ):
    print("    smoothing... ")
    global main_map

    for ID in main_map.catalogue.keys():
        neighbors = main_map.get_hex_neighbors( ID )

        this_one = main_map.catalogue[ID]
        # skip mountains 
        if this_one.genkey[1]=='1':
            continue
        
        if 'alt' in what:
            existing = 1
            total    = this_one._altitude_base
            for neighbor in neighbors:
                if neighbor in main_map.catalogue:
                    existing += 1
                    total    += main_map.catalogue[neighbor]._altitude_base 
            
            # make this altitude the average of it and its neighbors (which exist)
            main_map.catalogue[ID]._altitude_base = total / float(existing)


        # this may have made ocean become land and land become ocean... 
        if main_map.catalogue[ID]._altitude_base < 0.:
            main_map.catalogue[ID]._is_land = False
            main_map.catalogue[ID].fill = new_color( False, total / float(existing))
        else:
            main_map.catalogue[ID]._is_land = True
            main_map.catalogue[ID].fill = new_color( True, total/float(existing))

for i in range( n_rounds ):
    smooth()

#                Establish Rainfall
# ======================================================

if do_weather:

    print("Simulating Weather")

    rthree = sqrt(3)

    n_cloud_units = int( 2.*dimensions[1] / ( main_map._drawscale*rthree) )

    x_step          = 0.2*main_map._drawscale
    rain_rate       = 0.005
    evap_rate       = rain_rate*e
    diffusion       = 0.03


    if size=='large':
        reservoir_init  = 140.
    elif size=='small':
        reservoir_init  = 70.
    elif size=='cont':
        reservoir_init  = 45.
    else:
        reservoir_init  = 10. 
        print("invalid size??")


    def get_rate( reservoir , pressure ):
        """
        
        @ param pressure - (0,1)
        @ param reservoir - (0 , infty)
        """
        # pressure is like an approaching mountain, 
        # reservoir is how much water is in the clouds
        global rain_rate

        if reservoir<5:
            return(0.0)

        rate = rain_rate * exp(pressure)*exp(reservoir/reservoir_init)
        return( rate )

    def index_to_y( index ):
        return( index*main_map._drawscale*rthree/2. + 0.5*main_map._drawscale )

    # create cloud object. Reser
    clouds = [ [reservoir_init, 0.0] for i in range( n_cloud_units ) ]

    if plotting:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        plt.figure(1)
        plt.xlim([0, dimensions[0]])
        plt.ylim([0, dimensions[1]])
        plt.ion()
        plt.show()

        plt.figure(2)
        plt.ion()
        plt.show()

    def step():
        # just so it knows we're modifying this thing! 
        global clouds 
        global main_map

        # copy the clouds object 
        new_cloud = [ [clouds[i][0], clouds[i][1]] for i in range(len( clouds )) ]
        
        for index in range(len(clouds)):
            here_id  = main_map.get_id_from_point( Point( clouds[index][1], index_to_y(index)))
            neigh_id = main_map.get_id_from_point( Point( clouds[index][1]+2.7*main_map._drawscale, index_to_y(index)))
            
            pressure = 0.0
            try:
                here = main_map.catalogue[here_id]
                skip_some = False
            except KeyError:
                skip_some = True

            if not skip_some:
                # get the pressure factor 
                try:
                    neigh = main_map.catalogue[neigh_id]
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
                main_map.catalogue[here_id]._rainfall_base += rain

            # diffuse
            if index!=(len(clouds)-1):
                diff = new_cloud[index+1][0] - new_cloud[index][0]
                new_cloud[index][0]   += diff*diffusion
                new_cloud[index+1][0] -= diff*diffusion
           
            # cloud moves forward
            new_cloud[index][1] += (1.0-pressure)*x_step
            

        for index in range(len(clouds)):
            clouds[index] = [new_cloud[index][0], new_cloud[index][1]]

        if plotting:
            plot_it = [[clouds[index][0] for index in range(len(clouds))], [clouds[index][1]  for index in range(len(clouds)) ], [ index_to_y(index) for index in range(len(clouds))] ]
            plt.figure(1)
            plt.clf()
            plt.plot(plot_it[2], plot_it[0],'d')
            plt.title("Rainfall!")
            plt.ylim([0,105])
            plt.show()
            plt.figure(2)
            plt.clf()
            plt.title("Cloud Loc")
            plt.plot(plot_it[1], plot_it[2] )
            plt.xlim([0, dimensions[0]])
            plt.show()#block=False)
            plt.pause(0.05)

    percentages = [False for i in range(9)]
        
    
    while( min( [ i[1] for i in clouds] )<= dimensions[0] ):
        perc = int( 100.*clouds[0][1]/dimensions[0] )
        
        for test in range(len(percentages)):
            if percentages[test]:
                continue
            else:
                if perc > (test+1)*10:
                    print("{}% done".format((1.+test)*10.))
                    percentages[test] = True


        step()

    if plotting:
        plt.close()

    #                     Change Colors
    # ======================================================

    min_rain = 10000.
    max_rain = -1


    # set rainy thing
    for ID in main_map.catalogue.keys():
        
        this_hex = main_map.catalogue[ID]
        if not this_hex._is_land:
            continue
        if this_hex.genkey[0]=='1':
            continue

        if max_rain< this_hex._rainfall_base:
            max_rain = this_hex._rainfall_base
        if min_rain>this_hex._rainfall_base:
            min_rain = this_hex._rainfall_base
        

    print("Rainfall variance {}-{}".format(min_rain, max_rain))

    for ID in main_map.catalogue.keys():
        this_hex = main_map.catalogue[ID]
        if not this_hex._is_land:
            continue
        if this_hex.genkey[0]=='1':
            continue

        green = 100 + int(min( 155, max( 155*main_map.catalogue[ID]._rainfall_base/max_rain, 0.0 )))
        main_map.catalogue[ID].fill = ( main_map.catalogue[ID].fill[0],green ,main_map.catalogue[ID].fill[2])


if not os.path.isdir("./saves"):
    os.mkdir("saves")

save_map( main_map, out_file )

from math import exp
from MultiHex.hexmap import Hexmap, load_map, save_map

import os

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

# check if point is in the map
def point_is_in(point, dimensions):
    return( point.x < dimensions[0] and point.x > 0 and point.y < dimensions[1] and point.y>0)



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

def smooth(what = ['alt'] , which = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap')):
    
    main_map = load_map(which)

    full_str=""
    for thing in what:
        full_str += thing + "..."

    print("    smoothing... "+full_str)

    for ID in main_map.catalogue.keys():
        neighbors = main_map.get_hex_neighbors( ID )

        this_one = main_map.catalogue[ID]
                
        if 'alt' in what:
            # skip mountains 
            if not this_one.genkey[1]=='1':
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

        if 'rain' in what:
            if this_one._is_land and not (this_one.genkey[0]=='1'): 
                existing    = 1
                total       = this_one._rainfall_base
                for neighbor in neighbors:
                    if neighbor in main_map.catalogue:
                        if main_map.catalogue[neighbor]._is_land:
                            existing += 1
                            total    += main_map.catalogue[neighbor]._rainfall_base
                            
                
                # make this altitude the average of it and its neighbors (which exist)
                main_map.catalogue[ID]._rainfall_base = total / float(existing)
                if (total/float(existing)) > 1.0:
                    print("Warn! Setting rainfall > 1: {}".format(total/float(existing)))

                green = 100 +  int(min( 120, max( 120*main_map.catalogue[ID]._rainfall_base, 0.0 )))
                main_map.catalogue[ID].fill = ( 155, green, 0)
            else:
                # we're not smoothing the rainfall for the ocean
                pass 
    save_map( main_map, which )

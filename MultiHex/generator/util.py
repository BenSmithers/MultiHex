from math import exp
from MultiHex.core import Hexmap, load_map, save_map

import random
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
# used literally all of the time 

# TODO: generalize to different map shapes? 
# could be cool to do a Mollweide like projection 
def point_is_in(point, dimensions):
    return( point.x < dimensions[0] and point.x > 0 and point.y < dimensions[1] and point.y>0)


# open the files, build the function we need
#  This function is deprecated. It is kept here solely for the author to either delete or use elsewhere.
resources_dir = os.path.join( os.path.dirname(__file__),'..','resources')
adj_obj = open(os.path.join( resources_dir , "adjectives"),'r')
_adjectives = adj_obj.readlines()
adj_obj.close()
def _get_adj():
    which = _adjectives[int(random()*len(_adjectives))]
    return( which[0].upper() + which[1:-1] )

#  This function is deprecated. It is kept here solely for the author to either delete or use elsewhere.
noun_obj = open(os.path.join( resources_dir, "nouns"),'r')
_nouns = noun_obj.readlines()
noun_obj.close()
def _get_noun():
    which = _nouns[int(random()*len(_nouns))]
    return( which[0].upper() + which[1:-1])

#  This function is deprecated. It is kept here solely for the author to either delete or use elsewhere.
def get_name( what ):

    word = ""
    if random()>0.75:
        naan = _get_noun()
        word += _get_adj()+naan[0].lower() + naan[1:] + " "
    word += "The "+_get_adj() +" "+ what[0].upper()+what[1:]
    
    if random()>0.75:
        word+= " Of "+_get_noun()
        if random()>0.85:
            word+=" and "+ _get_noun()
            
            if random()>0.97:
                word+= " and also" + _get_noun() + " too"

    return( word )

#  The following function was written by Ross McGuyer. Credit goes to the author (currently unknown) of
#  http://pcg.wikidot.com/pcg-algorithm:markov-chain, as much of the code used is derived from the example.

#  create_name
#  Parameter(s): what - The region type. Appended to somewhere to the returned string.
#                order - Controls how complex each look up syllable. Default value is 2.
#  Return: A string to be used as a moniker for a region. Contains the region type so that users know what the region
#           represents.
#  Description: This function uses a simple markov chain to generate a name.


def create_name(what, order=2):

    mid_table, start_list = fill_name_tables(what, order)  # The markov chain
    syns = fetch_synonyms(what)
    name = generate_name(mid_table, order, start_list)
    final_name = determine_name_style(syns, name)
    return final_name

#  The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
#  of http://pcg.wikidot.com/pcg-algorithm:markov-chain, much of the code used is derived from the example.
#  fill_name_table
#  Parameter(s): what - The region type. Eventually used to determine the style of the generated name.
#                order - Controls how complex each look up syllable.
#  Return: A table containing the markov chain and weights
#  Description: This function reads from a file containing several example words/names and uses that to generate the
#                   rules for generating names.

mor_obj = open(os.path.join( resources_dir , "Morrowind"),'r')
_morrowind = mor_obj.readlines()
mor_obj.close()
def fill_name_tables(what, order):

    mid_table = {}
    start_list = []
    for word in _morrowind:
        start_list.append(word[:2])
        for i in range(len(word) - order):
            try:
                mid_table[word[i:i+order]]
            except KeyError:
                mid_table[word[i:i + order]] = []
            mid_table[word[i:i + order]] += word[i+order]

    return mid_table, start_list

#  The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
#  of http://pcg.wikidot.com/pcg-algorithm:markov-chain, since much of the code used is derived from the example.
#  fill_name_table
#  Parameter(s): table - The markov chain needed to form the name.
#                order - Controls how complex each look up syllable.
#                start - An index that chooses what syllable to start the new name with. Default is None, which means
#                           a random syllable in table is used.
#                max_length - controls that sizes of the word. Ideally terminating characters are reached, but in rare
#                               case they are not and you don't want super long names. Default value is 20.
#  Return: A string containing the a procedurally generated name.
#  Description: This function splices together elements from table to create a randomized (but sensible) word or name.


def generate_name(mid_table, order, start=None, max_length=20):

    name = ""
    if start == None:
        name += random.choice(list(mid_table))
    else:
        name += random.choice(start)
    try:
        while len(name) < max_length:
            name += random.choice(mid_table[name[-order:]])
    except KeyError:
        pass

    return name

#  fetch_synonyms
#  Parameter(s): what - The region type. Use to determine which synonym list to return.
#  Return: syns - A list of strings containing synonyms of 'what'.
#  Description: Takes in a string and returns a list containing the string and several synonyms.


def fetch_synonyms(what):

    switcher = {
        "grassland": ["Grasslands", "Fields", "Prairie", "Plains", "Steppes"],
        "desert": ["Desert", "Badlands", "Wastes", "Barrens"],
        "mountain": ["Mountains", "Peaks", "Crags"],
        "forest": ["Forest", "Woods", "Woodlands", "Backwoods", "Wilds"],
        "arctic": ["Boreal","Frost", "tundra","Arctic"],
        "river": ["Creek","River","Stream"]
    }

    return switcher.get(what, ["Invalid What"])

#  determine_name_style
#  Parameter(s): syns - list of generated synonyms of the region type
#  Return: A string to be used as a moniker for a region. Can either be in the format "The [region] of [name]" or
#           or "The [Name] [Region]"
#  Description: This randomly decides between two methods of arranging the region and the name.


def determine_name_style(syns, name):

    final_name = "The "
    result = random.randint(0, 100)
    if(result > 30):
        final_name += (name + " " + random.choice(syns))
    else:
        final_name += (random.choice(syns) + " of " + name)
    return final_name


def new_color(is_land, altitude):

    """
    TODO generalize this for a any hex
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
    """
    smooths some feature of all the hexes

    So far only elevation and rainfall can be smoothed, but this can be generalized for almost anything at the moment.
    Would be better to use the getattr('whatever') command, and then I could literally generalize this to anything 
    """
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

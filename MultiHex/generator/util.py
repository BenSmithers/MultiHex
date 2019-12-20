from math import exp
from MultiHex.core import Hexmap, load_map, save_map

import random
import os
import pickle
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

#  The following function was written by Ross McGuyer. Credit goes to the author (currently unknown) of
#  http://pcg.wikidot.com/pcg-algorithm:markov-chain, as much of the code used is derived from the example.

#  create_name
#  Parameter(s): what - The region type. Appended to somewhere to the returned string.
#                order - Controls how complex each look up syllable. Default value is 2.
#  Return: A string to be used as a moniker for a region. Contains the region type so that users know what the region
#           represents.
#  Description: This function uses a simple markov chain to generate a name.


def create_name(what, order=2, filename="Morrowind"):

    try:
        mid_table, start_list = open_tables(filename)
    except:
        try:
            mid_table, start_list = fill_name_tables(what, order, filename)  # The markov chain
        except:
            print("Ey yo, file not found dawg!")
            raise
    syns = fetch_synonyms(what)
    name = generate_name(mid_table, order, start_list)
    final_name = determine_name_style(syns, name)
    return final_name

#  The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
#  of http://pcg.wikidot.com/pcg-algorithm:markov-chain, much of the code used is derived from the example.
#  fill_name_table
#  Parameter(s): what - The region type. Eventually used to determine the style of the generated name.
#                order - Controls how complex each look up syllable.
#                filename - the text file to read from
#  Return: A table containing the markov chain and weights
#  Description: This function reads from a file containing several example words/names and uses that to generate the
#                   rules for generating names.


def fill_name_tables(what, order, filename):
    
    if not os.path.exists( os.path.join( resources_dir , 'binary_tables' )):
        os.mkdir( os.path.join( resources_dir, 'binary_tables'))

    mid_table = {}
    start_list = []
    try:
        file_obj = open(os.path.join(resources_dir, "text_files", filename), 'r')
        _file_obj = file_obj.readlines()
        file_obj.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

    for word in _file_obj:
        if word[-1] == '\n':
            no_newline = word[0:len(word)-1]
        else:
            no_newline = word
        start_list.append(no_newline[:2])
        for i in range(len(no_newline) - order):
            try:
                mid_table[no_newline[i:i+order]]
            except KeyError:
                mid_table[no_newline[i:i + order]] = []
            mid_table[no_newline[i:i + order]] += no_newline[i+order]

    save_tables(start_list, mid_table, filename)

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
            if not break_name_loop(name):
                name += random.choice(mid_table[name[-order:]])
            else:
                break
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
        "forest": ["Forest", "Woods", "Woodlands", "Backwoods"],
        "rainforest": ["Darkwoods","Tangle", "Rainforest", "Wilds", "Jungle"],
        "arctic": ["Boreal","Frost","Arctic"],
        "tundra": ["Tundra"],
        "river": ["Creek","River","Stream", "Rapids"],
        "wetlands":["Bog", "Fen", "Swamp", "Marsh"],
        "savanah":["Savanah"]
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


#  open_table
#  Parameter(s): filename - the type of style table to retrieve.
#  Return: N/A
#  Description: This takes in both the start_table and the mid_table and pickles them as binary files.

def open_tables(filename):
    try:
        start_file = open(os.path.join(resources_dir, 'binary_tables',filename + '_start'), 'rb')
        start_list = pickle.load(start_file)
        start_file.close()

        mid_file = open(os.path.join(resources_dir, 'binary_tables', filename + '_mid'), 'rb')
        mid_table = pickle.load(mid_file)
        mid_file.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        print("Could not find existing table that matched, creating new table from text file.")
        raise

    return mid_table, start_list

#  save_table
#  Parameter(s): start_table - the table of start characters to be saved
#                mid_table - the table of mid word syllables
#                filename - the name of the file associated with the start and mid tables
#  Return: N/A
#  Description: This takes in both the start_table and the mid_table and pickles them as binary files.


def save_tables(start_table, mid_table, filename):
    
    if not os.path.exists( os.path.join( resources_dir , 'binary_tables' )):
        os.mkdir( os.path.join( resources_dir, 'binary_tables'))

    try:
        start_file = open(os.path.join(resources_dir, 'binary_tables', filename + '_start'), 'wb')
        pickle.dump(start_table, start_file, -1)
        start_file.close()

        mid_file = open(os.path.join(resources_dir, 'binary_tables', filename + '_mid'), 'wb')
        pickle.dump(mid_table, mid_file, -1)
        mid_file.close()
    except IOError as e:
        print("The following error occurred while trying to create new table...")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

    return

#  break_name_loop
#  Parameter(s): name - the name being generated thus far
#  Return: True/False
#  Description: This takes in the currently generated name and decides whether or not to continue building
#                   the name or cutting it short. It will ensure that all names are at least 3 characters long.


def break_name_loop(name):
    if len(name) >= 3:
        chance = 100 - len(name)*5
        if random.randint(1, 100) >= chance:
            return True
    return False

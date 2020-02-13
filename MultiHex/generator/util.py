#!/usr/bin/python3.6

from math import exp
from MultiHex.core import Hexmap, load_map, save_map, Point, deconstruct_id

import random
import os
import pickle
from numpy import save, load, min, max, ndarray
from numpy.random import rand
#                  Prepare Utilities
# =====================================================

def _is_valid_texture(obj):
    """
    Checks the object provided to verify that it is a properly formated texture list
    """
    if not (isinstance(obj, list) or isinstance(obj, ndarray)):
        print("Not List, {}".format(type(obj)))
        return(False)
    if not (isinstance(obj[0], list) or isinstance(obj[0],ndarray)):
        print("Not List, {}".format(type(obj[0])))
        return(False)
    if not (len(obj)==len(obj[0])):
        print("Not rectangular")
        return(False)
    if not (isinstance(obj[0][0], float) or isinstance(obj[0][0], int)):
        print("Not number")
        return(False)
    return(True)

def _save_texture(obj):
    """
    Saves the texture to a numpy file and also ensures it is a properly formated texture list
    """
    assert(_is_valid_texture(obj))
    where = os.path.join(os.path.dirname(__file__),'.texture.npy')
    save( where, obj)

def _load_texture():
    """
    Loads the saved texture and verifies that it is valid before returning it
    """
    where = os.path.join(os.path.dirname(__file__),'.texture.npy')
    temp = load(where)
    assert(_is_valid_texture(temp))
    return( temp )

def sample_noise(x_pos, y_pos, xsize=None, ysize=None, texture=None):
    """
    Samples from a texture list-object by interpolating between points in its 2D array. This is done by treating the two indices of the texture as (x,y) coordinates.
    When a point between those integer indices is requested, the average of the values corresponding to the indices that are floor and roof of that point are used.

    When an xsize and ysize are specified, we stretch the provided x_pos and y_pos to fit within the texture's bounds by treating the x/ysize as the maximum index of the texture. 

    params
    x_pos   - float, the x position at which to sample
    y_pos   - float, the y position at which to sample

    """

    # optionally, the user can pass the texture itself to minimize IO
    if texture is None:
        try:
            texture = _load_texture()
        except IOError:
            print("File not found while sampling. Generating...")
            _generate_perlin_texture()
            texture = _load_texture()
    else:
        if not _is_valid_texture(texture):
            raise ValueError("Something was wrong with the specified texture")

    # we need to stretch the texture to fit the map
    if xsize is None:
        xscale_factor = 1.
    else:
        assert( isinstance(xsize,float) or isinstance(xsize,int))
        xscale_factor = float(len(texture))/xsize
    if ysize is None:
        yscale_factor = 1.
    else:
        yscale_factor = float(len(texture[0]))/ysize

    # get the lower corner in the texture that the requested position is closest to
    xsam = int(x_pos*xscale_factor)
    ysam = int(y_pos*yscale_factor)

    # we need to be sure we're sampling within the bounds of the texture
    if not (xsam < len(texture) and xsam>=0):
        raise ValueError("Position {} is beyond the extent {}".format(xsam, len(texture)))
    if not (ysam < len(texture[0]) and ysam>=0):
        raise ValueError("Position {} is beyond the extent {}".format(ysam, len(texture[0])))


    # now just average the pixels around the sampled point
    value = texture[xsam][ysam] + texture[(xsam+1)%len(texture)][ysam] + texture[xsam][(ysam+1)%len(texture[0])] + texture[(xsam+1)%len(texture)][(ysam+1)%len(texture[0])]
    return( 0.25*value)

def _generate_perlin_texture(size = 512):
    """
    This generates a texture from which to sample in the perlinize function. 
    """
    assert(isinstance(size, int))
    assert( size % 2 == 0 )

    # we need a 2D array of points which will represent our noise texture
    #    later, we will sample from this texture by interpolating between points on it
    grid_full = [ [rand() for j in range(size)] for i in range(size) ]

    # now we need some down-sampled maps to apply large-scale fluctuations

    # So first we find the maximum number of downsamples we can perform
    levels = 1
    while (size % (2**levels) ==0):
        levels += 1
    levels-=1
    print("Doing {} levels of down-sampling".format(levels))

    downsamples = {}
    for level in range(levels):
        eff_size = int(size/(2**(level+1)))
        downsamples[ level ] = [ [rand() for j in range(eff_size)] for i in range( eff_size ) ]


    # now we go add all the layers together
    for i in range(size):
        for j in range(size):
            for level in range(levels):
                eff_size = int(size/(2**(level+1)))
                eff_i = int(i/(2**(level+1))) 
                eff_j =  int(j/(2**(level+1)))
                grid_full[i][j] += 0.6*((level+1)**1)*downsamples[level][ eff_i ][ eff_j ]

                grid_full[i][j] += 0.1*((level+1)**1)*( downsamples[level][ (eff_i+1)%eff_size ][ eff_j ] \
                                + downsamples[level][ eff_i   ][ (eff_j+1)%eff_size ] \
                                + downsamples[level][ (eff_i-1)%eff_size ][ eff_j ] + downsamples[level][ eff_i ][ (eff_j-1)%eff_size ]  )

    maax = max(grid_full)
    miin = min(grid_full)
    for i in range(size):
        for j in range(size):
            grid_full[i][j] = 2*((grid_full[i][j]- miin)/(maax - miin)) - 1

    _save_texture(grid_full)



def perlinize( which = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap'), attr='_altitude_base', magnitude = 0.20 ):
    """
    Injets perline noise into the specified map's attribute. 

    @param which - which map. Either a string specifying the filepath or a pointer to the Hexmap
    @param attr  - which hex attribute to modify 
    @param magnitude - scale of noise to inject. 0.05-0.40
    """
    
    # this opens the map / loads the map to the proper variable 
    if isinstance(which,str):
        main_map = load_map(which)
    #elif isinstance(which, Hexmap):
    #    main_map = which
    else:
        raise TypeError("Unexpected type for arg 'which': {}. Expected {} or {}".format(type(which), str, Hexmap))


    # should ensure that the attribute given and the magnitude are appropriately typed
    if not isinstance( attr, str ):
        raise TypeError("Unexpected type {} for arg 'str', expected {}".format(type(attr), str))
    if not isinstance(magnitude, float):
        raise TypeError("Expected {} for 'magnitude', got {}".format(float, type(magnitude)))
    
    # We need to make sure the attribute exist in our Hexes! This way we don't waste time creating a texture we don't need 
    for HexID in main_map.catalogue:
        if hasattr( main_map.catalogue[HexID], attr):
            break
        else:
            raise KeyError("HexMap does not have attribute {}".format(attr))

    # We need to create a noise texture file
    _generate_perlin_texture()
    # then grab it into an object to minimize IO later on
    texture = _load_texture()
    for HexID in main_map.catalogue:
        this_hex = main_map.catalogue[HexID]
        cent = this_hex.center
        # use the Hexes location to skew the specified attribute of the hex 
        new_value = getattr(this_hex, attr) + magnitude*sample_noise(cent.x, cent.y, main_map.dimensions[0], main_map.dimensions[1], texture)
        setattr( this_hex, attr, new_value)
        this_hex.rescale_color()
    save_map( main_map, which )



def angle_difference( theta_1, theta_2 ):
    """
    Returns the absolute difference between two angles

    @param theta_1 - first angle [degrees]
    @param theta_2 - second angle [degrees]
    """
    if not isinstance( theta_1, float):
        raise TypeError("theta_1 not {}, it's {}".format(float, type(theta_1)))
    if not isinstance( theta_2, float):
        raise TypeError("theta_2 not {}, it's {}".format(float, type(theta_2)))

    if not (theta_1 >= 0 and theta_1<=360):
        raise Exception("bad angle {}".format(theta_1))
    if not (theta_2 >= 0 and theta_2<=360):
        raise Exception("bad angle {}".format(theta_2))
    
    return(min([(360.) - abs(theta_1-theta_2), abs(theta_1-theta_2)]) )


def get_distribution( direction, variance=20. ):
    """
    Creates a normalized, discrete, gaussian distribution centered at a given angle and with a given variance. Distribution applies to the six angles correlated with the directions to a Hexes' neighbors' centers. 

    @param direction - mean of distribution
    @param variance -  variance of distribution
    """
    normalization = 0
#    variance = 20.
    angles = [150., 90., 30., 330., 270., 210.]

    # We do this to calculate the overall normalization
    for angle in angles:
        normalization += exp( -1.*(angle_difference(angle, direction)**2)/(2*variance**2))

    # Then prepare a function returning normalized probabilities 
    def distribution(angle): 
        return( (1./normalization)*exp(-1*(angle_difference(angle, direction)**2)/(2*variance**2)))

    return( distribution )

def point_is_in(point, dimensions):
    """
    Returns whether or not a Point is within the bounds of a map of given dimensions.

    @param Point    - a Point object
    @param dimensions - list-like 
    """
    if not isinstance(point, Point):
        raise TypeError("Expected type {}, got {}".format(Point, type(point)))

    return( point.x < dimensions[0] and point.x > 0 and point.y < dimensions[1] and point.y>0)


# open the files, build the function we need
#  This function is deprecated. It is kept here solely for the author to either delete or use elsewhere.
resources_dir = os.path.join( os.path.dirname(__file__),'..','resources')


def create_name(what, order=2, filename="Morrowind"):
    """
    The following function was written by Ross McGuyer. Credit goes to the author (currently unknown) of
    http://pcg.wikidot.com/pcg-algorithm:markov-chain, as much of the code used is derived from the example.

    create_name
    Parameter(s): what - The region type. Appended to somewhere to the returned string.
                    order - Controls how complex each look up syllable. Default value is 2.
    Return: A string to be used as a moniker for a region. Contains the region type so that users know what the region represents.
    Description: This function uses a simple markov chain to generate a name.
    """
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

def fill_name_tables(what, order, filename):
    """ 
    The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
    of http://pcg.wikidot.com/pcg-algorithm:markov-chain, much of the code used is derived from the example.
    fill_name_table
    Parameter(s): what - The region type. Eventually used to determine the style of the generated name.
                    order - Controls how complex each look up syllable.
                    filename - the text file to read from
    Return: A table containing the markov chain and weights
    Description: This function reads from a file containing several example words/names and uses that to generate the rules for generating names.   
    """
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


def generate_name(mid_table, order, start=None, max_length=20):
    """
    The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
    of http://pcg.wikidot.com/pcg-algorithm:markov-chain, since much of the code used is derived from the example.
    fill_name_table
    Parameter(s): table - The markov chain needed to form the name.
                  order - Controls how complex each look up syllable.
                  start - An index that chooses what syllable to start the new name with. Default is None, which means
                             a random syllable in table is used.
                  max_length - controls that sizes of the word. Ideally terminating characters are reached, but in rare
                                 case they are not and you don't want super long names. Default value is 20.
    Return: A string containing the a procedurally generated name.
    Description: This function splices together elements from table to create a randomized (but sensible) word or name.
    """
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



def fetch_synonyms(what):
    """
    fetch_synonyms
    Parameter(s): what - The region type. Use to determine which synonym list to return.
    Return: syns - A list of strings containing synonyms of 'what'.
    Description: Takes in a string and returns a list containing the string and several synonyms.
    """
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


def determine_name_style(syns, name):
    """
    determine_name_style
    Parameter(s): syns - list of generated synonyms of the region type
    Return: A string to be used as a moniker for a region. Can either be in the format "The [region] of [name]" or
             or "The [Name] [Region]"
    Description: This randomly decides between two methods of arranging the region and the name.
    """

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

                green = 100 +  int(min( [120, max([ 120*main_map.catalogue[ID]._rainfall_base, 0.0  ])]))
                main_map.catalogue[ID].fill = ( 155, green, 0)
            else:
                # we're not smoothing the rainfall for the ocean
                pass 
    save_map( main_map, which )


def open_tables(filename):
    """
    open_table
    Parameter(s): filename - the type of style table to retrieve.
    Return: N/A
    Description: This takes in both the start_table and the mid_table and pickles them as binary files.
    """
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


def save_tables(start_table, mid_table, filename):
    """
    save_table
    Parameter(s): start_table - the table of start characters to be saved
                  mid_table - the table of mid word syllables
                  filename - the name of the file associated with the start and mid tables
    Return: N/A
    Description: This takes in both the start_table and the mid_table and pickles them as binary files.
    """
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


def break_name_loop(name):
    """
    break_name_loop
    Parameter(s): name - the name being generated thus far
    Return: True/False
    Description: This takes in the currently generated name and decides whether or not to continue building
                     the name or cutting it short. It will ensure that all names are at least 3 characters long.
    """
    if len(name) >= 3:
        chance = 100 - len(name)*5
        if random.randint(1, 100) >= chance:
            return True
    return False

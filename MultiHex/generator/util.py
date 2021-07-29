#!/usr/bin/python3.6

from math import exp
from MultiHex.core import Hexmap, load_map, save_map, Point, deconstruct_id, Point, PointNd, Hex
from MultiHex.map_types.overland import River

import random
import os # used by the Climatizer 
import pickle
import json # used by the Climatizer
from numpy import save, load, min, max, ndarray
from numpy.random import rand
#                  Prepare Utilities
# =====================================================

def get_tileset_params(tileset = "standard"):
    if not isinstance(tileset, str):
        raise TypeError("Passed tileset should be {}, not {}".format(str, type(tileset)))

    loc = os.path.join(os.path.dirname(__file__), '..' ,'resources', 'tilesets.json')
    file_object = open( loc, 'r')
    config = json.load( file_object )
    file_object.close()

    # get the parameters
    parameters = []
    ignoring = ["color","is_ray"]
    for super_type in config[tileset]["types"]:
        for sub_type in config[tileset]["types"][super_type]:
            for param in config[tileset]["types"][super_type][sub_type]:
                if param not in ignoring:
                    parameters.append( param )
            # we really only need to do this for the first entry. So let's break! 
            break
        break
    return( parameters )
    # this is a length of strings. It tells the object what to access in the Hexes

class Climatizer:
    def __init__(self, tileset = "standard"):

        loc = os.path.join(os.path.dirname(__file__), '..' ,'resources', 'tilesets.json')
        file_object = open( loc, 'r')
        self.tileset = tileset
        self.config = json.load( file_object )
        file_object.close()

        if tileset not in self.config:
            raise IOError("Tileset {} not in `tilesets.json` file".format(tileset))

        # this is a length of strings. It tells the object what to access in the Hexes
        self.parameters = get_tileset_params(tileset)
        assert(len(self.parameters)>=1)


    def get_sup_sub(self, parameters):
        """
        For a given set of parameters (list of numbers), get the sub-type and super-type from the given tileset 
        """
        if not isinstance(parameters, list):
            raise TypeError("Parameters should be type {}, got {}".format(list, type(parameters)))
        # the number of parameters needs to match that which this object has been configured for 
        if not (len(parameters) == len(self.parameters)):
            raise ValueError("Should specify {} params, got {}".format(len(self.parameters), len(parameters)))
        for entry in parameters:
            if not (isinstance( entry,int) or isinstance(entry, float)):
                raise TypeError("Found non-numberlike entry: {}".format(entry))

        # build a point for these parameters 
        testing = PointNd( parameters )
        distance = 100.
        curr_pt = None
        super = ""
        sub = ""

        # loop over all the specified presets and find the one closest to the parameters were given 
        for super_type in self.config[self.tileset]["types"]:
            for sub_type in self.config[self.tileset]["types"][super_type]:
                which = self.config[self.tileset]["types"][super_type][sub_type]
                temp  =[ which[param] for param in self.parameters ]
                new = PointNd( temp )

                # none found yet, set the chosen one and move on
                if which=="":
                    curr_pt = new
                    super = super_type
                    sub = sub_type
                    distance = distance_between( testing, new)
                    continue

                # calculate at distance depending on whether we treat this as a "ray" or a point in space
                if self.config[self.tileset]["types"][super_type][sub_type]["is_ray"]:
                    # temporarily disabling the ray stuff
                    dist = distance_between( testing, new )
                else:
                    dist = distance_between( testing, new)

                # if this biome is closer to the sampled point than the current best fit, assign it! 
                if dist < distance:
                    distance = dist
                    curr_pt = new
                    sub = sub_type
                    super = super_type

        return( super, sub )

    def apply_climate_to_hex( self, target ):
        """
        Uses the Climatizer's configuration to assign a new fill and "climate" to the Hex
        """
        if not isinstance(target, Hex):
            raise TypeError("Expected {}, got {}".format(Hex, type(target)))

        temp  = [ getattr(target, param) for param in self.parameters ]
        for iter in range(len(temp)):
            if isinstance(temp[iter], bool):
                temp[iter] = int(temp[iter])*10.

        super, sub = self.get_sup_sub( temp )

        target._fill = tuple( self.config[self.tileset]["types"][super][sub]["color"] )
        target.biome = sub



def distance_between( point1, point2):
    """
    Returns the distance between two Points 
    """
    if not isinstance(point1, Point):
        raise TypeError("Expected type {}, got {}".format(Point, type(point1)))
    if not isinstance(point2, Point):
        raise TypeError("Expected type {}, got {}".format(Point, type(point2)))

    new = point1 - point2
    return( new.magnitude )

def distance_from_climate_ray( point1, ray):
    if not isinstance(point1, PointNd):
        raise TypeError("Expected type {}, got {}".format(Point3d, type(point1)))
    if not isinstance(ray, PointNd):
        raise TypeError("Expected type {}, got {}".format(Point3d, type(ray)))
    
    if point1.z > ray.z:
        return( distance_between( point1, ray))
    else:
        difference = ray - point1
        return( sqrt( difference.x**2 + difference.y**2) )


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
        "prarie": ["Grasslands", "Fields", "Prairie", "Plains", "Steppes"],
        "desert": ["Desert", "Badlands", "Wastes", "Barrens"],
        "mountain": ["Mountains", "Peaks", "Crags"],
        "ridge":["Ridge"],
        "wetland": ["Swamp","Bog", "Fen", "Marsh"],
        "gentle forest": ["Forest", "Woods", "Woodlands", "Backwoods"],
        "dark forest": ["Darkwoods","Tangle", "Rainforest", "Wilds", "Jungle"],
        "scrub":["Wastes", "Scrubland","Flats","Expanse","Rot"],
        "tundra": ["Boreal","Frost","Arctic"],
        "river": ["Creek","River","Stream", "Rapids"],
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

    for ID in main_map.catalog.keys():
        neighbors = main_map.get_hex_neighbors( ID )

        this_one = main_map.catalog[ID]
                
        if 'alt' in what:
            # skip mountains 
            if not this_one.genkey[1]=='1':
                existing = 1
                total    = this_one._altitude_base
                for neighbor in neighbors:
                    if neighbor in main_map.catalog:
                        existing += 1
                        total    += main_map.catalog[neighbor]._altitude_base 
                
                # make this altitude the average of it and its neighbors (which exist)
                main_map.catalog[ID]._altitude_base = total / float(existing)
                
                # this may have made ocean become land and land become ocean... 
                if main_map.catalog[ID]._altitude_base < 0.:
                    main_map.catalog[ID]._is_land = False
                    main_map.catalog[ID]._fill = new_color( False, total / float(existing))
                else:
                    main_map.catalog[ID]._is_land = True
                    main_map.catalog[ID]._fill = new_color( True, total/float(existing))

        if 'rain' in what:
            if this_one._is_land and not (this_one.genkey[0]=='1'): 
                existing    = 1
                total       = this_one._rainfall_base
                for neighbor in neighbors:
                    if neighbor in main_map.catalog:
                        if main_map.catalog[neighbor]._is_land:
                            existing += 1
                            total    += main_map.catalog[neighbor]._rainfall_base
                            
                
                # make this altitude the average of it and its neighbors (which exist)
                main_map.catalog[ID]._rainfall_base = total / float(existing)
                if (total/float(existing)) > 1.0:
                    print("Warn! Setting rainfall > 1: {}".format(total/float(existing)))

                green = 100 +  int(min( [120, max([ 120*main_map.catalog[ID]._rainfall_base, 0.0  ])]))
                main_map.catalog[ID]._fill = ( 155, green, 0)
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


"""
Implements several objects to be added on the map

Entries
    Entity          - A static object on the map
    Settlement      - Implements Entity. Represents somewhere people live 
    Mobile          - Implements Entity. A moving object on the map.
"""

from PyQt5 import QtGui
import os

from glob import glob

class Icons:
    def __init__(self):
        self._art_dir = os.path.join(os.path.dirname(__file__), '..', 'Artwork')
        self._icon_size = 24
        
        self._allowed_extensions = [".svg", ".png" ]

        for file_type in self._allowed_extensions:
            # gets a list of filenames matching the provided path, with * being a wildcard
            files_found = glob( os.path.join( self._art_dir, "*" + file_type) )
        
            # load that file in and apply it to the self
            for found_file in files_found:
                obj_name = os.path.basename(found_file).split(".")[0]
                if hasattr( self, obj_name):
                    print("Skipping '{}{}', already have file with same name".format( obj_name, file_type))
                    continue

                setattr( self, obj_name , QtGui.QPixmap(found_file).scaledToWidth( self._icon_size) )
                print("Loaded media '{}{}'".format( obj_name, file_type ))
    
    @property
    def shift(self):
        return( self._icon_size / 2)


class Entity:
    """
    Defines static entity that can be placed on a Hex
    """
    def __init__(self, name, location = None ):
        """
        @param name     - String. name of this entity
        @param location - HexID. Where this entity is placed. (optional. Entites can be off the map)
        """

        if not type(name)==str:
            raise TypeError("Arg 'name' must be {}, received {}".format(str, type(name)))
        self.name        = name
        self.description = ""
        self.icon        = ""

        self._location = location
    
    @property 
    def location( self ):
        copy = self._location
        return( copy )


class Settlement(Entity):
    """
    Generic implementation for settlements of people. Can be applied for space stations, planets, towns, or anything really. Maintains a total population and its demographics. 

    Settlements can be divided into `wards` to represent sub-sections of the 
    """
    def __init__(self, name, location=None, is_ward=False):
        Entity.__init__(self, name, location)

        # these values are assigned to the city-center 
        self._population = 1
        self._wealth = 1

        self._order = 1.0
        self._war   = 1.0
        self._spirit= 1.0

        self.wards = [ ]
        self._is_ward = is_ward

        # this only describes the population directly contained by the _population attribute
        self.demographics = { 'racial': { 'human': 1.00 } }

    @property 
    def order(self):
        copy = self._order
        return(copy)
    @property 
    def war(self):
        copy = self._war
        return(copy)
    @property
    def spirit(self):
        copy = self._spirit
        return(spirit)
    def set_order(self, new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for order, expected {}".format(type(new), float ))
        self._order =  min( 1.0, max( 0.0, new))
    def set_war(self, new)
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for war, expected {}".format(type(new), float ))
        self._war =  min( 1.0, max( 0.0, new))
    def set_spirit(self,new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for spirit, expected {}".format(type(new), float ))
        self._spirit =  min( 1.0, max( 0.0, new))

    def get_demographics_as_str(self , ward, key):
        """
        Returns an entry in the demographics object formated in the ward-dialog style. Must specify a ward and the demographic
        """
        if not isinstance(ward, int):
            raise TypeError("Expected type {} for ward, but got {}".format( int, type(ward)))
        if not isinstance(key, str):
            raise TypeError("Expected type {} for key, but got {}".format( str, type(key)))
    
        out = ""
        if ward == 0:
            if key not in self.demographics:
                raise KeyError("Demographic {} is not in demographics.".format(key))

            for subkey in self.demographics[key]:
                out += "{}:{}".format(subkey, self.demographics[key][subkey])
        else:
            if key not in self.wards.demographics[ward-1]:
                raise KeyError("Demographic {} is not in Ward {}'s demographics".fprmat(key,ward))
            for subkey in self.wards.demographics[ward-1][key]:
                out += "{}:{}".format(subkey, self.wards[ward-1].demographics[key][subkey])
        return(out)


    @property
    def partial_wealth(self):
        """
        returns just the wealth belonging to the 'city center'. Does not include any ward wealth
        """
        return(self._wealth)

    @property
    def partial_population(self):
        """
        returns just the wealth belonging to the city center
        """
        return(self._population)

    def set_wealth(self,new_wealth, ward=None):
        diff = new_wealth - self.wealth

        self.add_wealth( diff, ward )

    def add_wealth( self, amount, which_ward = None):
        """
        Adds an amount of wealth to the settlement. If no ward is specified, it spreads the wealth according to populations 
        """
        if which_ward is None:
            self._wealth += int(amount*float(self._population/self.population))
            for ward in self.wards:
                ward.add_wealth( int(amount*float(ward.population/self.population)))
        else:
            if not isinstance( which_ward, int):
                raise TypeError("Expected type {} for ward, got {}".format(int, type(which_ward)))

            if which_ward == 0:
                self._wealth += amount
            else:
                lowered = which_ward - 1
                self.wards[lowered].add_wealth( amount )

    @property
    def wealth(self):
        """
        returns all the wealth of all the wards combined 
        """
        total_wealth = self._wealth
        for ward in self.wards:
            total_weatlth+= ward._wealth
        return(total_wealth)

    def add_ward( self, new_ward ):
        """
        Adds a ward to this settlement's list, such that it is now a part of this Settlement. 
        """

        if not isinstance(new_ward, Settlement):
            raise TypeError("Arg `new_ward` is type {}, expected {}".format(type(new_ward), Settlement))

        new_ward._is_ward = True
        self.wards.append( new_ward )

    def _valid_demo_structure( self, demo ):
        """
        Verifies that the passed demographics object is of the proper structure.

        We're expecting a dictionary containing dictionaries.
        """

        if type(demo)!=dict:
            return(False)
        else:
            for key in demo:
                if type( demo[key]) != dict :
                    return(False) 
        
        # ensure the demographics thing is normalized 
        for key in demo:
            total = 0.0
            for subkey in demo[key]:
                total += demo[key][subkey]

            if abs(total-1.0)>0.001:
                return(False)

        return(True)

    def _norm_demographics( self ):
        """
        Normalize the demographics dictionary! 
        """
        for key in self.demographics:
            total = 0.
            for subkey in self.demographics[key]:
                total += self.demographics[key][subkey]

            for subkey in self.demographics[key]:
                self.demographics[key][subkey] /= total
        
    def add_population(self, to_add, ward=None, demographics = None):
        """
        Adds population to the Settlement. If no ward is specified, it divides added population evently between the wards.  

        To specify wards are enumerated starting at 1. The 0-Ward is the city-center. 
        """
        if (demographics is not None) and (not self._valid_demo_structure( demographics )):
            raise ValueError("Arg 'demographics' is not structured properly.")
        else:
            if demographics is not None:
                # populate the dictionaries such that the keys are symmetric  
                for key in demographics:
                    if key not in self.demographics:
                        self.demographics[key] = {}
                    for subkey in demographics[key]:
                        if subkey not in self.demographics[key]:
                            self.demographics[key][subkey] = 0.0
                for key in self.demographics:
                    if key not in demographics:
                        demographics[key] = {}
                    for subkey in self.demographics[key]:
                        if subkey not in demographics[key]:
                            demographics[key][subkey] = 0.0

        # update the demographics of the main part of town 
        if demographics is not None:
            # update the demographics
            for key in self.demographics:
                for subkey in self.demographics[key]:
                    self.demographics[key][subkey] = (self.demographics[key][subkey]*self._population + demographics[key][subkey]*to_add)/( self._population + to_add )
                    if self.demographics[key][subkey] < 0:
                        self.demographics[key][subkey] = 0.0 

        if ward is None:
            if len(self.wards)==0:                
                self._population += to_add
                assert( self._population >= 0 )

            else:
                # keep track of number added to avoid rounding errors. Just put any extras in the main ward
                added = 0 
                pre_population = self.population

                added            += int(to_add*float(self._population)/pre_population)
                self._population += int(to_add*float(self._population)/pre_population)

                for ward in self.wards:
                    added   +=           int(to_add*float(ward.population)/pre_population)
                    ward.add_population( int(to_add*float(ward.population)/pre_population), demographics=demographics )
                    
                if added!=to_add:
                    self._population += ( to_add - added )
        else:
            if ward<0:
                raise ValueError("Invalid ward no. {}".format(ward))
            elif ward==0:
                self._population += to_add
            else:
                ward -= 1
                if ward>=(len(self.wards)):
                    raise ValueError("No ward of number {}".format(ward))
                else:
                    self.wards[ward].add_population( to_add, demographics = demographics )
        
        self._norm_demographics()

    def set_population(self, population, ward=None ):
        """
        Sets the population of the settlement to the given amount 
        """
        assert( isinstance( population, int))
        assert( population >= 0 )
        
        to_add = population - self.population
        self.add_population( to_add, ward )

    @property
    def population(self):
        pop = self._population
        for ward in self.wards:
            pop += ward.population
        return( pop )
        
    @property
    def size( self ):
        """
        Returns a string representing the effective size of the Settlement 
        """
        return("")

    def __str__(self):
        """
        Returns a string describing the settlement. Used implicitly with Python's print function
        """
        output = ""
        if self._is_ward:
            output += "    "

        output  += "{}: A {} of total poulation {}. ".format( self.name, self.size, self.population )
        if (not self._is_ward) and len(self.wards)!=0:
            output += "City Center Demographics...\n"
        else:
            output += "Demographics are...\n"
        for key in self.demographics:
            if self._is_ward:
                output += "    "
            output += "{}:\n".format( key[0].upper()+key[1:] )
            for subkey in self.demographics[key]:
                if self._is_ward:
                    output += "    "
                output += "    {:.2f}% {}\n".format( 100*self.demographics[key][subkey], subkey[0].upper()+subkey[1:])
        if len(self.wards)>0:
            output += "Contains Wards...\n"
            for ward in self.wards:
                output+= ward.__str__()

        return( output )
             

class Mobile( Entity ):
    """
    Defines a mobile map Entity. Fundamentally the same as an Entity, but its location can be moved 
    """
    def __init__(self, name):
        Entity.__init__(self, name, location=None)
        
        self.speed = 1. #miles/minute 

    def set_location(self, location):
        # add a check thingy
        self._location = location

    

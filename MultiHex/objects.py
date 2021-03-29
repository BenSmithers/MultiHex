
"""
Implements several objects to be added on the map

Entries
    Entity          - A static object on the map
    Settlement      - Implements Entity. Represents somewhere people live 
    Mobile          - Implements Entity. A moving object on the map.
"""

from PyQt5 import QtGui, QtWidgets, QtCore
import os

from glob import glob

from copy import deepcopy, copy

from MultiHex.logger import Logger

art_dir = os.path.join( os.path.dirname(__file__),'Artwork')

class PixHolder:
    """
    Generic implementation of an object that loads in images from some directory and stores them as pixmaps. 

    These are intended to be used as icons, buttons, and cursors to minimize the amount of times such pixmaps are stored in memory. 

    @ param subidr  - sub-directory of the Artwork directory where this object will search for Art
    """
    def __init__(self, subdir):
        assert( isinstance( subdir, str))
        self._art_dir = os.path.join(os.path.dirname(__file__), 'Artwork', subdir)
        if not os.path.isdir( self._art_dir ):
            raise OSError("No such directory exists at: {}".format( self._art_dir))

        self._icon_size = 24
        
        self._allowed_extensions = [".svg", ".png" ]

        self.pixdict = {} 

    def load(self):
        for file_type in self._allowed_extensions:
            # gets a list of filenames matching the provided path, with * being a wildcard
            files_found = glob( os.path.join( self._art_dir, "*" + file_type) )
        
            # load that file in and apply it to the self
            for found_file in files_found:
                obj_name = os.path.basename(found_file).split(".")[0]
                if obj_name in self.pixdict:
                    Logger.Log("Skipping '{}{}', already have file with same name".format( obj_name, file_type))
                    continue
            
                self.pixdict[ obj_name ] = QtGui.QPixmap(found_file).scaledToWidth( self._icon_size, 1) 
            if len(files_found)!=0:
                Logger.Log("Loaded ({}) media in {}".format(len(files_found), self._art_dir ))

    @property
    def shift(self):
        return( self._icon_size / 2)

class Icons( PixHolder ):
    def __init__(self):
        PixHolder.__init__(self,'map_icons')
        self.load()

class Cursors( PixHolder ):
    def __init__(self):
        PixHolder.__init__(self,'cursors')
        self.load()

class Buttons( PixHolder ):
    def __init__(self):
        PixHolder.__init__(self,'buttons')
        self.load()

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

    @staticmethod
    def widget(self):
        return [EntityWidget]

class GenericTab(QtWidgets.QWidget):
    def __init__(self, parent=None, config_entity=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        if not isinstance(config_entity, Entity):
            Logger.Fatal("Expected {}, got {}".format(Entity, type(config_entity)), TypeError)

    def set_configuration(self, entity):
        if not isinstance(entity, Entity):
            raise TypeError("Cannot configure object of type {}".format(type(entity)))
        return(entity)

    def get_configuration(self, entity):
        if not isinstance(entity, Entity):
            raise TypeError("Cannot configure object of type {}".format(type(entity)))


class EntityWidget(GenericTab):
    def __init__(self, parent=None, config_entity=None):
        GenericTab.__init__(self,parent, config_entity)
        self.setObjectName("EntityWidget")

        if False: #isinstance(self, MobileWidget):
            self.art_dir = os.path.join(art_dir, 'mobiles')
        else:
            self.art_dir = os.path.join(art_dir, 'map_icons')

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        # build the name label depending on the mode this is being built in
        font = QtGui.QFont()
        font.setPointSize(24)
        self.entity_name = QtWidgets.QLineEdit(self)
        self.entity_name.setObjectName("entity_name")
        self.entity_name.setFont(font)
        self.entity_name.setText("temp")

        self.verticalLayout.addWidget(self.entity_name)
        self.central_panes = QtWidgets.QHBoxLayout()
        self.left_pane = QtWidgets.QFormLayout()
        line = 0
        if isinstance(self, MobileWidget):
            self.speed_lbl = QtWidgets.QLabel(self)
            self.speed_lbl.setObjectName("speed_lbl")
            self.speed_lbl.setText("Speed:")
            self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.speed_lbl) #FieldRole SpanningRole
            self.speed_edit = QtWidgets.QDoubleSpinBox(self)
            self.speed_edit.setObjectName("speed_edit")
            self.speed_edit.setMinimum(0)
            self.speed_edit.setSingleStep(0.1)
            self.speed_edit.setDecimals(1)
            self.speed_edit.setMaximum(100.)
            self.left_pane.setWidget(line, QtWidgets.QFormLayout.FieldRole, self.speed_edit)
            line+=1

        self.description_lbl = QtWidgets.QLabel(self)
        self.description_lbl.setObjectName("description_lbl")
        self.description_lbl.setText("Description: \n")
        self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.description_lbl)
        line+=1
        self.description_edit = QtWidgets.QTextEdit(self)
        self.description_edit.setObjectName("description_edit")

        self.left_pane.setWidget(line, QtWidgets.QFormLayout.SpanningRole, self.description_edit)
        self.right_pane = QtWidgets.QVBoxLayout()
        self.icon_combo = QtWidgets.QComboBox(self)
        self.icon_combo.setObjectName("icon_combo")

        self.pictures = glob(os.path.join(self.art_dir, "*.svg"))
        self.pictures = [entry.split(".")[0] for entry in self.pictures]

        for each in self.pictures:
            name = os.path.basename(each)
            self.icon_combo.addItem( QtGui.QIcon(QtGui.QPixmap(each)), name )

        self.picture_box = QtWidgets.QLabel(self)
        self.picture_box.setObjectName("picture_box")
        self.picture_box.setPixmap(QtGui.QPixmap(os.path.join(self.art_dir,self.pictures[self.icon_combo.currentIndex()])).scaledToWidth(400))
        self.right_pane.addWidget(self.picture_box)
        self.right_pane.addWidget(self.icon_combo)
        # Picture spot

        self.central_panes.addItem(self.left_pane)
        self.central_panes.addItem(self.right_pane)
        self.verticalLayout.addItem(self.central_panes)

        self.icon_combo.currentIndexChanged.connect(self.combo_change)

        if config_entity is not None:
            self.get_configuration(config_entity)

        #self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.speed_lbl) #FieldRole SpanningRole

    def combo_change(self):
        self.picture_box.setPixmap(QtGui.QPixmap(os.path.join(self.art_dir,self.pictures[self.icon_combo.currentIndex()])).scaledToWidth(400))

    def set_configuration(self, entity):
        """
        Takes an entity and applies the GUIs current configuration to it

        returns the modified entity 
        """
        GenericTab.set_configuration(self, entity)

        entity.name = self.entity_name.text()
        entity.description = self.description_edit.toPlainText()
        entity.icon = self.icon_combo.currentText()
        return(entity)



    def get_configuration(self, entity):
        """
        Gets the configuration of the entity provided, and uses that to configure the gui

        returns void
        """
        GenericTab.get_configuration(self, entity)

        self.entity_name.setText(entity.name)
        self.description_edit.setText(entity.description)
        which = self.icon_combo.findText( entity.icon )
        if which==-1:
            Logger.Warn("Could not find icon of name: {}".format(entity.icon))
        else:
            self.icon_combo.setCurrentIndex(which)

class GovernmentWidget(GenericTab):
    def __init__(self, parent=None, config_entity=None):
        GenericTab.__init__(self, parent, config_entity)
        self.setObjectName("GovernmentWidget")

        self.formlayout = QtWidgets.QFormLayout(self)

        self.orderlbl = QtWidgets.QLabel(self)
        self.orderlbl.setObjectName("orderlbl")
        self.orderlbl.setText("Order: ")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.orderlbl)
        self.orderbar = QtWidgets.QSlider(self)
        self.orderbar.setOrientation(QtCore.Qt.Horizontal)
        self.orderbar.setObjectName("orderbar")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.orderbar)

        self.warlbl = QtWidgets.QLabel(self)
        self.warlbl.setObjectName("warlbl")
        self.warlbl.setText("War: ")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.warlbl)
        self.warbar = QtWidgets.QSlider(self)
        self.warbar.setOrientation(QtCore.Qt.Horizontal)
        self.warbar.setObjectName("warbar")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.warbar)

        self.spiritlbl = QtWidgets.QLabel(self)
        self.spiritlbl.setObjectName("spiritlbl")
        self.spiritlbl.setText("Spirit: ")
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.spiritlbl)
        self.spiritbar = QtWidgets.QSlider(self)
        self.spiritbar.setOrientation(QtCore.Qt.Horizontal)
        self.spiritbar.setObjectName("spiritbar")
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spiritbar)

        self.get_configuration(config_entity)

    def set_configuration(self, entity):
        GenericTab.set_configuration(self, entity)
        if not isinstance(entity, Government):
            raise TypeError("Expected {}, got {}".format(Government, type(entity)))

        entity.set_war(self.warbar.value()/100.)
        entity.set_spirit(self.spiritbar.value()/100.)
        entity.set_order(self.orderbar.value()/100.)
        return(entity)

    def get_configuration(self, entity):
        GenericTab.get_configuration(self, entity)
        if not isinstance(entity, Government):
            raise TypeError("Expected {}, got {}".format(Government, type(entity)))

        self.warbar.setValue(entity.war*100)
        self.spiritbar.setValue(entity.spirit*100)
        self.orderbar.setValue(entity.order*100)

class Government():
    """
    A Generic implementation of 'government.' Intended to not be used on its own, but as a parent class to other objects. 
    """
    def __init__(self, order = 0.0, war = 0.0, spirit = 0.0):

        self._order = order
        self._war   = war
        self._spirit= spirit

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
        return(copy)

    def set_order(self, new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for order, expected {}".format(type(new), float ))
        self._order =  min( 1.0, max( 0.0, new))
    def set_war(self, new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for war, expected {}".format(type(new), float ))
        self._war =  min( 1.0, max( 0.0, new))
    def set_spirit(self,new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for spirit, expected {}".format(type(new), float ))
        self._spirit =  min( 1.0, max( 0.0, new))

    @staticmethod
    def widget(cls):
        return [GovernmentWidget]

class SettlementWidget(GenericTab):
    def __init__(self, parent=None, config_entity=None):
        GenericTab.__init__(self, parent, config_entity)
        self.setObjectName("SettlementWidget")

        self.get_configuration(config_entity)

        self.formlayout = QtWidgets.QFormLayout(self)

        self.populationlbl = QtWidgets.QLabel(self)
        self.populationlbl.setObjectName("populationlbl")
        self.populationlbl.setText("Population: ")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.populationlbl)
        self.populationedit = QtWidgets.QSpinBox(self)
        self.populationedit.setMaximum(10000)
        self.populationedit.setMinimum(0)
        self.populationedit.setObjectName("populationedit")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.populationedit)

        self.wealthlbl = QtWidgets.QLabel(self)
        self.wealthlbl.setObjectName("wealthlbl")
        self.wealthlbl.setText("Wealth: ")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.wealthlbl)
        self.wealthedit = QtWidgets.QSpinBox(self)
        self.wealthedit.setMaximum(10000)
        self.wealthedit.setMinimum(0)
        self.wealthedit.setObjectName("wealthedit")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.wealthedit)

class Settlement(Entity, Government):
    """
    Generic implementation for settlements of people. Can be applied for space stations, planets, towns, or anything really. Maintains a total population and its demographics. 

    Settlements can be divided into `wards` to represent sub-sections of the 
    """
    def __init__(self, name, location=None, is_ward=False):
        Entity.__init__(self, name, location)
        Government.__init__(self)

        # these values are assigned to the city-center 
        self._population = 1
        self._wealth = 1

        self.wards = [ ]
        self._is_ward = is_ward

        # this only describes the population directly contained by the _population attribute
        self._demographics = { 'racial': { 'human': 1.00 } }

    @property
    def tension(self):

        if len(self.wards)==0:
            return(0)
        else:
            # get averages! 
            avg_ord = (self.partial_population/self.population)*self.order/(1+len(self.wards))
            avg_war = (self.partial_population/self.population)*self.war/(1+len(self.wards))
            avg_spi = (self.partial_population/self.population)*self.spirit/(1+len(self.wards))

            for ward in wards:
                avg_ord += (ward.population/self.population)*ward.order/(1+len(self.wards))
                avg_war += (ward.population/self.population)*ward.war/(1+len(self.wards))
                avg_spi += (ward.population/self.population)*ward.spirit/(1+len(self.wards))

            wip = (self.partial_population/self.population)*( ( avg_ord - self.order)**2 + (avg_war - self.war)**2 + (avg_spi - self.spirit)**2)
            for ward in wards:
                wip += (ward.population/self.population)*((avg_ord - ward.order)**2 + (avg_war - ward.war)**2 + (avg_spi - ward.spirit)**2)

            wip = sqrt(wip)
            return( wip )


    @property
    def demographics(self):
        """
        Returns a copy of this object's demographics! 
        """
        copy = deepcopy( self._demographics )
        return( copy )

    def set_demographics(self, new_demo):
        if not self._valid_demo_structure( new_demo ):
            raise TypeError("Improperly formatted demographics object!")
        
        self._demographics = new_demo
        self._norm_demographics()

    @staticmethod
    def widget(self):
        return Entity.widget(self)+Government.widget(self)+[SettlementWidget]

    def get_demographics_as_str(self):
        """
        Returns an entry in the demographics object formated in the ward-dialog style. Must specify a ward and the demographic
        """
  
        out = ""
        for key in self._demographics:
            out += "+{}\n".format(key)
            for subkey in self._demographics[key]:
                out+= "{}:{:.4f}\n".format(subkey, self._demographics[key][subkey])
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

    def set_wealth(self,new_wealth, which_ward=None):
        diff = new_wealth - self.wealth

        self.add_wealth( diff, which_ward )

    def add_wealth( self, amount, which_ward = None):
        """
        Adds an amount of wealth to the settlement. If no ward is specified, it spreads the wealth according to populations 
        """
        if which_ward is None:
            self._wealth += int(amount*float(self._population)/self.population)
            for ward in self.wards:
                ward.add_wealth( int(amount*float(ward.population)/self.population))
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
            total_wealth+= ward._wealth
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
        for key in self._demographics:
            total = 0.
            for subkey in self._demographics[key]:
                total += self._demographics[key][subkey]

            for subkey in self._demographics[key]:
                self._demographics[key][subkey] /= total
        
    def add_population(self, to_add, which_ward=None, demographics = None):
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
                    if key not in self._demographics:
                        self._demographics[key] = {}
                    for subkey in demographics[key]:
                        if subkey not in self._demographics[key]:
                            self._demographics[key][subkey] = 0.0
                for key in self._demographics:
                    if key not in demographics:
                        demographics[key] = {}
                    for subkey in self._demographics[key]:
                        if subkey not in demographics[key]:
                            demographics[key][subkey] = 0.0

        # update the demographics of the main part of town 
        if demographics is not None:
            # update the demographics
            for key in self._demographics:
                for subkey in self._demographics[key]:
                    self._demographics[key][subkey] = (self._demographics[key][subkey]*self._population + demographics[key][subkey]*to_add)/( self._population + to_add )
                    if self._demographics[key][subkey] < 0:
                        self._demographics[key][subkey] = 0.0 

        if which_ward is None:
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
            if which_ward<0:
                raise ValueError("Invalid ward no. {}".format(which_ward))
            elif which_ward==0:
                self._population += to_add
            else:
                which_ward -= 1
                if which_ward>=(len(self.wards)):
                    raise ValueError("No ward of number {}".format(which_ward))
                else:
                    self.wards[which_ward].add_population( to_add, demographics = demographics )
        
        self._norm_demographics()

    def set_population(self, population, which_ward=None ):
        """
        Sets the population of the settlement to the given amount 
        """
        assert( isinstance( population, int))
        assert( population >= 0 )
        
        to_add = population - self.population
        self.add_population( to_add, which_ward=which_ward )

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
        for key in self._demographics:
            if self._is_ward:
                output += "    "
            output += "{}:\n".format( key[0].upper()+key[1:] )
            for subkey in self._demographics[key]:
                if self._is_ward:
                    output += "    "
                output += "    {:.2f}% {}\n".format( 100*self._demographics[key][subkey], subkey[0].upper()+subkey[1:])
        if len(self.wards)>0:
            output += "Contains Wards...\n"
            for ward in self.wards:
                output+= ward.__str__()

        return( output )
             

class Mobile( Entity ):
    """
    Defines a mobile map Entity. Fundamentally the same as an Entity, but its location can be moved. Also allows for a route to be stored in the Mobile: it's planned direction in life 
    """
    def __init__(self, name):
        Entity.__init__(self, name, location=None)
        
        self._speed = 1. #miles/hour 

        # this is a list of hex IDs. It represents where the Mobile is going to go. 
        #    these should be managed by the ActionManager in `utils.py`
        self._route = []

    @property
    def route(self):
        return(self._route)

    def set_route(self, new_route = None):
        if new_route is None:
            self._route = []
        if not isinstance(new_route, (list,tuple)):
            raise TypeError("New route should be {}, got {}".format(list, type(new_route)))
        for entry in new_route:
            if not isinstance(entry, int):
                raise TypeError("Found {} in new_route. Should be {}, not {}".format(entry, int, type(entry)))

        self._route = new_route

    def set_location(self, location):
        if not isinstance(location,int):
            raise TypeError("Can only set location to {}, not {}".format(int, type(location)))
        self._location = location

    @property 
    def speed(self):
        return(self._speed)

    def set_speed(self, new_speed):
        if not (isinstance(new_speed,float) or isinstance(new_speed,int)):
            raise TypeError("Expected {}, got {}".format(float, type(new_speed)))
        if new_speed <= 0.:
            raise ValueError("Need positive speed, got {}".format(new_speed))

        self._speed = new_speed


class MobileWidget(EntityWidget):
    def __init__(self,parent=None, config_entity=None):
        EntityWidget.__init__(self,parent)
    
        self.get_configuration(config_entity)

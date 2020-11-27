from enum import Enum 

from MultiHex.objects import Mobile, Entity 
from MultiHex.clock import Clock, Time
from MultiHex.core import Hexmap

from MultiHex.logger import Logger

from panas import DataFrame, read_csv
import os


def get_base_dir():
    # set up the save directory
    if sys.platform=='linux':
        basedir = os.path.join(os.path.expandvars('$HOME'),'.local','MultiHex')
    elif sys.platform=='darwin': #macOS
        basedir = os.path.join(os.path.expandvars('$HOME'),'MultiHex')
    elif sys.platform=='win32' or sys.platform=='cygwin': # Windows and/or cygwin. Not actually sure if this works on cygwin
        basedir = os.path.join(os.path.expandvars('%AppData%'),'MultiHex')
    else:
        Logger.Fatal("{} is not a supported OS".format(sys.platform), NotImplementedError)

    return(basedir)

class mapActionItem(Enum):
    move = 1

class MapEvent:
    def __init__(self, kind,recurring=None, **kwargs):
        """
        An event used by the Action Manager. 

        kind - mapActionItem enum entry. Specifies what kind of event this is 
        recurring - a Time object. Represents how frequently the event happens. 'None' for one-time events. When this kind of event is triggered, a new one is auto-queued 
        kwargs - arguments specific to this kind of event. Varies 
        """
        if not isinstance(kind, mapActionItem):
            Logger.Fatal("Can only create action of type {}, not {}".format(mapActionItem, type(kind)), TypeError)

        if recurring is not None:
            if not isinstance(recurring, Time):
                Logger.Fatal("If recurring, arg must be {}, not {}".format(Time, type(recurring)), TypeError)
        self.recurring = recurring

        self.brief_desc = "" # will be used on the event list
        self.long_desc = ""

        # whether or not the event should appear in the Event List
        self._show = True

    @property
    def show(self):
        return(self._show)


class MapAction(MapEvent):
    def __init__(self, kind,recurring=None, **kwargs):
        """
        Implementation of MapEvent that actually does something. 
        """
        MapEvent.__init__(self, kind, recurring, **kwargs)

        if kind==mapActionItem.move:
            needed =["eID", "to"]
            for entry in needed:
                if entry not in kwargs:
                    Logger.Fatal("Missing entry {} in kwargs".format(entry), ValueError)
            self.eid = kwargs["eID"]
            self.to = kwargs["to"]

            def this_action(map):
                if not isinstance(map, Hexmap):
                    Logger.Fatal("Can only act on {}, not {}".format(Hexmap, type(map)), ValueError)
                map.eid_catalog[self.eid].set_location(self.to)

            self.do = this_action
            
        else:
            Logger.Fatal("Unrecognized kind: {}".format(kind), NotImplementedError)



class ActionManager:
    """
    This keeps track of upcoming events (and actions) and the time.
    It allows you to add new events and 
    """
    def __init__(self, parent_map):
        if not isinstance(parent_map, Hexmap):
            Logger.Fatal("Parent must be {}, received {}".format(Hexmap, type(parent_map)), TypeError)

        self._queue = []

        self.clock = Clock()
        self._parent = parent_map

        self.database_dir = get_base_dir()
        self.database_filename = "event_database.csv"


    def add_event(self, event, time):
        if not isinstance(event, MapEvent):
            Logger.Fatal("Can only register {} type events, not {}".format(MapEvent, type(event)), TypeError)
        if not isinstance(time, Time):
            Logger.Fatal("Expected {} for time, not {}.".format(Time, type(time)), TypeError)

        if len(self.queue)==0:
            self._queue.append( [time, event] )
        else:
            if time<self.queue[0][0]:
                self._queue.insert(0, [time,event])
            elif time > self.queue[-1][0]:
                self._queue.append([time,event])

            else:
                loc = 0
                while time > self.queue[loc][0]:
                    loc+=1

                self._queue.insert(loc, [time,event])

    def skip_to_next_event(self):
        if len(self.queue)==0:
            return

        data = self.queue[0]

        # If this is an action, do it. Otherwise it's an event, nothing is done. 
        if isinstance(data[1], MapAction):
            data[1].do()
            if data[1].recurring is not None:
                self.add_event(data[1], data[0]+data[1].recurring)

        self.clock.skip_to(data[0])
        self.queue.pop(0)

    def skip_to_time(self, time):
        if len(self.queue)!=0:
            while time<self.queue[0][0]:
                # moves time up to the next event, does the action (if there is one), and pops the event from the queue
                self.skip_to_next_event()

                if len(self.queue)==0:
                    break

        self.clock.skip_to(time)


    @property
    def queue(self):
        return(self._queue)

    @property 
    def parent(self):
        return(self._parent)

from enum import Enum 
from MultiHex.objects import Mobile, Entity 
from MultiHex.clock import Clock, Time

class mapActionItem(Enum):
    move = 1

class MapEvent:
    def __init__(self, kind,recurring=None, *args):
        if not isinstance(kind, mapActionItem):
            raise TypeError("Can only create action of type {}, not {}".format(mapActionItem, type(kind)))

        if recurring is not None:
            if not isinstance(recurring, Time):
                raise TypeError("If recurring, arg must be {}, not {}".format(Time, type(recurring)))
        self.recurringh = recurring


class MapAction(MapEvent):
    def __init__(self, kind,recurring=None, *args):
        MapEvent.__init__(self, kind, recurring, *args)
        
    def do(self):
        pass


class ActionManager:
    """
    This keeps track of upcoming events (and actions) and the time.
    It allows you to add new events and 
    """
    def __init__(self):
        self._queue = []

        self.clock = Clock()

    def add_event(self, event, time):
        if not isinstance(event, MapEvent):
            raise TypeError("Can only register {} type events, not {}".format(MapEvent, type(event)))
        if not isinstance(time, Time):
            raise TypeError("Expected {} for time, not {}.".format(Time, type(time)))

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
        data = self.queue[0]

        # If this is an action, do it. Otherwise it's an event, nothing is done. 
        if isinstance(data[1], MapAction):
            data[1].do()
            if data[1].recurring is not None:
                # create duplicate of the event. re-queue 
                pass

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
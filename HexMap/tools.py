


class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self, parent=None):
        pass
    def press(self,event):
        """
        Called when the mouse is pressed

        @param event 
        """
        pass
    def activate(self, event):
        """
        This is called when the mouse is released from a localized click. 

        @param event - location of release
        """
        pass
    def hold(self,event, step):
        """
        Called continuously while the mouse is held

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def move(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass



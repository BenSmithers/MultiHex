

class Entity:
    """
    Defines moving map entity that can (in theory) be placed on a map
    """
    def __init__(self, name):
        self.name = name

        self.speed  = 1. #miles/minute
        self.contains = {}


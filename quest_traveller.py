"""
Helper class to manage all transformation of the user when (s)he travels.

"""

class TravellerAPI:
    """API exposed to the actions."""
    def __init__(self):
        self.score = 0
        self.story = []
        self.new_location = None

    def goto(self, place):
        self.new_location = place

    def pop_location(self):
        location = self.new_location
        self.new_location = None
        return location

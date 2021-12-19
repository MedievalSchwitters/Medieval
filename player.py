# the real people that play the game multiple times
class Player:
    def __init__(self, name, initials, id):
        self.name = name
        self.initials = initials
        self.id = id + 1
        self.times_played = 0
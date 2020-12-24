class Anthropos:

    isAlive = False
    children = []

    def die(self):
        self.isAlive = False

    def beget(self, other):
        other.isAlive = True
        self.children.append(other)

    def __init__(self):
        self.isAlive = True
        self.children = []


#if this can make it to the desktop without a clone I'll call it for now



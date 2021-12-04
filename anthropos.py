class Anthropos:

    def slay(self):
        self.isAlive = False
        if self.isTheist:
            self.inAfterLife = True

    def beget(self, other):
        other.isAlive = True
        self.children.append(other)

    def __init__(self):
        self.isAlive = True
        self.children = []
        self.inAfterLife = False
        self.isTheist = True

    def commitApostasy(self):
        self.isTheist = False





dan = Anthropos()
dan.commitApostasy()
dan.slay()


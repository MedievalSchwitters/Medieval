class Anthropos:

    isAlive = False
    children = []

    def die(self, death_eon):
        self.isAlive = False
        self.eons_lived = death_eon - self.birth_eon

    def beget(self, other):
        if self.num_children < 2:
            other.isAlive = True
            if self.left_child is None:
                self.left_child = other
            else:
                self.right_child = other
            self.num_children += 1

    def __init__(self, name, birth_eon):
        self.isAlive = True
        self.left_child = None
        self.right_child = None
        self.num_children = 0
        self.name = name
        self.birth_eon = birth_eon
        self.eons_lived = 0





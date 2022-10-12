class Person:

    def __init__(self, name):
        self.name = name
        self.alive = False
        self.child_count = 0
        self.age = 0

    def log_in_out(self):
        if self.alive == True:
            self.alive = False
            self.child_count = 0
        elif self.alive == False:
            self.alive = True
        if self.alive:
            print(f'\n\n{self.name}, you have logged in as alive!')
        else:
            print(f'\n\n{self.name}, you are logged out as dead :(')
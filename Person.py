class Person:

    def __init__(self, name):
        self.name = name
        self.alive = False
        self.child_count = 0
        self.age = 0
        self.fertile = False

    def log_in_out(self):
        if self.alive:
            self.alive = False
            self.child_count = 0
            self.age = 0
            self.fertile = False
            print(f'\n\n{self.name}, you are logged out as dead :(')
        else:
            self.alive = True
            print(f'\n\n{self.name}, you have logged in as alive!')

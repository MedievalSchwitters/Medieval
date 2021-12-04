import random

# edit before game
player_list = 'Kelsey,Kaley,Connor,Dan,Tom,Rae,Alix,Molly,Taya, Kori, Carter, Rae, Ella'.split(',')

# should be able to leave the rest alone
people_list = []
fertile_people_list = []


class Person:

    def __init__(self, name):
        self.name = name
        self.alive = False
        self.child_count = 0

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

#Makes the people instances from the list of players
for x in player_list:
    working = Person("wow")
    working.name = x
    people_list.append(working)

# intro
i = 0
print("\nHere's everyone's numbers:")
while i < len(player_list):
    print(f'{str(i + 1)}: {player_list[i]}')
    i += 1
x = input('\nHit enter to get started\n')

#main code
continue_ = True
while True:
    while continue_:
        x = int(input('Enter your number and hit enter to sign in/out as alive/dead:\n\n'))
        try:
            if x != 0:
                p = people_list[int(x - 1)]
                p.log_in_out()
                print('---------------------------')
            else:
                continue_ = not continue_
        except:
            print("Don't just hit enter, silly. Try again:")

    print("\nHere's a list of living, fertile players:")
    fertile_people_list = []
    for x in people_list:
        if x.alive and x.child_count < 2:
            fertile_people_list.append(x)
    j = 1
    random.shuffle(fertile_people_list)
    for x in fertile_people_list:
        print(f'\t{j}: {x.name}')
        j += 1

    x = int(input('\nHow many had kids?\n'))
    print('\nOk, the following people are entered as having had a kid:')
    if x>len(fertile_people_list):
        x=len(fertile_people_list)
    for i in range(0, x):
        fertile_people_list[i].child_count += 1
        print('\t', fertile_people_list[i].name)
    continue_ = True
    print('---------------------------------\n')

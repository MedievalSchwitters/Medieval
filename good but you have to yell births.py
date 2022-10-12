import random, json
from Person import Person

f = open('medieval_config.json')
config = json.load(f)

with open('player_list.csv', 'r') as player_list:
    player_list = player_list.read()
    player_list = player_list.split(',')

# should be able to leave the rest alone
people_list = []
fertile_people_list = []

# Makes the people instances from the list of players
for name in player_list:
    people_list.append(Person(name))

# intro
i = 0
print("\nHere's everyone's numbers:")
while i < len(player_list):
    print(f'{str(i + 1)}: {player_list[i]}')
    i += 1

input('\nHit enter to get started\n')

# main code
while True:
    while True:
        x = int(input('Enter your number and hit enter to sign in/out as alive/dead:\n\n'))
        try:
            if x != 0:
                people_list[int(x - 1)].log_in_out()
                print('---------------------------')
            else:
                break
        except:
            print("Don't just hit enter, silly. Try again:")
    print("\nHere's a list of living players by age:\n")
    for person in people_list:
        if person.alive:
            print(f"{person.name: <8}{person.age: >8}")
            person.age += 1

    print("----------------------------\nHere's a list of living, fertile players:")
    fertile_people_list = []
    for x in people_list:
        if x.alive and x.child_count <= config['max_num_offspring']:
            fertile_people_list.append(x)
    j = 1
    random.shuffle(fertile_people_list)
    for x in fertile_people_list:
        print(f'\t{j}: {x.name}')
        j += 1

    num_begetter = int(input('\nHow many had kids?\n'))
    print('\nOk, the following people are entered as having had a kid:')
    if num_begetter > len(fertile_people_list):
        num_begetter = len(fertile_people_list)
    for i in range(0, num_begetter):
        fertile_people_list[i].child_count += 1
        print('\t', fertile_people_list[i].name)
    print('\n-----------------------------------\n')

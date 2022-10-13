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


def update_fertility():
    for person in people_list:
        person.fertile = (person.alive and
                          person.age >= config["adulthood"] and
                          person.child_count < config["max_num_offspring"])


def update_ages():
    for person in people_list:
        if person.alive:
            person.age += 1


if __name__ == '__main__':

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
            user_input = input('Type your number and hit enter to die (or be created ex nihilo, if not already alive):\n\n')
            try:
                x = int(user_input)
                if x != 0:
                    people_list[x - 1].log_in_out()
                    print('---------------------------')
                else:
                    break
            except:
                print(f"\"{user_input}\" ain't no number I ever heard of. ")
        print("\nLiving Players Names And Ages:\n")
        for person in people_list:
            if person.alive:
                print(f"{person.name: <8}{person.age: >8}")
        # to be alive is a necessary condition for being fertile
        print("----------------------------\nFertile Players:\n")
        update_fertility()
        fertile_people_list = []
        for person in people_list:
            if person.fertile:
                print(person.name)
                fertile_people_list.append(person)
        print("----------------------------")
        random.shuffle(fertile_people_list)
        # here we keep popping until Heaven/Sheol/Hades is empty of players or all fertile people have begotten
        # ho Theos presses 0 in the prior case
        out_of_potential_parents = True
        while len(fertile_people_list) != 0:
            user_input = input(
                'Type your number and hit enter to be born\n')
            try:
                x = int(user_input)
                if x != 0:
                    people_list[x - 1].log_in_out()
                    parent = fertile_people_list.pop()
                    print(f"{people_list[x - 1].name}, your progenitor is {parent.name}")
                    print('---------------------------')
                else:
                    out_of_potential_parents = False
                    break
            except:
                print(f"\"{user_input}\" ain't no number I ever heard of. ")
        if out_of_potential_parents:
            print("no more potential progenitors")
        print("----------------------------")
        update_ages()

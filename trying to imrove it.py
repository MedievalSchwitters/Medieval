import random  # random.shuffle(your_list)

# edit before game
player_name_list = 'Kelsey,Kaley,Connor,Dan,Tom,Rae,Alix,Molly,Taya,Kori,Carter,Rae,Ella,Trent,Aubrey,'.split(',')
# pick how many turns are in each life stage
childhood = 2
adulthood = 4
# should be able to leave the rest alone! :)

player_list = []
people_list = []
living_people_list = []
living_children_list = []  # todo these 3
living_adults_list = []
living_elders_list = []
# should be a dictionary
string_of_living = []
# wait_list for fertile players waiting to having a baby
baby_wait_list = []
next_parent_in_line_to_have_a_baby = None
def tys_func():
    print("dis tys func")

# todo make it so people die at certain age and have a childhood in which they cannot reproduce
# and you can enter peoples initials to sign them out


# Players

# the real people that play the game multiple times
class Player:
    def __init__(self, name, initials, id):
        self.name = name
        self.initials = initials
        self.id = id + 1
        self.times_played = 0


# A person is just one time that a player played. A player will make a new person every time they play.
class Person:

    def __init__(self, player, life_number_for_player, parent):
        self.life_number_for_player = life_number_for_player
        self.player = player
        self.parent = parent
        try:
            parent.children.append(self)
        except AttributeError:
            if date != 1:
                print(f'ERROR THEY DIDN\'T GET A PARENT')
        self.birthday = date
        self.alive = True
        self.age = 0
        self.children = []
        self.date_of_death = None
        if parent is not None:
            print(
                f'\n\nWelcome to the world, {self.player.name}! Go tell {self.parent.player.name} that you\'re their kid!\n')

    def die(self):
        self.alive = False
        living_people_list.remove(self)
        self.date_of_death = date
        self.player.times_played += 1
        print(
            f'\nHAHA\n{self.player.name} DIED\nYour stats for life number {self.life_number_for_player}:\nAge:\n{self.age}\nParent:\n{self.parent}\nChildren:\n')
        for child in self.children:
            print(f'{child.player.name}\n')
        total_living_descendants = 0
        try:
            total_living_descendants = len(self.get_descendants())
        except TypeError:
            total_living_descendants = 0
        print(f'How IMPRESSIVE you are, aka Total Descendants at time of death:\n{total_living_descendants}')
        living_descendants = self.get_descendants()
        try:
            for descendant in living_descendants:
                try:
                    if not descendant.alive:
                        living_descendants.remove(descendant)
                except AttributeError:
                    pass
        except TypeError:
            living_descendants = 0
        try:
            living_descendants_count = len(living_descendants)
        except TypeError:
            living_descendants_count = 0
        print(f'({living_descendants_count} of which are alive\n)')
        print(f'_____\n')

    def get_descendants(self):
        descendant_list = []  # can counter be in method? todo

        # if someone doesn't have children, they don't have descendants
        if len(self.children) == 0:
            return None

        # if someone has no grandchildren, their only descendants are their own children
        has_grandchildren = False
        for child in self.children:
            if len(child.children) > 0:
                has_grandchildren = True
        if not has_grandchildren:
            for child in self.children:
                descendant_list.append(child)

        # if someone has grandchildren, try recursion to figure out how many descendants they have
        for child in self.children:
            descendant_list.append(child.get_descendants())

        return descendant_list


def refresh_string_of_living_people():
    global string_of_living
    string_of_living = []
    for x in living_people_list:
        string_of_living.append(str(x.player.name))


def make_new_baby_wait_list():
    global next_parent_in_line_to_have_a_baby
    global baby_wait_list
    baby_wait_list = []

    # graduate old children into adulthood
    for x in living_children_list:
        if x.age > childhood:
            living_adults_list.append(x)
            for y in living_children_list:
                if x.name is y.name:
                    living_children_list.remove(x)

    # graduate adults with 2 children into elderhood
    for x in living_adults_list:
        if len(x.children) > 1:
            living_elders_list.append(x)
            for y in living_adults_list:
                if x.name is y.name:
                    living_adults_list.remove(x)

    # create que for adults to have babies
    for x in living_adults_list:
        baby_wait_list.append(x)

    # randomize
    random.shuffle(baby_wait_list)
    if len(baby_wait_list) > 0:
        next_parent_in_line_to_have_a_baby = baby_wait_list[0]


def pop_parent_off_of_baby_wait_list(baby_they_are_having):
    global next_parent_in_line_to_have_a_baby
    global baby_wait_list
    try:
        next_parent_in_line_to_have_a_baby.children.append(baby_they_are_having)
        baby_wait_list.remove(baby_wait_list[-1])
    except:
        pass


def add_to_book_of_life(baby):
    living_people_list.append(baby)
    people_list.append(baby)
    living_children_list.append(baby)


def print_family_tree():
    print('not yet')


# Uses the list of player names to make a list of player objects
for x in player_name_list:  # may need to be a while loop to get 'id's
    y = Player(x, x[0:2:1], player_name_list.index(x))
    player_list.append(y)

# Makes the people instances from the list of players
# PROP OBSOLETE DO TO ABOVE FUNCTION
# for name in player_name_list:
#     name_being_added_to_people_list = Person("meh" player, life_number_for_player, name, parent):)
#     name_being_added_to_people_list.name = person
#     people_list.append(name_being_added_to_people_list)

# intro
print("\nHere's everyone's numbers:")
i = 0
while i < len(player_name_list) - 1:
    print(f'{str(i + 1)}: {player_name_list[i]}')
    i += 1

# main code
date = 1
while True:
    while True:
        entered_id_or_initials = (input('\nEnter your number and hit enter to sign in/out as alive/dead:\n\n'))
        entered_id = None
        entered_initials = None

        # did they enter letters?
        try:
            entered_id = int(entered_id_or_initials)
        except ValueError:
            entered_initials = entered_id_or_initials[0:2:1]

        # If the user entered their initials, convert to id
        if entered_initials is not None:
            for x in player_list:
                if x.initials.lower() == entered_initials.lower():
                    entered_id = x.id

        if entered_id is not None:
            if entered_id > 0:

                # find out which player is trying to sign in/out
                player_signing_in_or_out = None
                for x in player_list:
                    if x.id == entered_id:
                        player_signing_in_or_out = x
                        break

                # if alive, die
                refresh_string_of_living_people()
                if player_signing_in_or_out.name in string_of_living:  # there's gotta be a better way... todo
                    for person in living_people_list:
                        if person.player.name == player_signing_in_or_out.name:
                            person.die()

                # else dead, so be birthed!
                else:
                    # find out if there are are no fertile people who can birth the player back into the game
                    if len(baby_wait_list) == 0:
                        if len(living_people_list) == 0:
                            print(
                                f'\nWelcome, {player_signing_in_or_out.name}. Looks like you\'ll be the Adam/Eve of this world! No pressure. Oh, and don\'t let your kids fight like Cain and Abel...\n')
                            baby = Person(player_signing_in_or_out, 1, None)
                            add_to_book_of_life(baby)
                            break
                        # if there are other people but no one ready to have a baby, then they need to wait!
                        else:
                            print(
                                f'\n\nSorry, {player_signing_in_or_out.name}. Looks like there\'re no available parents for you yet. Back to Heaven, now!\n')

                    else:
                        # find out what life number the player will be on when born this time
                        name_of_guy_that_is_being_birthed = player_signing_in_or_out.name
                        life_number_for_player_that_will_soon_be_born = None
                        for x in player_list:
                            if x.name == name_of_guy_that_is_being_birthed:
                                life_number_for_player_that_will_soon_be_born = x.times_played + 1
                                baby = Person(x, life_number_for_player_that_will_soon_be_born,
                                              next_parent_in_line_to_have_a_baby)
                                add_to_book_of_life(baby)
                                try:
                                    pop_parent_off_of_baby_wait_list(baby)
                                except NameError:
                                    print(f'you did not have a parent')
                                if len(baby_wait_list) == 0:
                                    print(f'\nNO MORE BABIES CAN BE BORN THIS TURN\n')
                                break
            else:
                break  # because I must be trying to end turn manually

    # Next turn because I entered 0
    if entered_id > -1:
        make_new_baby_wait_list()
        print(
            f'TURN {date + 1}:\nStats:\n\t{len(living_people_list)} -> Pop\n\t{len(baby_wait_list)} -> Fertile pop\n\t{len(people_list)} -> Total people ever lived\n')  # todo add stats here: pop, total people ever lived, total fertile players
        date += 1
    else:
        x = input(f'What turns would you like printed?')
        print_family_tree()

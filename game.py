import random  # random.shuffle(your_list)

from person import Person
from player import Player


class Game:

    def __init__(self, player_name_list, childhood, lifespan):
        self.player_name_list = player_name_list
        self.childhood = childhood
        self.lifespan = lifespan
        self.player_list = []
        self.people_list = []
        self.living_people_list = []
        self.living_children_list = []
        self.living_adults_list = []
        self.living_elders_list = []
        self.baby_wait_list = []
        # should be a dictionary
        self.string_of_living = []
        # wait_list for fertile players waiting to having a baby
        self.baby_wait_list = []
        self.next_parent_in_line_to_have_a_baby = None
        self.date = 0

    # todo and you can enter peoples initials to sign them out

    def refresh_string_of_living_people(self):
        string_of_living = []
        for x in self.living_people_list:
            string_of_living.append(str(x.player.name))

    def make_new_baby_wait_list(self):
        # should be able to delete this block
        # global next_parent_in_line_to_have_a_baby
        # global baby_wait_list
        self.baby_wait_list = []

        # todo dan help ony does one child
        # graduate old children into adulthood
        for x in self.living_children_list:
            if x.age >= self.childhood:
                self.living_adults_list.append(x)
                self.living_children_list.remove(x)

        # graduate adults with 2 children into elderhood
        for x in self.living_adults_list:
            if len(x.children) > 1:
                self.living_elders_list.append(x)
                self.living_adults_list.remove(x)

        # create que for adults to have babies
        for x in self.living_adults_list:
            self.baby_wait_list.append(x)

        # randomize
        random.shuffle(self.baby_wait_list)
        if len(self.baby_wait_list) > 0:
            next_parent_in_line_to_have_a_baby = self.baby_wait_list[0]

    def pop_parent_off_of_baby_wait_list(self, parent_which_just_had_their_baby):
        # global next_parent_in_line_to_have_a_baby
        # global baby_wait_list
        try:
            next_parent_in_line_to_have_a_baby = self.baby_wait_list[1]
            try:
                self.baby_wait_list.remove(parent_which_just_had_their_baby)
            except ValueError:
                pass
        except IndexError or ValueError:
            try:
                if len(self.baby_wait_list) == 1:
                    self.baby_wait_list.remove(parent_which_just_had_their_baby)
            except ValueError:
                pass

    def add_to_book_of_life(self, baby):
        self.living_people_list.append(baby)
        self.people_list.append(baby)
        self.living_children_list.append(baby)

    def print_family_tree(self):
        print('not yet')

    def start_game(self):
        # Uses the list of player names to make a list of player objects
        for x in self.player_name_list:  # may need to be a while loop to get 'id's
            y = Player(x, x[0:2:1], self.player_name_list.index(x))
            self.player_list.append(y)

        # Makes the people instances from the list of players
        # PROP OBSOLETE DO TO ABOVE FUNCTION
        # for name in player_name_list:
        #     name_being_added_to_people_list = Person("meh" player, life_number_for_player, name, parent):)
        #     name_being_added_to_people_list.name = person
        #     people_list.append(name_being_added_to_people_list)

        # intro
        print("\nHere's everyone's numbers:")
        i = 0
        while i < len(self.player_name_list) - 1:
            print(f'{str(i + 1)}: {self.player_name_list[i]}')
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
                    for x in self.player_list:
                        if x.initials.lower() == entered_initials.lower():
                            entered_id = x.id

                if entered_id is not None:
                    if entered_id > 0:

                        # find out which player is trying to sign in/out
                        player_signing_in_or_out = None
                        for x in self.player_list:
                            if x.id == entered_id:
                                player_signing_in_or_out = x
                                break

                        # if alive, die
                        self.refresh_string_of_living_people()
                        if player_signing_in_or_out.name in self.string_of_living:  # there's gotta be a better way... todo
                            for person in self.living_people_list:
                                if person.player.name == player_signing_in_or_out.name:
                                    person.die()

                        # else dead, so be birthed!
                        else:
                            # find out if there are are no fertile people who can birth the player back into the game
                            if len(self.baby_wait_list) == 0:
                                if len(self.living_people_list) == 0:
                                    print(
                                        f'\nWelcome, {player_signing_in_or_out.name}. Looks like you\'ll be the Adam/Eve of this world! No pressure. Oh, and don\'t let your kids fight like Cain and Abel...\n')
                                    baby = Person(player_signing_in_or_out, 1, None, self)

                                    break
                                # if there are other people but no one ready to have a baby, then they need to wait!
                                else:
                                    print(
                                        f'\n\nSorry, {player_signing_in_or_out.name}. Looks like there\'re no available parents for you yet. Back to Heaven, now!\n')

                            else:
                                # find out what life number the player will be on when born this time
                                name_of_guy_that_is_being_birthed = player_signing_in_or_out.name
                                life_number_for_player_that_will_soon_be_born = None
                                for x in self.player_list:
                                    if x.name == name_of_guy_that_is_being_birthed:
                                        life_number_for_player_that_will_soon_be_born = x.times_played + 1
                                        baby = Person(x, life_number_for_player_that_will_soon_be_born,
                                                      self.next_parent_in_line_to_have_a_baby)
                                        try:
                                            self.pop_parent_off_of_baby_wait_list(baby)
                                        except NameError:
                                            print(f'you did not have a parent')
                                        if len(self.baby_wait_list) == 0:
                                            print(f'\nNO MORE BABIES CAN BE BORN THIS TURN\n')
                                        break
                    else:
                        break  # because I must be trying to end turn manually

            # Next turn because I entered 0
            if entered_id > -1:
                # age people
                for x in self.living_people_list:
                    x.age += 1
                # kill old people
                for x in self.living_people_list:
                    if x.age > self.lifespan:
                        x.die()
                        x = input(f'\nHit enter:\n')
                self.make_new_baby_wait_list()
                print(
                    f'TURN {date + 1}:\nStats:\n\t{len(self.living_people_list)} -> Pop\n\t{len(self.baby_wait_list)} -> Fertile pop\n\t{len(self.people_list)} -> Total people ever lived\n')  # todo add stats here: pop, total people ever lived, total fertile players
                date += 1
            else:
                x = input(f'What turns would you like printed? not implemented')
                self.print_family_tree()

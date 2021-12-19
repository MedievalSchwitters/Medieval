# A person is just one time that a player played. A player will make a new person every time they play.
class Person:

    def __init__(self, player, life_number_for_player, parent):
        self.life_number_for_player = life_number_for_player
        self.player = player
        self.parent = parent
        self.birthday = date
        self.alive = True
        self.age = 0
        self.children = []
        self.date_of_death = None
        add_to_book_of_life(self)
        pop_parent_off_of_baby_wait_list(parent)
        try:
            parent.children.append(self)
        except AttributeError:
            if date != 1:
                print(f'ERROR THEY DIDN\'T GET A PARENT')
        if parent is not None:
            print(
                f'\n\nWelcome to the world, {self.player.name}! Go tell {self.parent.player.name} that you\'re their kid!\n')

    def die(self):
        self.alive = False
        living_people_list.remove(self)
        self.date_of_death = date
        self.player.times_played += 1
        print(
            f'\nHAHA\n{self.player.name} DIED\nYour stats for life number {self.life_number_for_player}:\n\t{self.age} <-Age\n\t{self.parent.player.name} <-Parent\n\tChildren:\n')
        for child in self.children:
            print(f'\n\t{child.player.name}')
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
        print(f'\n')

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
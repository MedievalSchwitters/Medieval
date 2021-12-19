# edit before game
from game import Game

player_name_list = 'Kelsey,Kaley,Connor,Dan,Tom,Rae,Alix,Molly,Taya,Kori,Carter,Rae,Ella,Trent,Aubrey,'.split(',')
# pick how many turns are in each life stage
childhood = 0  # turns which young people cannot have children
lifespan = 4  # total turns allowed until a person dies of old age

x = Game(player_name_list, childhood, lifespan)
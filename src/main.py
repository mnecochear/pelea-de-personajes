""" This module simulates a battle between two teams of five superheroes each. """

import sys
import core
import teams

all_heroes = core.get_heroes()
max_index = len(all_heroes) - 1

if max_index < 9:
    sys.exit(f'At least 10 heroes required to start a Battle, only {max_index + 1} found.')

blue_team_indexes = core.get_hero_indexes(max_index, [])
red_team_indexes = core.get_hero_indexes(max_index, blue_team_indexes)

blue_team = teams.Team(all_heroes, blue_team_indexes)
# print(list(map(lambda h: h.attacks, blue_team.heroes)))
# red_team = teams.Team(all_heroes, red_team_indexes)

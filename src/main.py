""" This module simulates a battle between two teams of five superheroes each. """

import sys
import teams
import battles

all_heroes = teams.get_heroes()
max_index = len(all_heroes) - 1

if max_index < 9:
    sys.exit(f'Not enough superheroes found to start a battle ({max_index + 1}/10 minimum).')

blue_team_indexes = teams.get_hero_indexes(max_index, [])
red_team_indexes = teams.get_hero_indexes(max_index, blue_team_indexes)

blue_team = teams.Team(all_heroes, blue_team_indexes, 'Blue')
red_team = teams.Team(all_heroes, red_team_indexes, 'Red')

battle = battles.Battle(blue_team, red_team)
battle.winner = battle.simulate()

""" This module contains classes required to represent & simulate a battle. """

import random
import teams

class Turn:
    """ Represents a turn within a fight. """

    def __init__(self, attacker: teams.Hero, defender: teams.Hero, turn_number):
        self.number = turn_number
        self.attacker = attacker
        self.defender = defender
        self.hp_before = defender.hp
        self.attack_name = attacker.select_attack()
        self.damage_dealt = self.__process_attack()
        self.hp_after = defender.hp

    def __process_attack(self):
        """ Returns the damage dealt to the Health Points of the defender. """
        attack_damage = self.attacker.attacks[self.attack_name]
        damage_dealt = attack_damage if self.hp_before - attack_damage >= 0 else self.hp_before
        self.defender.hp -= damage_dealt
        return damage_dealt

class Fight:
    """ Represents a fight between two superheroes. """

    def __init__(self, opponents):
        self.opponents = opponents
        self.turns = []

    def __create_turn(self, turn_number, defender_index):
        """ Appends a new turn to the fight. """
        attacker = self.opponents[0 if defender_index else 1]
        defender = self.opponents[defender_index]
        self.turns.append(Turn(attacker, defender, turn_number))

    def simulate(self):
        """ Creates the turns of a fight and returns its winner. """
        turn_count = 1
        defender_index = random.randint(0, 1)  # each fighter has a 50% chance of attacking first
        self.__create_turn(turn_count, defender_index)
        while self.opponents[defender_index].hp > 0:
            turn_count += 1
            defender_index = 0 if defender_index else 1
            self.__create_turn(turn_count, defender_index)
        return self.get_winner()

    def get_winner(self) -> teams.Hero:
        """ Returns the winner of the fight. """
        return self.turns[-1].attacker

    def get_loser(self) -> teams.Hero:
        """ Returns the loser of the fight. """
        return self.turns[-1].defender

class Battle:
    """ Represents a battle between two teams of 5 superheroes each. """

    def __init__(self, blue_team, red_team):
        self.blue_team = blue_team
        self.red_team = red_team
        self.fights = self.__create_fights()

    def __create_fights(self):
        """ Creates the battle's fights. """
        opponentes = list(zip(self.blue_team.heroes, self.red_team.heroes))
        return list(map(Fight, opponentes))

    def simulate(self):
        """ Simulates the battle's fights and returns the winning team. """
        blue_winners = list(map(lambda f: f.simulate() in self.blue_team.heroes, self.fights))
        if blue_winners.count(True) > 2:
            return self.blue_team.name
        return self.red_team.name

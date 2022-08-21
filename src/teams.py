""" This module contains the classes necessary to represent a team. """

import random
import math
import core

class Hero:
    """ Represents a superheroe. """

    ATTACK_NAMES = ['Mental', 'Strong', 'Fast']

    def __init__(self, hero_info, team_alignment):
        self.id = hero_info["id"]
        self.name = hero_info["name"]
        self.alignment = core.cast_alignment(hero_info["biography"]["alignment"])
        self.fb = self.calculate_fb(team_alignment)

        self.intelligence = self.calculate_stat(hero_info["powerstats"]["intelligence"])
        self.strength = self.calculate_stat(hero_info["powerstats"]["strength"])
        self.speed = self.calculate_stat(hero_info["powerstats"]["speed"])
        self.durability = self.calculate_stat(hero_info["powerstats"]["durability"])
        self.power = self.calculate_stat(hero_info["powerstats"]["power"])
        self.combat = self.calculate_stat(hero_info["powerstats"]["combat"])
        self.hp = self.calculate_hp()

        self.attacks = {}
        list(map(self.calculate_attack_damage, self.ATTACK_NAMES))

    def calculate_fb(self, team_alignment):
        """ Calculates the Filiation Coefficient. """
        fb_base = 1 + random.randint(0, 9)
        fb_modifier = 1 if self.alignment == team_alignment else -1
        return pow(fb_base, fb_modifier)

    def calculate_stat(self, base_stat):
        """ Calculates the real value of a power stat. """
        actual_stamina = random.randint(0, 10)
        real_stat = (2 * base_stat + actual_stamina) * self.fb / 1.1
        return math.floor(real_stat)

    def calculate_hp(self):
        """ Calculates Health Points. """
        base_hp = (self.strength * 0.8 + self.durability * 0.7 + self.power) / 2
        actual_stamina = random.randint(0, 10)
        as_modifier = 1 + actual_stamina / 10
        return math.floor(base_hp * as_modifier) + 100

    def calculate_attack_damage(self, attack_name):
        """ Appends an attack with its damage to the Hero's attacks dictionary. """
        match attack_name:
            case 'Mental':
                base_damage = self.intelligence * 0.7 + self.speed * 0.2 + self.combat * 0.1
            case 'Strong':
                base_damage = self.strength * 0.6 + self.power * 0.2 + self.combat * 0.2
            case 'Fast':
                base_damage = self.speed * 0.55 + self.durability * 0.25 + self.strength * 0.2
        self.attacks[attack_name] = math.ceil(base_damage * self.fb)

    def select_attack(self):
        """ Randomly selects an attack name. """
        return random.choice(self.ATTACK_NAMES)

class Team:
    """ Represents a team of five superheroes. """

    def __init__(self, all_heroes, hero_indexes):
        self.alignment = self.get_team_alignment(all_heroes, hero_indexes)
        self.heroes = list(map(lambda i: self.create_hero(all_heroes[i]), hero_indexes))

    def create_hero(self, hero_info):
        """ Creates a Hero considering its team alignment. """
        return Hero(hero_info, self.alignment)

    def get_team_alignment(self, all_heroes, hero_indexes):
        """ Returns the team alignment. """
        hero_alignments = list(map(lambda i: core.cast_alignment(all_heroes[i]["biography"]["alignment"]), hero_indexes))
        return hero_alignments.count(True) > 2

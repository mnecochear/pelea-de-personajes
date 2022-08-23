""" This module contains the classes necessary to represent a team. """

import os
import random
import math
import requests

class Hero:
    """ Represents a superheroe. """

    ATTACK_NAMES = ['Mental', 'Strong', 'Fast']
    DEFAULT_IMAGE = 'thumbnails/placeholder.jpg'

    def __init__(self, hero_info, team_alignment):
        self.name = hero_info["name"]
        self.image = self.__get_image_path(hero_info["images"]["sm"])
        self.alignment = cast_alignment(hero_info["biography"]["alignment"])
        self.fb = self.__calculate_fb(team_alignment)

        self.intelligence = self.__calculate_stat(hero_info["powerstats"]["intelligence"])
        self.strength = self.__calculate_stat(hero_info["powerstats"]["strength"])
        self.speed = self.__calculate_stat(hero_info["powerstats"]["speed"])
        self.durability = self.__calculate_stat(hero_info["powerstats"]["durability"])
        self.power = self.__calculate_stat(hero_info["powerstats"]["power"])
        self.combat = self.__calculate_stat(hero_info["powerstats"]["combat"])
        self.hp = self.__calculate_hp()
        self.base_hp = self.hp

        self.attacks = {}
        list(map(self.__calculate_attack_damage, self.ATTACK_NAMES))

    def __calculate_fb(self, team_alignment):
        """ Calculates the Filiation Coefficient. """
        fb_base = 1 + random.randint(0, 9)
        fb_modifier = 1 if self.alignment == team_alignment else -1
        return pow(fb_base, fb_modifier)

    def __calculate_stat(self, base_stat):
        """ Calculates the real value of a power stat. """
        actual_stamina = random.randint(0, 10)
        real_stat = (2 * base_stat + actual_stamina) * self.fb / 1.1
        return math.floor(real_stat)

    def __calculate_hp(self):
        """ Calculates Health Points. """
        base_hp = (self.strength * 0.8 + self.durability * 0.7 + self.power) / 2
        actual_stamina = random.randint(0, 10)
        as_modifier = 1 + actual_stamina / 10
        return math.floor(base_hp * as_modifier) + 100

    def __calculate_attack_damage(self, attack_name):
        """ Appends an attack with its damage to the Hero's attacks dictionary. """
        match attack_name:
            case 'Mental':
                base_damage = self.intelligence * 0.7 + self.speed * 0.2 + self.combat * 0.1
            case 'Strong':
                base_damage = self.strength * 0.6 + self.power * 0.2 + self.combat * 0.2
            case 'Fast':
                base_damage = self.speed * 0.55 + self.durability * 0.25 + self.strength * 0.2
        self.attacks[attack_name] = math.ceil(base_damage * self.fb)

    def __get_image_path(self, url):
        """ Returns local relative path to image located at url. """
        placeholder = self.DEFAULT_IMAGE
        try:
            data = requests.get(url)
            if data.status_code == 200:
                image_ext = os.path.splitext(url)[-1]
                image_path = f'thumbnails/{self.name}{image_ext}'
                with open(image_path, 'wb') as stream:
                    stream.write(data.content)
                return image_path
            return placeholder
        except requests.exceptions.RequestException as err:
            print(f'Error occured while retrieving {self.name}\'s image.\nMessage: {err}')
            return placeholder

    def select_attack(self):
        """ Randomly selects an attack name. """
        return random.choice(self.ATTACK_NAMES)

class Team:
    """ Represents a team of five superheroes. """

    def __init__(self, all_heroes, hero_indexes, name, color):
        self.name = name
        self.color = color
        self.alignment = self.__get_team_alignment(all_heroes, hero_indexes)
        self.heroes = list(map(lambda i: self.__create_hero(all_heroes[i]), hero_indexes))

    def __create_hero(self, hero_info):
        """ Creates a Hero considering its team alignment. """
        return Hero(hero_info, self.alignment)

    def __get_team_alignment(self, all_heroes, hero_indexes):
        """ Returns the team alignment. """
        hero_alignments = list(map(lambda i: cast_alignment(all_heroes[i]["biography"]["alignment"]), hero_indexes))
        return hero_alignments.count(True) > 2

def cast_alignment(alignment_text):
    """ Casts alignment from string to bool. """
    return alignment_text == "good"

def get_heroes():
    """ Returns all heroes from Superheroes API. """
    endpoint = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'
    try:
        response = requests.get(endpoint)
        return response.json()
    except requests.exceptions.RequestException as err:
        message = 'Error occured while retrieving superheroes from API'
        raise SystemExit(message) from err

def get_hero_indexes(max_index, used_indexes):
    """ Generates a list of five hero indexes. """
    hero_indexes = []
    for _ in range(5):
        hero_index = random.randint(0, max_index)
        while hero_index in used_indexes:
            hero_index = random.randint(0, max_index)
        hero_indexes.append(hero_index)
    return hero_indexes

def delete_image(image_path):
    """ Deletes the image located at image_path """
    if os.path.exists(image_path):
        os.remove(image_path)

""" This module contains various neccesary methods that don't fit elsewhere. """

import random
import requests

@staticmethod
def cast_alignment(alignment_text):
    """ Casts alignment from string to bool. """
    return alignment_text == "good"

@staticmethod
def get_heroes():
    """ Returns all heroes from Superheroes API. """
    endpoint = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'
    try:
        response = requests.get(endpoint)
        return response.json()
    except requests.exceptions.RequestException as err:
        message = f'Error while getting superheroes from API.\nMessage: {err}'
        raise SystemExit(message) from err

@staticmethod
def get_hero_indexes(max_index, used_indexes):
    """ Generates a list of five hero indexes. """
    hero_indexes = []
    for _ in range(5):
        hero_index = random.randint(0, max_index)
        while hero_index in used_indexes:
            hero_index = random.randint(0, max_index)
        hero_indexes.append(hero_index)
    return hero_indexes
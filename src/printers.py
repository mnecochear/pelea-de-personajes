""" This module contains methods to print battles to stdout. """

from math import floor
import climage
import teams
import battles

BLOCK_WIDTH = 33
SEPARATOR = '-' * BLOCK_WIDTH
FILLER = ' ' * BLOCK_WIDTH

def print_turn(turn: battles.Turn, left_hero):
    """ Prints a turn. """
    attacker_text = create_attack_block(turn.attack_name, turn.damage_dealt)
    defender_text = create_hp_block(turn.hp_after)
    if left_hero == turn.attacker:
        left = attacker_text
        right = defender_text
    else:
        left = defender_text
        right = attacker_text
    info = create_label_block(f'TURN #{turn.number}')
    print(left + info + right)
    print(SEPARATOR * 3)

def print_fight(fight: battles.Fight, title, blue_heroes):
    """ Prints a fight. """
    blue_hero = fight.opponents[0]
    red_hero = fight.opponents[1]

    image_height = len(get_image_lines(blue_hero.image))
    header_block = create_header_block(blue_hero, red_hero, image_height)

    print(create_label_block(paint_label(title, 'yellow'), 9, True))
    print('\n'.join(header_block))
    print(SEPARATOR * 3)

    list(map(lambda t: print_turn(t, blue_hero), fight.turns))

    winner_color = 'blue' if fight.winner in blue_heroes else 'red'
    winner_label = f'{paint_label(fight.winner.name, winner_color)} wins!'

    print(create_label_block(winner_label, 9, True))
    print(SEPARATOR * 3)

def print_battle(battle: battles.Battle):
    """ Prints a battle. """
    overview_label = paint_label('BATTLE OVERVIEW', 'underline')

    print(SEPARATOR * 3)
    print(create_label_block(overview_label, 8, True))

    blue_team_block = create_team_block(battle.blue_team)
    red_team_block = create_team_block(battle.red_team)
    vs_block = create_middle_block('VS', len(battle.blue_team.heroes))
    middle_block = [FILLER] * 2 + vs_block
    middle_block[1] = SEPARATOR

    zipped = list(zip(blue_team_block, middle_block, red_team_block))
    header_block = list(map(''.join, list(zipped)))

    print('\n'.join(header_block))
    print(SEPARATOR * 3)

    for i, fight in enumerate(battle.fights):
        print_fight(fight, f'FIGHT #{i+1}', battle.blue_team.heroes)

    result_title = paint_label('BATTLE RESULT', 'underline')
    winner_label = f'{paint_label(battle.winner.name, battle.winner.color)} wins!'
    blue_wins_label = paint_label(str(battle.blue_wins), battle.blue_team.color)
    red_wins_label = paint_label(str(battle.red_wins), battle.red_team.color)
    result_label = f'{blue_wins_label} \U00002694 {red_wins_label}'

    print(create_label_block(result_title, 8, True))
    print(create_label_block(result_label, 18, True))
    print(create_label_block(winner_label, 9, True))
    print(SEPARATOR * 3)

def get_image_lines(path):
    """ Returns a list with the lines of an image. """
    image = climage.convert(path, is_unicode=True, is_truecolor=True, is_256color=False, width=BLOCK_WIDTH)
    return image.splitlines()

def paint_label(label, color):
    """ Returns a colored string. """
    match color:
        case 'red':
            label = '\033[91m' + label
        case 'blue':
            label = '\033[94m' + label
        case 'yellow':
            label = '\033[93m' + label
        case 'underline':
            label = '\033[4m' + label
        case _:
            return label
    return label + '\033[0m'

def create_label_block(label, offset = 0, fill = False):
    """ Returns a string used to print a label. """
    label_width = len(label) - offset
    left_filler = ' ' * floor((BLOCK_WIDTH - label_width) / 2)
    right_filler = ' ' * (BLOCK_WIDTH - len(left_filler) - label_width)
    label_block = left_filler + label + right_filler
    if fill:
        return FILLER + label_block + FILLER
    return label_block

def create_name_block(name, color = ''):
    """ Returns a string used to print superhero names. """
    if color:
        name = paint_label(name, color)
    offset = 9 if color else 0
    return create_label_block(name, offset)

def create_fb_block(hero_fb):
    """ Returns a string used to print a superheroe's Filiation Coefficient. """
    fb_icon = '\U000025B2' if hero_fb >= 1 else '\U000025BC'
    fb_label = f'FB {fb_icon} {round(hero_fb, 3)}'
    return create_label_block(fb_label)

def create_hp_block(health_points):
    """ Returns a string used to print Health Points. """
    if health_points > 0:
        unicode_heart = 'HP \U00002764'
        hp_label = f'{unicode_heart} {health_points}'
        return create_label_block(hp_label)
    hp_label = '\U0001F480'
    return create_label_block(hp_label, -1)

def create_attack_block(attack_name, attack_damage):
    """ Returns a string describing an attack. """
    unicode_swords = '\U00002694'
    attack_label = f'{attack_name} Attack {unicode_swords} {attack_damage}'
    return create_label_block(attack_label)

def create_hero_block(hero, color = ''):
    """ Returns a list of strings describing a superhero. """
    hero_block = get_image_lines(hero.image)
    hero_block.append(create_name_block(hero.name, color))
    hero_block.append('-' * BLOCK_WIDTH)
    hero_block.append(create_hp_block(hero.base_hp))
    hero_block.append(create_fb_block(hero.fb))
    for attack_name in teams.Hero.ATTACK_NAMES:
        hero_block.append(create_attack_block(attack_name, hero.attacks[attack_name]))
    return hero_block

def create_middle_block(label, height):
    """ Returns a list of strings to print between two blocks. """
    middle_block = [FILLER] * height
    middle_block[floor(height / 2)] = create_label_block(label)
    return middle_block

def create_header_block(blue_hero, red_hero, image_height):
    """ Returns a list of strings used to print a fight's header. """
    blue_hero_block = create_hero_block(blue_hero, 'blue')
    red_hero_block = create_hero_block(red_hero, 'red')

    vs_block = create_middle_block('VS', image_height)
    vs_block.append(' ' * BLOCK_WIDTH)
    stats_height = len(blue_hero_block) - len(vs_block)
    stats_block = create_middle_block('STATS', stats_height)
    stats_block[0] = SEPARATOR

    zipped = zip(blue_hero_block, (vs_block + stats_block), red_hero_block)
    header_block = list(map(''.join, list(zipped)))
    return header_block

def create_team_block(team):
    """ Returns a list of strings used to print a team. """
    team_block = []
    team_block.append(create_name_block(team.name, team.color))
    team_block.append(SEPARATOR)
    for hero in team.heroes:
        team_block.append(create_name_block(hero.name))
    return team_block

# TODO: borrar
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

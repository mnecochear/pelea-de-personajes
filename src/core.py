""" This module contains code used to run the program. """

import sys
from email_validator import validate_email, EmailNotValidError
import teams
import battles
import printers
import mailing

class Main:
    """ Main program runner. """
    def __init__(self, title):
        self.title = title
        self.__run()

    def __run(self):
        """ Starts the simulator. """
        title_label = printers.paint_label('SUPERHEROE BATTLE SIMULATOR', 'underline')
        print(printers.create_label_block(title_label, 8, True))
        print(' ' * printers.BLOCK_WIDTH)

        email = self.__get_email()
        mailer = mailing.Mailer(email, 'Battle summary')
        delay = self.__get_delay()
        fights_to_print = self.__get_fights_to_print()

        all_heroes = teams.get_heroes()
        max_index = len(all_heroes) - 1
        if max_index < 9:
            sys.exit(f'Not enough superheroes found to start a battle ({max_index + 1}/10 minimum).')

        blue_team_indexes = teams.get_hero_indexes(max_index, [])
        red_team_indexes = teams.get_hero_indexes(max_index, blue_team_indexes)
        blue_team = teams.Team(all_heroes, blue_team_indexes, 'Blue team', 'blue')
        red_team = teams.Team(all_heroes, red_team_indexes, 'Red team', 'red')

        if delay < 0:
            print('You are in manual mode, press ENTER to print the next block')
            printers.delay_output(delay)

        battle = battles.Battle(blue_team, red_team)

        printers.print_battle(battle, delay, fights_to_print)

        for hero in (blue_team.heroes + red_team.heroes):
            if hero.image != teams.Hero.DEFAULT_IMAGE:
                teams.delete_image(hero.image)

        if email != '':
            mailer.send(battle)

    def __get_email(self):
        """ Asks for an email address and returns it. """
        email = input('Enter your email address to receive a battle summary or press ENTER to skip:\n')
        while email != '':
            try:
                email = validate_email(email).email
                break
            except EmailNotValidError:
                email = input('Enter a valid email address or press ENTER to skip:\n')
        return email

    def __get_delay(self):
        """ Asks for the delay between turns and fights. """
        delay = input('Enter the delay (>= 0 in seconds) between turns and fights or press ENTER for manual control:\n')
        while delay != '':
            try:
                delay = float(delay)
                if delay >= 0:
                    break
                delay = input('Enter a float >= 0 or press ENTER for manual control:\n')
            except ValueError:
                delay = input('Enter a float >= 0 or press ENTER for manual control:\n')
        return -1 if delay == '' else delay

    def __get_fights_to_print(self):
        """ Returns an integer indicating the amount of battles to print. """
        fights_to_print = input('Enter the amount of fights you want to print or press ENTER to print all:\n')
        while fights_to_print != '':
            try:
                fights_to_print = int(fights_to_print)
                if fights_to_print >= 0:
                    break
                fights_to_print = input('Enter an integer > 0 or press ENTER to print all:\n')
            except ValueError:
                fights_to_print = input('Enter an integer > 0 or press ENTER to print all:\n')
        return 5 if fights_to_print == '' else fights_to_print

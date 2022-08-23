""" This module contains code to send emails. """

import os
import base64
import requests
import printers

class Mailer:
    """ This class is used to send emails using Mailgun. """

    def __init__(self, to_email, subject):
        self.to_email = to_email
        self.subject = subject

    def __build_body(self, battle):
        """ Returns a summary of the battle. """
        body = []
        blue_label = printers.decorate(battle.blue_team.name, 'span', 'blue')
        red_label = printers.decorate(battle.red_team.name, 'span', 'red')
        body.append(f'{blue_label} against {red_label}')
        body.append('<p></p>')
        for i, fight in enumerate(battle.fights):
            body.append(f'<p>{printers.decorate(f"Fight #{i+1}", "strong", "black")}</p>')
            loser_index = 1 if fight.winner == fight.opponents[0] else 0
            winner_label = f'{fight.winner.name} {printers.decorate("(W)", "span", "green")}'
            loser_label = f'{fight.opponents[loser_index].name} {printers.decorate("(L)", "span", "red")}'
            vs_label = printers.decorate("vs", "span", "gray")
            if loser_index:
                body.append(f'<p>{winner_label} {vs_label} {loser_label}</p>')
            else:
                body.append(f'<p>{loser_label} {vs_label} {winner_label}</p>')
        body.append('<p></p>')
        body.append(f'<strong>{battle.winner.name} wins!</strong>')
        return ''.join(body)

    def __read_key(self):
        """ Reads the Mailgun API key and returns it. """
        file = f'{os.path.dirname(__file__)}/mailgun_key'
        try:
            with open(file, 'r', encoding = 'utf8') as stream:
                return stream.readline()
        except FileNotFoundError as err:
            raise SystemExit('API key not found') from err

    def send(self, battle):
        """ Sends an email. """
        api_key = base64.b64decode(self.__read_key()).decode('utf-8')
        domain = 'sandbox33c6b29fca024befa43c0825f61c526d.mailgun.org'
        body = self.__build_body(battle)
        try:
            post = requests.post(
                f'https://api.mailgun.net/v3/{domain}/messages',
                auth = ('api', api_key),
                data = {'from': 'Battle Simulator <simulator@battle.org>',
                    'to': [self.to_email],
                    'subject': self.subject,
                    'html': body})
            if post.status_code == 200:
                print(f'Mail successfully sent to {self.to_email}')
                return
            print(f'Unable to send mail. Status code: {post.status_code}')
        except requests.exceptions.RequestException as err:
            message = (f'An error occured while sending mail to {self.to_email}')
            raise SystemExit(message) from err

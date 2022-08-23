""" This module contains code to send emails. """

import requests

class Mailer:
    """ This class is used to send emails using Mailgun. """

    def __init__(self, to_email, subject):
        self.to_email = to_email
        self.subject = subject

    def send(self, body):
        """ Sends an email. """
        api_key = 'f0bd0b85d5112fbf956a543b2d8365ee-c76388c3-a6abd114'
        domain = 'sandbox4f797eff405a4990899ac35cc1f25d3a.mailgun.org'
        try:
            post = requests.post(
                f'https://api.mailgun.net/v3/{domain}/messages',
                auth = ('api', api_key),
                data = {'from': 'Battle Simulator <report@simulator.org>',
                    'to': [self.to_email],
                    'subject': self.subject,
                    'html': body})
            if post.status_code == 200:
                print(f'Mail successfully sent to {self.to_email}')
                return post
            print(f'Unable to send mail. Status code: {post.status_code}')
        except requests.exceptions.RequestException as err:
            message = (f'An error occured while sending mail to {self.to_email}')
            raise SystemExit(message) from err

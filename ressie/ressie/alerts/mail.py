import requests

from ..configurations.config import Config


class Mailer(object):
    apiKey = None
    sandboxUrl = None
    recipient = None

    def __init__(self):
        configuration = Config()
        self.apiKey = configuration.parse_config("MailGun", "apikey")
        self.sandboxUrl = configuration.parse_config("MailGun", "sandbox")
        self.recipient = configuration.parse_config("MailGun", "recipient")
        pass

    def send_message(self, message):
        request = requests.post(self.sandboxUrl, auth=('api', self.apiKey), data={
            'from': 'ressie@woof.com',
            'to': self.recipient,
            'subject': 'Hello',
            'text': message
        })

        print(request.status_code)
        print(request.text)
        print("Sent")

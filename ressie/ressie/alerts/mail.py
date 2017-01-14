from mailgun2 import Mailgun

from ..configurations.config import Config


class Mailer(object):
    publicKey = None
    privateKey = None
    domain = None
    authorized_recipient = None

    def __init__(self):
        configuration = Config()

        self.publicKey = configuration.parse_config("MailGun", "public_key")
        self.privateKey = configuration.parse_config("MailGun", "private_key")
        self.domain = configuration.parse_config("MailGun", "domain")
        self.authorized_recipient = configuration.parse_config("MailGun", "authorized_recipient")

    def send_message(self, message):

        mailer = Mailgun(self.domain, self.privateKey, self.publicKey)
        response = mailer.send_message(
            'alert@ressie.com', [self.authorized_recipient],
            subject="[ALERT] New issue",
            text=message
        )

        if response.status_code == 200:
            print("Queued. Thank you.")

        else:
            print("Ooops something went wrong with sending alert mail: \n %s", response.text)

import requests

from ..configuration.config import Config


class Slack(object):
    apiKey = None
    sandbox = None
    sc = None

    def __init__(self):
        configuration = Config()
        self.apiKey = configuration.parse_config("MailGun", "apikey")
        pass

    def send_message(self, message):
        key = 'YOUR API KEY HERE'
        sandbox = 'YOUR SANDBOX URL HERE'
        recipient = 'YOUR EMAIL HERE'

        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
        request = requests.post(request_url, auth=('api', key), data={
            'from': 'hello@example.com',
            'to': recipient,
            'subject': 'Hello',
            'text': 'Hello from Mailgun'
        })

        print("Sent")

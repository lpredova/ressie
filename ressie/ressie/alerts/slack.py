from slackclient import SlackClient

from ..configurations.config import Config


class Slack(object):
    apiKey = None
    sc = None

    def __init__(self):
        configuration = Config()
        self.apiKey = configuration.parse_config("Slack", "token")
        self.sc = SlackClient(self.apiKey)
        pass

    def send_message(self, message):
        result = self.sc.api_call(
            "chat.postMessage",
            channel="#lovro-test",
            text=":warning: \n" + message
        )

        if result.get('ok', False):
            print("Sent")
        else:
            print("Ooops, there was problems with sending slack notification")

        return

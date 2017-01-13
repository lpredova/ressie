from slackclient import SlackClient

from ..configuration.config import Config


class Slack(object):
    apiKey = None
    sc = None

    def __init__(self):
        configuration = Config()
        self.apiKey = configuration.parse_config("Slack", "apikey")
        self.sc = SlackClient(self.apiKey)
        pass

    def send_message(self, message):
        self.sc.api_call(
            "chat.postMessage",
            channel="#lovro-test",
            text=":warning: \n" + message
        )

        print("Sent")

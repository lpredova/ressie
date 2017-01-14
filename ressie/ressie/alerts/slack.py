from slackclient import SlackClient

from ..configurations.config import Config


class Slack(object):
    token = None
    sc = None
    channel = None

    def __init__(self):
        configuration = Config()
        self.token = configuration.parse_config("Slack", "token")
        self.channel = configuration.parse_config("Slack", "channel")

        self.sc = SlackClient(self.token)
        pass

    def send_message(self, message):
        result = self.sc.api_call(
            "chat.postMessage",
            channel=self.channel,
            text=":warning: \n" + message
        )

        if result.get('ok', False):
            print("Sent")
        else:
            print("Ooops, there was problems with sending slack notification")

        return

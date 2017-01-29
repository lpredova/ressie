# compare for standard html and SQL keywords
from ..alerts.mail import Mailer
from ..alerts.slack import Slack

class Http(object):
    def number_requests(self):
        print("Number of requests")

        # Number of hits above average, if above average raise alarm
        '''if res['hits']['total'] > 5:
            mailer = Mailer()
            slack = Slack()

            mailer.send_message("Number of requests suspiciously high")
            slack.send_message("AAAAA jebiga :D")
         '''

    def url(self):
        print("URL")

    def body(self):


        print("Analyzing body")
        print("check for sql keywords")

    def header(self):
        print("Analyzing header (length)")

    def ip(self):
        print("Analyzing header (length)")

    def response_time(self):
        print("Analyzing response time")

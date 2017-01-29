# compare for standard html and SQL keywords

class Http(object):
    def number_requests(self, results):
        print("Number of requests")

        # Number of hits above average, if above average raise alarm
        '''if res['hits']['total'] > 5:
            mailer = Mailer()
            slack = Slack()

            mailer.send_message("Number of requests suspiciously high")
            slack.send_message("AAAAA jebiga :D")
         '''

    def url(self, hit):
        print("URL")

    def body(self, hit):
        print("Analyzing body")
        print("check for sql keywords")

    def header(self, hit):
        print("Analyzing header (length)")

    def ip(self, hit):
        print("Analyzing header (length)")

    def response_time(self, hit):
        print("Analyzing response time")

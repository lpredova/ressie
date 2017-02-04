import decimal

from checks import Check
from ip import IP
from ressie.database import Queries


class Http(object):
    check = None
    average_threshold = 1.5

    def __init__(self):
        super(Http, self).__init__()
        self.check = Check()

    def number_requests(self, hits):
        query = Queries()
        result = query.number_of_requests()

        # min 3 items for average
        if result['total'] >= 3:

            average = query.avg_requests()['average']
            threshold = decimal.Decimal(average) * decimal.Decimal(self.average_threshold)

            if hits['hits']['total'] > threshold:
                self.check.send_alert("Number of requests suspiciously high", None)

        query.insert_requests(hits['hits']['total'])

    def url(self, hit):
        url = hit.get_path()
        if url and not (self.check.check_for_sql_and_js(url)):
            if self.check.check_blacklist(url):
                msg = "URL blacklisted"
                self.check.send_alert(msg, hit)
                return msg

        else:
            msg = "SQL or JS detected in url"
            self.check.send_alert(msg, hit)
            return msg

        # parse each param in url
        '''
        try:
            url = url.split('/')
            print url
        except Exception as e:
            print(e.message)
        '''

        return True

    def body(self, hit):
        if hit.get_method() == "POST":

            body = hit.get_request_body()
            if body and not (self.check.check_for_sql_and_js(body)):
                # check fuzz db
                # TODO
                print ("POST METODA")

            else:
                print ("POST NESTO NE VALAJ")

        return True

    def header(self, hit):
        header = hit.get_request_headers()

        for field in header:
            if self.check.check_for_sql_and_js(header[field]):
                msg = "SQL or JS detected in header"
                self.check.send_alert(msg, hit)
                return msg

            if self.check.check_blacklist(header[field]):
                msg = "URL blacklisted"
                self.check.send_alert(msg, hit)
                return msg

        return True

    def ip(self, hit):
        ip = hit.get_ip()
        checker = IP()
        if ip:
            if checker.check_ip_is_tor(ip):
                msg = "User with TOR spotted"
                self.check.send_alert(msg, hit)
                return msg

            if checker.check_ip_virus_total(ip):
                msg = "User from malicious IP spotted"
                self.check.send_alert(msg, hit)
                return msg

        return True

    def response_time(self, hit):
        query = Queries()
        average = query.avg_response_times()['average']

        if average:
            response_time = hit.get_response_time()
            if response_time:
                avg = decimal.Decimal(average) * decimal.Decimal(self.average_threshold)
                if avg and avg <= decimal.Decimal(response_time):
                    msg = "Response is taking unusually long (%d ms)" % response_time
                    self.check.send_alert(msg, hit)
                    return msg

        return True

    def handle_average(self, average):
        self.check.handle_average(average)

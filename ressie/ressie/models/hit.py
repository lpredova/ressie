import json


class Hit(object):
    hit = None

    def set_hit(self, hit):
        self.hit = hit

    def get_timestamp(self):
        if self.hit["_source"]["@timestamp"]:
            return self.hit["_source"]["@timestamp"]

        return None

    def get_method(self):
        if self.hit["_source"]["method"]:
            return self.hit["_source"]["method"]

        return None

    def get_ip(self):
        if self.hit["_source"]["client_ip"]:
            return self.hit["_source"]["client_ip"]

        return None

    def get_response_time(self):
        if self.hit["_source"]["responsetime"]:
            return self.hit["_source"]["responsetime"]

        return None

    def get_query(self):
        if self.hit["_source"]["query"]:
            return self.hit["_source"]["query"]

        return None

    def get_path(self):
        if self.hit["_source"]["path"]:
            return self.hit["_source"]["path"]

        return None

    def get_request(self):
        if self.hit["_source"]["http"]["request"]:
            return self.hit["_source"]["http"]["request"]

        return None

    def get_request_headers(self):
        if self.hit["_source"]["http"]["request"]["headers"]:
            return self.hit["_source"]["http"]["request"]["headers"]

        return None

    def get_request_body(self):
        if self.hit["_source"]["http"]["request"]["params"]:
            return self.hit["_source"]["http"]["request"]["params"]

        return None

    def get_response(self):
        if self.hit["_source"]["http"]["response"]:
            return self.hit["_source"]["http"]["response"]

        return None

    def get_response_headers(self):
        if self.hit["_source"]["http"]["response"]["headers"]:
            return self.hit["_source"]["http"]["response"]["headers"]

        return None

    def get_response_code(self):
        if self.hit["_source"]["http"]["response"]["code"]:
            return self.hit["_source"]["http"]["response"]["code"]

        return None

    def get_pretty_print(self):

        return (
            "%s %s \n:arrow_right: %s \n :arrow_left: %s" % (
                self.get_method(), self.get_path(), json.dumps(self.get_request(), ensure_ascii=False),
                json.dumps(self.get_response(), ensure_ascii=False)))

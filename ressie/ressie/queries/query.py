from __future__ import print_function

import datetime

from elasticsearch import Elasticsearch

from ressie.analyzer.http import Http
from ressie.models import Hit


class ElasticQuery(object):
    # in minutes
    time_threshold = 200000

    def __init__(self):
        pass

    def check_status(self):
        self.elasticsearch()

    def elasticsearch(self):

        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "_type": "http"
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "now-%dm" % self.time_threshold
                                }
                            }
                        }
                    ]
                }
            }
        }

        date = datetime.datetime.now()
        date = date.strftime("%Y.%m.%d")
        index_date = "logstash-%s" % date
        es = Elasticsearch()
        try:
            res = es.search(index=index_date, body=query)

            http_analyzer = Http()
            http_analyzer.number_requests(res)

            for hit in res['hits']['hits']:
                elastic_hit = Hit()
                elastic_hit.set_hit(hit)

                http_analyzer.body(elastic_hit)
                http_analyzer.header(elastic_hit)
                http_analyzer.ip(elastic_hit)
                http_analyzer.response_time(elastic_hit)

        except Exception as e:
            print(e.message)

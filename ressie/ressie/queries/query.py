from __future__ import print_function

import datetime
import time

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

        start = time.clock()
        try:
            results = es.search(index=index_date, body=query)

            http_analyzer = Http()
            http_analyzer.number_requests(results)
            response_times = average = 0

            for hit in results['hits']['hits']:
                elastic_hit = Hit()
                elastic_hit.set_hit(hit)

                http_analyzer.url(elastic_hit)
                http_analyzer.body(elastic_hit)
                http_analyzer.header(elastic_hit)
                http_analyzer.ip(elastic_hit)
                http_analyzer.response_time(elastic_hit)

                response_times += elastic_hit.get_response_time()

            if results['hits']['total'] > 0:
                average = response_times / results['hits']['total']

            if average > 0:
                http_analyzer.handle_average(average)

            end = time.clock()
            print("Evaluation done in: %f" % (end - start))

        except Exception as e:
            end = time.clock()
            print("Evaluation done in: %f" % (end - start))
            print(e.message)

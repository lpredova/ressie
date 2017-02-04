from __future__ import print_function

import datetime
import time

from elasticsearch import Elasticsearch

from ressie.analyzer.http import Http
from ressie.helpers import *
from ressie.models import Hit


class ElasticQuery(object):
    # in minutes
    time_threshold = 200000
    response_times = average = 0

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
            idx = 0

            for hit in results['hits']['hits']:
                idx += 1
                self.run_evaluation(idx, hit, http_analyzer)

            if results['hits']['total'] > 0:
                average = self.response_times / results['hits']['total']
                if average > 0:
                    http_analyzer.handle_average(average)

            end = time.clock()
            print("Evaluation done in: %f" % (end - start))

        except Exception as e:
            end = time.clock()
            print("Evaluation done in: %f" % (end - start))
            print(e.message)

    def run_evaluation(self, index, hit, http_analyzer):
        elastic_hit = Hit()
        elastic_hit.set_hit(hit)

        status = []
        result = http_analyzer.url(elastic_hit)
        if not isinstance(result, bool):
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.body(elastic_hit)
        if not isinstance(result, bool):
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.header(elastic_hit)
        if not isinstance(result, bool):
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.ip(elastic_hit)
        if not isinstance(result, bool):
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.response_time(elastic_hit)
        if not isinstance(result, bool):
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        print("%d.\t%s-%s\t%s" % (index, elastic_hit.get_response_code(), elastic_hit.get_path(), ' '.join(status)))
        response_time = elastic_hit.get_response_time()
        if response_time:
            self.response_times += response_time

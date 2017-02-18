from __future__ import print_function

import datetime
import time
from threading import Thread, current_thread

from elasticsearch import Elasticsearch

from ressie.analyzer.http import Http
from ressie.database.logging import Logger
from ressie.helpers import *
from ressie.models import Hit


class ElasticQuery(object):
    # in seconds
    time_threshold = 1800
    response_times = request_length = average = number_of_valid_times = number_of_valid_length = 0
    fine = 0
    logger = None

    def __init__(self):
        self.logger = Logger()
        pass

    def check_status(self):
        self.elasticsearch()

    def elasticsearch(self):

        query = {
            "size": 1000,
            "sort": [
                {"@timestamp": {"order": "asc"}}
            ],
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
                                    "gte": "now-%ds" % self.time_threshold
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

            for hit in results['hits']['hits']:
                thread = Thread(target=self.run_evaluation, args=(hit, http_analyzer))
                thread.start()
                thread.join()

            if self.number_of_valid_times > 0:
                average_response_time = self.response_times / self.number_of_valid_times
                if average_response_time > 0:
                    http_analyzer.handle_average_response_time(average_response_time)

            if self.number_of_valid_length > 0:
                average_request_length = self.request_length / self.number_of_valid_length
                if average_request_length > 0:
                    http_analyzer.handle_average_request_size(average_request_length)

            end = time.clock()
            stop = end - start
            print("\nEvaluation done in: %fms" % stop)

            if results['hits']['total'] == self.fine:
                print_green("%d/%d requests healthy" % (self.fine, results['hits']['total']))

            else:
                print("\n")
                print_red("%d/%d requests healthy" % (self.fine, results['hits']['total']))

            self.logger.write_to_log("\nEvaluation done in: %fms" % stop,
                                     "%d/%d requests healthy" % (self.fine, results['hits']['total']))

        except Exception as e:
            end = time.clock()
            stop = end - start
            print("\nEvaluation done in: %fms" % stop)
            self.logger.write_to_log("\nEvaluation done in: %fms" % stop, "")

    def run_evaluation(self, hit, http_analyzer):
        elastic_hit = Hit()
        elastic_hit.set_hit(hit)

        healthy = True
        status = []
        result = http_analyzer.url(elastic_hit)
        if not isinstance(result, bool):
            healthy = False
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.body(elastic_hit)
        if not isinstance(result, bool):
            healthy = False
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.header(elastic_hit)
        if not isinstance(result, bool):
            healthy = False
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.ip(elastic_hit)
        if not isinstance(result, bool):
            healthy = False
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.response_time(elastic_hit)
        if not isinstance(result, bool):
            healthy = False
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        result = http_analyzer.request_size(elastic_hit)
        if not isinstance(result, bool):
            healthy = False
            status.append(format_red(result))
        else:
            status.append(format_green("OK"))

        print("%s.\t%s \t%s ->%s\t%s" % (current_thread().getName(), elastic_hit.get_timestamp(),
                                         elastic_hit.get_query(),
                                         elastic_hit.get_response_code(), ' '.join(status)))

        response_time = elastic_hit.get_response_time()

        # bigger than 10 because of average, skipping outliers
        if response_time and response_time > 10:
            self.response_times += response_time
            self.number_of_valid_times += 1

        request_length = elastic_hit.get_request_size()
        # bigger than 30 because of average, skipping outliers
        if request_length and request_length > 30:
            self.request_length += request_length
            self.number_of_valid_length += 1

        if healthy:
            self.fine += 1

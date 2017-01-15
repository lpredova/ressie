import os

import whoosh.index as index
from elasticsearch import Elasticsearch
from whoosh.qparser import QueryParser


class ElasticQuery(object):
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def check_status(self):
        self.check_elasticsearch()
        '''
        ix = index.open_dir(self.index_dir)
        writer = ix.writer()

        writer.commit()
        '''

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("attack", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)

    def check_elasticsearch(self):
        es = Elasticsearch()
        res = es.search(index="logstash-2017.01.15",
                        doc_type="logs",
                        body={"query": {"match_all": {}}})

        for hit in res['hits']['hits']:
            print("%s" % hit["_source"]["message"])

            # print "aaa"

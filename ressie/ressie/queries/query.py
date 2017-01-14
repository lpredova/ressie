import os

import whoosh.index as index
from whoosh.qparser import QueryParser


class ElasticQuery(object):
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def check_status(self):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("attack", schema=ix.schema)
        q = qp.parse(u"php")

        with ix.searcher() as s:
            results = s.search(q, limit=20)

            print results

        '''
        ix = index.open_dir(self.index_dir)
        writer = ix.writer()

        writer.commit()
        '''

import os

import whoosh.index as index

import schema


class Indexer(object):
    index_dir = os.getcwd() + "/data/fuzzdb/"
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def create_index(self):
        if not os.path.exists(self.index_folder):
            os.mkdir(self.index_folder)

        ix = index.create_in("indexdir", schema.AttackSchema)

        print index

        '''
        ix = index.open_dir(self.index_dir)
        writer = ix.writer()

        writer.commit()
        '''

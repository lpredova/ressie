import codecs
import os

import whoosh.index as index

import schema


class Indexer(object):
    fuzzdb_folder = os.getcwd() + "/data/fuzzdb/"
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def create_index(self):

        if not os.path.exists(self.index_folder):
            os.mkdir(self.index_folder)

        index.create_in(self.index_folder, schema.AttackSchema)
        ix = index.open_dir(self.index_folder)

        writer = ix.writer()

        for root, dirs, files in os.walk(self.fuzzdb_folder):
            for f in files:
                file_path = os.path.join(root, f)

                with codecs.open(file_path, "r", "utf-8") as content_file:
                    for line in content_file:
                        if line != "":
                            try:
                                line.decode('utf-8')
                                writer.add_document(title=u"%s" % f, attack=u"%s" % line, path=u"%s" % file_path)
                            except UnicodeError:
                                continue
                            except Exception as e:
                                print(e.message)

        writer.commit()
        print("Indexing done")

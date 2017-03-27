import ConfigParser
import os
import sys


class Config(object):
    def __init__(self):
        pass

    def parse_config(self, section, key):
        config_reader = ConfigParser.ConfigParser()

        path = os.path.dirname(sys.modules['__main__'].__file__) + '/configurations/config.prod'
        config_reader.read(path)
        return self.config_section_map(section, config_reader)[key]

    def config_section_map(self, section, config_reader):
        dict1 = {}
        options = config_reader.options(section)
        for option in options:
            try:
                dict1[option] = config_reader.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except Exception as e:
                print("exception on %s. \n %s" % option, e.message)
                dict1[option] = None

        return dict1

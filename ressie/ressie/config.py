import ConfigParser


class Config(object):
    def __init__(self):
        pass

    def parse_config(self):
        Config = ConfigParser.ConfigParser()
        var = Config.read('config')

        print "parsing config" + var

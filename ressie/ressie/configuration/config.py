import ConfigParser


class Config(object):
    def __init__(self):
        pass

    @staticmethod
    def parse_config():
        Config = ConfigParser.ConfigParser()
        var = Config.read('config')

        print "parsing config" + var

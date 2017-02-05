import datetime
import os


class Logger(object):
    log_folder = os.getcwd() + "/data/custom/logs/"
    today_log = None

    def __init__(self):
        super(Logger, self).__init__()

        date = datetime.datetime.now()
        date = date.strftime("%Y.%m.%d")
        self.today_log = "log-ressie-%s" % date

    def write_to_log(self, line, message):
        log_file = open(self.log_folder + self.today_log, "a+")

        date = datetime.datetime.now()
        time = date.strftime("%c")

        log_file.write('\n%s- %s\n%s\n' % (time, message, line))
        log_file.close()

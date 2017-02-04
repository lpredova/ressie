from difflib import SequenceMatcher


def print_help():
    print "\n" \
          "Ressie is SIEM monitoring plugin for Elastic stack \n" \
          "python -m ressie [options] \n" \
          "\nOptions\n---------------------\n" \
          "monitor - runs monitoring deamon\n" \
          "h, help - open help prompt\n" \
          "slack - sends slack notification\n" \
          "mail - sends mail\n" \
          ""


def format_yellow(text):
    return '\x1b[6;30;43m' + text + '\x1b[0m'


def print_yellow(text):
    print('\x1b[6;30;43m' + text + '\x1b[0m')


def format_green(text):
    return '\x1b[6;30;42m' + text + '\x1b[0m'


def print_green(text):
    print('\x1b[6;30;42m' + text + '\x1b[0m')


def format_red(text):
    return '\x1b[6;30;41m' + text + '\x1b[0m'


def print_red(text):
    print('\x1b[6;30;41m' + text + '\x1b[0m')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def print_help():
    print "\n" \
          "Ressie is SIEM monitoring plugin for Elastic stack \n" \
          "python -m ressie [options] \n" \
          "\nOptions\n---------------------\n" \
          "monitor - runs monitoring deamon\n" \
          "h, help - open help prompt\n" \
          ""


def print_green(text):
    print('\x1b[6;30;42m' + text + '\x1b[0m')


def print_red(text):
    print('\x1b[6;30;41m' + text + '\x1b[0m')

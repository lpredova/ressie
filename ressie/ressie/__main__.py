import sys

import helpers.helper as helper


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    try:
        if args[0] == 'query':
            print args[0]

        elif args[0] == 'help' or args[0] == 'h':
            helper.print_help()

        else:
            helper.print_red("Unknown option")

    except Exception as e:
        helper.print_red("Missing required options: " + e.message)


if __name__ == "__main__":
    main()

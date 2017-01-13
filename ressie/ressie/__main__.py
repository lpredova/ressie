import sys

import alerting.slack as slack
import helpers.helper as helper
import queries.query as query


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    try:
        param = args[0]
        if param == "query":
            elastic = query.ElasticQuery()
            elastic.check_status()

        elif param == "slack":
            alert = slack.Slack()
            alert.send_message("CUSTOM MESSAGE FOR SLACK")

        elif param == "help" or param == "h":
            helper.print_help()

        else:
            helper.print_red("Unknown option")

    except Exception as e:
        helper.print_red("\nError: " + e.message + "\n")


if __name__ == "__main__":
    main()
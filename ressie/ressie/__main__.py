import sys

import alerts.mail as mailer
import alerts.slack as slack
import analyzer.ip as ip
import helpers.helper as helper
import indexes.indexer as index
import queries.query as query


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    try:
        param = args[0]
        if param == "tor":
            tor = ip.IP()
            tor.fetch_tor_exit_nodes()
            tor.fetch_ip_addresses_from_file()

        if param == "search":
            elastic = query.ElasticQuery()
            elastic.check_status()

        elif param == "slack":
            alert = slack.Slack()
            alert.send_message("CUSTOM MESSAGE FOR SLACK")

        elif param == "mail":
            alert = mailer.Mailer()
            alert.send_message("CUSTOM MESSAGE FOR EMAIL")

        elif param == "index":
            indexer = index.Indexer()
            indexer.create_index()

        elif param == "help" or param == "h":
            helper.print_help()

        else:
            helper.print_red("Unknown option")

    except Exception as e:
        helper.print_red("\nError: " + e.message + "\n")


if __name__ == "__main__":
    main()

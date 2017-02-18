from __future__ import print_function

import sys
import time

import alerts.mail as mailer
import alerts.slack as slack
import analyzer.checks as check
import analyzer.ip as ip
import helpers.helper as helper
import indexes.indexer as index
import queries.query as query
import ressie.analyzer.scripts as script


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    try:
        param = args[0]
        if param == "run":
            iteration = 1
            try:
                while 1:
                    print("%d Evaluating requests...\n" % iteration)
                    elastic = query.ElasticQuery()
                    elastic.check_status()
                    time.sleep(10)
                    iteration += 1
            except KeyboardInterrupt:
                print('\nExiting by user request.\n')
                sys.exit(0)

        if param == "tor":
            tor = ip.IP()
            tor.fetch_tor_exit_nodes()
            tor.fetch_ip_addresses_from_file()

        if param == "script":
            sc = script.Scripts()
            sc.run_defined_scripts()

        if param == "find":
            c = check.Check()
            result = c.check_attack_db("wordpress")

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

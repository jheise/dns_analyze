#!/usr/bin/env python

import argparse
import csv
import datastream.analyzer

class NewDomainAnalyzer(datastream.analyzer.Analyzer):

    def __init__(self, zmq_host, zmq_topic, port, domains):
        super(NewDomainAnalyzer, self).__init__(zmq_host, zmq_topic, port)
        domain_list = []
        with open(domains) as fh:
            data = csv.DictReader(fh)
            for line in data:
                domain_list.append(line["Domain"])

        self.domains = set(domain_list)

    def _analyzer(self, data):
        query = data["Query"].split(".")
        if len(query) >= 2:
            domain = ".".join(query[-2:])
            if domain in domain_list:
                data["new_domain"] = "true"

        return data


def main(zmq_host, zmq_topic, port, domains):

    domain_analyzer = NewDomainAnalyzer(zmq_host, zmq_topic, port, domains)
    domain_analyzer.activate()

    running = True

    try:
        while running:
            domain_analyzer.process()
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-zh", "--zmq-host", default="tcp://localhost:7777", help="host running zmq dns stream, default tcp://localhost:7777")
    parser.add_argument("-zt", "--zmq-topic", default="dns", help="zmq topic to listen for")
    parser.add_argument("-p", "--port", default=8888, type=int,
        help="port to bind, default 8888")
    parser.add_argument("-d", "--domains", default="new_domains.csv", help="csv file containing new domains")

    args = parser.parse_args()

    main(args.zmq_host, args.zmq_topic, args.port, args.domains)

#!/usr/bin/env python

import argparse
import datastream.analyzer

class DomainAnalyzer(datastream.analyzer.Analyzer):

    def _analyze(self, data):
        # check if this is a query for a new domain
        query = data["Query"].split(".")
        domain = ".".join(query[-2:])
        subdomain = ".".join(query[:-2])
        data["Domain"] = domain
        data["Subdomain"] = subdomain

        return data

def main(zmq_host, zmq_topic, port):

    domainanalyzer = DomainAnalyzer(zmq_host, zmq_topic, port)
    domainanalyzer.activate()
    running = True

    try:
        while running:
            domainanalyzer.process()
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-zh", "--zmq-host", default="tcp://localhost:7777", help="host running zmq dns stream, default tcp://localhost:7777")
    parser.add_argument("-zt", "--zmq-topic", default="dns", help="zmq topic to listen for")
    parser.add_argument("-p", "--port", default=9999, type=int,
        help="port to bind, default 9999")

    args = parser.parse_args()

    main(args.zmq_host, args.zmq_topic, args.port)

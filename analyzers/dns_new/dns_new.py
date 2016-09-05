#!/usr/bin/env python

import argparse
import csv
import datastream.analyzer

class NewDomainAnalyzer(datastream.analyzer.Analyzer):

    def __init__(self, zmq_host, zmq_topic, port, domains):
        super(NewDomainAnalyzer, self).__init__(zmq_host, zmq_topic, port)
        self.domains = domains

    def _analyzer(self, data):
        query = data["Query"].split(".")
        if len(query) >= 2:
            domain = ".".join(query[-2:])
            if domain in domain_list:
                data["new_domain"] = "true"

        return data


def main(zmq_host, zmq_topic, port, domains):

    # setup the zmq pub socket
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{0}".format(port))

    # setup the zmq sub socket
    scontext = zmq.Context()
    ssocket = scontext.socket(zmq.SUB)
    ssocket.connect(zmq_host)
    ssocket.setsockopt(zmq.SUBSCRIBE, zmq_topic)

    # read new domains into set

    domain_list = []
    with open(domains) as fh:
        data = csv.DictReader(fh)
        for line in data:
            domain_list.append(line["Domain"])

    domain_list = set(domain_list)

    running = True

    try:
        while running:
            msg = ssocket.recv()
            topic, data = msg.split(" ", 1)
            data = json.loads(data)

            # check if this is a query for a new domain

            # repackage data and deploy
            socket.send(zmq_topic + " " + json.dumps(data))

    except Exception as e:
        print e

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-zh", "--zmq-host", default="tcp://localhost:7777", help="host running zmq dns stream, default tcp://localhost:7777")
    parser.add_argument("-zt", "--zmq-topic", default="dns", help="zmq topic to listen for")
    parser.add_argument("-p", "--port", default=8888, type=int,
        help="port to bind, default 8888")
    parser.add_argument("-d", "--domains", default="new_domains.csv", help="csv file containing new domains")

    args = parser.parse_args()

    main(args.zmq_host, args.zmq_topic, args.port, args.domains)

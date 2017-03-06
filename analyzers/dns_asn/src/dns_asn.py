#!/usr/bin/env python

import argparse
import datastream.analyzer
from ipwhois import Net
from ipwhois import IPASN

class ASNAnalyzer(datastream.analyzer.Analyzer):

    def _analyzer(self, data):
        if "Answer" in data:
            net = Net(data["Answer"])
            obj = IPASN(net)
            data["ASN"] = obj.lookup()["asn"]

        return data

def main(zmq_host, zmq_topic, port):

    asnanalyzer = ASNAnalyzer(zmq_host, zmq_topic, port)
    asnanalyzer.activate()
    running = True

    try:
        while running:
            asnanalyzer.activate()
    except KeyboardInterrupt:
            running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parse data lookup ASN")
    parser.add_argument("-zh", "--zmq-host", default="tcp://localhost:7777",
                        help="host running zmq dns stream, default tcp://localhost:7777")
    parser.add_argument("-zt", "--zmq-topic", default="dns",
                        help="zmq topic to listen for")
    parser.add_argument("-p", "--port", default=9999, type=int,
                        help="port to bind, default 9999")
    args = parser.parse_args()

    main(args.zmq_host, args.zmq_topic, args.port)


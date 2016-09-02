#!/usr/bin/env python

import argparse
import datastream.analyzer

class FilterAnalyzer(datastream.analyzer.Analyzer):

    def __init__(self, zmq_host, zmq_topic, port, whitelist, blacklist):
        super(FilterAnalyzer, self).__init__(zmq_host, zmq_topic, port)
        self.whitelist = whitelist
        self.blacklist = blacklist
        print "whitelist:", whitelist
        print "blacklist:", blacklist

    def _analyze(self, data):
        if data["Domain"] in self.whitelist:
            return data

        if data["Domain"] in self.blacklist:
            print "dropping", data["Domain"]
            return None

        return data

def main(zmq_host, zmq_topic, port, whitelist_path, blacklist_path):
    whitelist = []
    blacklist = []
    if whitelist_path:
        whitelist = [x[:-1] for x in open(whitelist_path).readlines()]
    if blacklist_path:
        blacklist = [x[:-1] for x in open(blacklist_path).readlines()]

    filteranalyzer = FilterAnalyzer(zmq_host, zmq_topic, port, whitelist, blacklist)
    filteranalyzer.activate()
    running = True

    try:
        while running:
            filteranalyzer.process()
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Filter based on blacklist and whitelist")
    parser.add_argument("-z", "--zmq", default="tcp://localhost:7777", help="ZMQ connection, default tcp://localhost:7777")
    parser.add_argument("-t", "--topic", default="dns", help="topic on zmq, default dns")
    parser.add_argument("-p", "--port", default=7778, help="port to open on, default 7778")
    parser.add_argument("-w", "--whitelist", help="path to whitelist file")
    parser.add_argument("-b", "--blacklist", help="path to blacklist file")

    args = parser.parse_args()

    main(args.zmq, args.topic, args.port, args.whitelist, args.blacklist)

#!/usr/bin/env python

import argparse
import datastream.analyzer
import requests
import json

class ThreatAnalyzer(datastream.analyzer.Analyzer):

    def _analyze(self, data):
        query = data["Query"]
        resp = requests.get("http://localhost:9999/domain/{0}/".format(query))
        try:
            threat_data = json.loads(resp.text)
            if "permalink" in threat_data:
                data["permalink"] = threat_data["permalink"]
            if "hashes" in threat_data:
                hashes = threat_data["hashes"]
                hashes_str = ",".join(hashes)
                data["hashes"] = hashes_str
        except Exception as e:
            print "Error with {0}".format(query)
            print e
        return data


def main(zmq_host, zmq_topic, port):

    threatanalyzer = ThreatAnalyzer(zmq_host, zmq_topic, port)
    threatanalyzer.activate()
    running = True

    try:
        while running:
            threatanalyzer.process()
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-zh", "--zmq-host", default="tcp://localhost:7777", help="host running zmq dns stream, default tcp://localhost:7777")
    parser.add_argument("-zt", "--zmq-topic", default="dns", help="zmq topic to listen for")
    parser.add_argument("-p", "--port", default=7788, type=int,
        help="port to bind, default 7788")

    args = parser.parse_args()

    main(args.zmq_host, args.zmq_topic, args.port)

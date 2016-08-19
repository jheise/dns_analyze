#!/usr/bin/env python

import argparse
import analyzer

class PrintAnalyzer(analyzer.Analyzer):

    def _analyze(self, data):
        print data
        return None

def main(zmq_host, zmq_topic):
    printer = PrintAnalyzer(zmq_host, zmq_topic, "9999")
    printer.activate()
    running = True

    try:
        while running:
            printer.process()
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Consume json from zmq and display data")
    parser.add_argument("-z", "--zmq", default="tcp://localhost:7777", help="ZMQ connection, default tcp://localhost:7777")
    parser.add_argument("-t", "--topic", default="dns", help="ZMQ topic, default dns")

    args = parser.parse_args()

    main(args.zmq, args.topic)

#!/usr/bin/env python

import argparse
import analyzer

class DomainAnalyzer(analyzer.Analyzer):

    def _analyze(self, data):
        print data
        return None

def main(zmq_host, zmq_topic, port):
    printer = DomainAnalyzer(zmq_host, zmq_topic, port)
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
    parser.add_argument("-p", "--port", default="7778", help="port to advertise on, default 7778")

    args = parser.parse_args()

    main(args.zmq, args.topic, args.port)

#!/usr/bin/env python

import argparse
import datastream.reporter
import json
import requests

default_keys = set(["Timestamp","SrcIP","DstIP","Query"])

class GelfReporter(datastream.reporter.Reporter):
    def __init__(self, zmq_host, zmq_topic, gelf_host, hostname):
        super(GelfReporter,self).__init__(zmq_host, zmq_topic)
        self.gelf_host = gelf_host
        self.hostname = hostname

    def _report(self, data):
        output = {}
        output["version"] = "1.1"
        output["host"] = self.hostname
        output["short_message"] = "dns_scan"
        output["timestamp"] = data["Timestamp"]
        output["level"] = 1
        output["_src_ip"] = data["SrcIP"]
        output["_dst_ip"] = data["DstIP"]

        # all standard keys taken care of, deal with any new keys
        for key in data.keys():
            if key not in default_keys:
                new_key = "_{0}".format(key.lower())
                output[new_key] = data[key]

        print output
        r = requests.post(self.gelf_host, data=json.dumps(output))

def main(zmq_host, zmq_topic, gelf_host, hostname):
    gelf_reporter = GelfReporter(zmq_host, zmq_topic, gelf_host, hostname)
    gelf_reporter.activate()
    running = True

    try:
        while running:
            gelf_reporter.process()

    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Consume json from zmq and export gelf")
    parser.add_argument("-z", "--zmq", default="tcp://localhost:7777", help="ZMQ connection eg: tcp://localhost:7777")
    parser.add_argument("-t", "--topic", default="dns", help="ZMQ topic, default dns")
    parser.add_argument("-g", "--gelf", default="http://localhost:9500/gelf", help="GELF endpoint eg: http://localhost:9500/gelf")
    parser.add_argument("-ho", "--host", default="dns_scan", help="hostname to set in gelf")

    args = parser.parse_args()

    main(args.zmq, args.topic, args.gelf, args.host)

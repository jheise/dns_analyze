#!/usr/bin/env python

import zmq
import json
import requests
import argparse

default_keys = set(["Timestamp","SrcIP","DstIP","Query"])

def main(zmq_host, zmq_topic, gelf_host, hostname):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(zmq_host)
    socket.setsockopt(zmq.SUBSCRIBE, zmq_topic)

    running = True

    try:
        while running:
            msg = socket.recv()
            topic, data = msg.split(" ", 1)
            data = json.loads(data)

            output = {}
            output["version"] = "1.1"
            output["host"] = hostname
            output["short_message"] = "dns_scan"
            output["timestamp"] = data["Timestamp"]
            output["level"] = 1
            output["_src_ip"] = data["SrcIP"]
            output["_dst_ip"] = data["DstIP"]
            output["_query"] = data["Query"]

            # all standard keys taken care of, deal with any new keys
            for key in data.keys():
                if key not in default_keys:
                    new_key = "_{0}".format(key.lower())
                    output[new_key] = data[key]

            #if "new_domain" in data:
                #output["_new_domain"] = data["new_domain"]

            print output
            r = requests.post(gelf_host, data=json.dumps(output))

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

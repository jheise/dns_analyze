#!/usr/bin/env python

import zmq
import json
import argparse

def main(zmq_host, zmq_topic):
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
            output["host"] = "dns_scan"
            output["short_message"] = "dns_scan"
            output["timestamp"] = data["timestamp"]
            output["level"] = 1
            output["_src_ip"] = data["src_ip"]
            output["_dst_ip"] = data["dst_ip"]
            output["_query"] = data["query"]

            print output

    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Consume json from zmq and display data")
    parser.add_argument("-z", "--zmq", required=True, help="ZMQ connection eg: tcp://10.0.0.1:7777")
    parser.add_argument("-t", "--topic", default="dns", help="ZMQ topic, default dns")

    args = parser.parse_args()

    main(args.zmq, args.topic)

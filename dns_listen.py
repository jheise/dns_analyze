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

            print data

    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Consume json from zmq and display data")
    parser.add_argument("-z", "--zmq", default="tcp://localhost:7777", help="ZMQ connection eg: tcp://localhost:7777")
    parser.add_argument("-t", "--topic", default="dns", help="ZMQ topic, default dns")

    args = parser.parse_args()

    main(args.zmq, args.topic)

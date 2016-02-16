#!/usr/bin/env python

from threatcrowd import domain_report
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.0.42.7:7777")
socket.setsockopt(zmq.SUBSCRIBE, "dns")

running = True

try:
    while running:
        msg = socket.recv()
        topic, data = msg.split(" ", 1)
        data = json.loads(data)
        domain = data["query"][:-1]
        print "Report: {0}".format(domain)
        print domain_report(domain)
except KeyboardInterrupt:
    running = False

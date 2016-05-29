#!/usr/bin/env python

import zmq
import json
import requests

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
        threat_req = requests.get("http://10.0.42.7:8888/domain/{0}/".format(domain))
        print json.loads(threat_req.text)
except KeyboardInterrupt:
    running = False

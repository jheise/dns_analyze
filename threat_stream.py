#!/usr/bin/env python

import zmq
import json
import requests

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:7777")
socket.setsockopt(zmq.SUBSCRIBE, "dns")

running = True

try:
    while running:
        msg = socket.recv()
        topic, data = msg.split(" ", 1)
        data = json.loads(data)
        domain = data["Query"]
        print "Report: {0}".format(domain)
        threat_req = requests.get("http://localhost:9999/domain/{0}/".format(domain))
        threat_data = json.loads(threat_req.text)
        print threat_data["hashes"]
        print threat_data["permalink"]
except KeyboardInterrupt:
    running = False

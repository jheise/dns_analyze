#
# Super class for analzyers
#

import json
import zmq

class Probe(object):

    def __init__(self, port):
        super(Analyzer, self).__init__()
        self.running = False
        self.port = port
        self.output_context= None
        self.output_socket = None

    def activate(self):
        self.output_context = zmq.Context()
        self.output_socket = self.output_context.socket(zmq.PUB)
        self.output_socket.bind("tcp://*:{0}".format(self.port))


    def process(self):

        msg = self.source_socket.recv()
        topic, data = msg.split(" ", 1)
        data = json.loads(data)

        data = self._analyze(data)

        self.output_socket.send(self.zmq_topic + " " + json.dumps(data))

    def deactivate(self):
        self.output_socket.close()
        self.output_context.term()

    def _analyze(self, data):
        return data

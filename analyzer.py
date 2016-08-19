#
# Super class for analzyers
#

import json
import zmq

class Analyzer(object):

    def __init__(self, zmq_host, zmq_topic, port):
        super(Analyzer, self).__init__()
        self.running = False
        self.zmq_host = zmq_host
        self.zmq_topic = zmq_topic
        self.port = port
        self.source_context = None
        self.source_socket = None
        self.output_context= None
        self.output_socket = None

    def activate(self):
        self.source_context = zmq.Context()
        self.source_socket = self.source_context.socket(zmq.SUB)
        self.source_socket.connect(self.zmq_host)
        self.source_socket.setsockopt(zmq.SUBSCRIBE, self.zmq_topic)

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
        self.source_socket.close()
        self.source_context.term()

        self.output_socket.close()
        self.output_context.term()

    def _analyze(self, data):
        return data

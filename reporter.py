#
# Super class for analzyers
#

import json
import zmq

class Reporter(object):

    def __init__(self, zmq_host, zmq_topic):
        super(Reporter, self).__init__()
        self.running = False
        self.zmq_host = zmq_host
        self.zmq_topic = zmq_topic
        self.source_context = None
        self.source_socket = None

    def activate(self):
        self.source_context = zmq.Context()
        self.source_socket = self.source_context.socket(zmq.SUB)
        self.source_socket.connect(self.zmq_host)
        self.source_socket.setsockopt(zmq.SUBSCRIBE, self.zmq_topic)

    def process(self):

        msg = self.source_socket.recv()
        topic, data = msg.split(" ", 1)
        data = json.loads(data)

        data = self._report(data)

    def deactivate(self):
        self.source_socket.close()
        self.source_context.term()

    def _report(self, data):
        pass

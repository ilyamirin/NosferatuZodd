
from programy.utils.logging.ylogger import YLogger
import socket
import json

from programy.clients.events.client import EventBotClient
from programy.clients.events.tcpsocket.config import SocketConfiguration
from programy.clients.render.json import JSONRenderer


class ClientConnection(object):

    def __init__(self, clientsocket, addr, max_buffer):
        self._clientsocket = clientsocket
        self._addr = addr
        self._max_buffer = max_buffer

    def receive_data(self):
        json_data = self._clientsocket.recv(self._max_buffer).decode()
        YLogger.debug(self, "Received: %s", json_data)
        return json.loads(json_data, encoding="utf-8")

    def send_response(self, userid, answer):
        return_payload = {"result": "OK", "answer": answer, "userid": userid}
        json_data = json.dumps(return_payload)

        YLogger.debug(self, "Sent %s:", json_data)

        self._clientsocket.send(json_data.encode('utf-8'))

    def send_error(self, error):
        if hasattr(error, 'message') is True:
            return_payload = {"result": "ERROR", "message": error.message}
        elif hasattr(error, 'msg') is True:
            return_payload = {"result": "ERROR", "message": error.msg}
        else:
            return_payload = {"result": "ERROR", "message": str(error)}

        json_data = json.dumps(return_payload)

        YLogger.debug(self, "Sent: %s", json_data)

        self._clientsocket.send(json_data.encode('utf-8'))

    def close(self):
        if self._clientsocket is not None:
            self._clientsocket.close()
            self._clientsocket = None


class SocketFactory(object):

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
        return socket.socket(family, type)


class SocketConnection(object):

    def __init__(self, host, port, queue, max_buffer=1024, factory=SocketFactory()):
        self._socket_connection = self._create_socket(host, port, queue, factory)
        self._max_buffer = max_buffer

    def _create_socket(self, host, port, queue, factory):
        # create a socket object
        serversocket = factory.create_socket()
        # bind to the port
        serversocket.bind((host, port))
        # queue up to 5 requests
        serversocket.listen(queue)
        return serversocket

    def accept_connection(self):
        # establish a connection
        clientsocket, addr = self._socket_connection.accept()
        return ClientConnection(clientsocket, addr, self._max_buffer)


class Args(object):
    def __init__(self):
        self.args = None
        self._bot_root = 'storage'
        self._logging = 'config\windows\logging.yaml'
        self._config_name = 'config\windows\config.tcp.yaml'
        self._config_format = 'yaml'
        self._no_loop = False
        self._substitutions = None

    def parse_args(self, client):
        pass

    @property
    def bot_root(self):
        return self._bot_root

    @bot_root.setter
    def bot_root(self, root):
        self._bot_root = root

    @property
    def logging(self):
        return self._logging

    @property
    def config_filename(self):
        return self._config_name

    @property
    def config_format(self):
        return self._config_format

    @property
    def noloop(self):
        return self._no_loop

    @property
    def substitutions(self):
        return self._substitutions


class EventBotClientNoCmdArgs(EventBotClient):

    def parse_arguments(self, *args, **kwargs):
        client_args = Args()
        client_args.parse_args(self)
        return client_args


class SocketBotClient(EventBotClientNoCmdArgs):

    def __init__(self, argument_parser=None):
        EventBotClient.__init__(self, "Socket", argument_parser)

        print("TCP Socket Client server now listening on %s:%d" % (self._host, self._port))
        self._server_socket = self.create_socket_connection(self._host, self._port, self._queue, self._max_buffer)

        self._renderer = JSONRenderer(self)

    def get_client_configuration(self):
        return SocketConfiguration()

    def parse_configuration(self):
        self._host = self.configuration.client_configuration.host
        self._port = self.configuration.client_configuration.port
        self._queue = self.configuration.client_configuration.queue
        self._max_buffer = self.configuration.client_configuration.max_buffer

    def extract_question(self, receive_payload):
        question = None
        if 'question' in receive_payload:
            question = receive_payload['question']
        if question is None or question == "":
            raise Exception("Clientid missing from payload")
        return question

    def extract_userid(self, receive_payload):
        userid = None
        if 'userid' in receive_payload:
            userid = receive_payload['userid']
        if userid is None or userid == "":
            raise Exception("Clientid missing from payload")
        return userid

    def create_socket_connection(self, host, port, queue, max_buffer):
        return SocketConnection(host, port, queue, max_buffer)

    def process_question(self, client_context, question):
        self._questions += 1
        return client_context.bot.ask_question(client_context, question, responselogger=self)

    def render_response(self, client_context, response):
        # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        self._client_connection.send_response(client_context.userid, response)

    def wait_and_answer(self):
        running = True
        try:
            self._client_connection = self._server_socket.accept_connection()

            receive_payload = self._client_connection.receive_data()

            question = self.extract_question(receive_payload)
            userid = self.extract_userid(receive_payload)

            client_context = self.create_client_context(userid)
            answer = self.process_question(client_context, question)

            self.render_response(client_context, answer)

        except KeyboardInterrupt:
            running = False
            YLogger.debug(self, "Cleaning up and exiting...")

        except Exception as e:
            if self._client_connection is not None:
                self._client_connection.send_error(e)

        finally:
            if self._client_connection is not None:
                self._client_connection.close()

        return running

    def set_local_property(self, property_name, property_value):
        self.client_context.brain.properties.add_property(property_name, property_value)

if __name__ == '__main__':
    print("Initiating TCP Socket Client...")

    def run():
        tcpsocket_app = SocketBotClient()
        tcpsocket_app.run()

    run()
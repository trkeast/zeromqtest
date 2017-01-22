from Client import Client
from Server import Server


class ZMQTester:
    """
        Description:
            Implements functionality of server and client for send and receive
            message from/to another processes via zeromq protocol
    """

    def __init__(self, ioprovider, name, serverUrl, clientUrl):
        """
        :param ioprovider: Instance of IOProvider
        :param name: Name of instance
        :param serverUrl: Endpoint url for server
        :param clientUrl:  Endpoint url for client
        """
        self.ioprovider = ioprovider
        self.name = name
        self.serverUrl = serverUrl
        self.clientUrl = clientUrl
        self.server = Server(serverUrl, ioprovider)
        self.client = Client(clientUrl, ioprovider)
        self.processing = False  # processing flag, if False - stop processing
        # command for handle input
        self.commands = {
            "/quit": self.stop,
            "/test": self.test
        }

    def test(self):
        """
            Write test string to std out
        """
        self.ioprovider.write("Test from ZMQTester")

    def stop(self):
        """
            Stop processing commands/messages
        """
        self.processing = False

    def process(self):
        """
            Processing messages/commands
        """
        self.server.start()  # start server thread
        self.processing = True
        while self.processing:
            message = self.ioprovider.read(
                'Enter message for sending to "%s":' % self.clientUrl)  # read message from stdin
            cmd = self.commands.get(message.lower())  # try detect command
            if not cmd:
                self.client.send(message)  # if not detects - send message
            else:
                cmd()  # else - execute command
        # stop server thread and wait until thread ends
        self.server.stop()
        self.server.join()

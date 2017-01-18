import zmq


class Client:
    """
        Description:
            Provides client of zeromq to send message to selected server
    """

    def __init__(self, url, ioprovider):
        """
            :param str url: Endpoint url for connect to remote zeromq server
            :param IOProvider ioprovider: Instance of IOProvider
        """
        self.url = url
        self.ioprovider = ioprovider

    def send(self, message):
        """
            Sends message to server
            :param message: Message to send
        """
        context = zmq.Context()
        self.ioprovider.write("Connecting to server %s" % self.url)
        socket = context.socket(zmq.REQ)
        socket.connect(self.url)
        socket.send(message)

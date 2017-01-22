import threading

import zmq


class Server(threading.Thread):
    """
        Description:
            ZeroMQ server class, started in own thread
    """

    def __init__(self, url, ioprovider):
        """
            :param url: Endpoint url for bind socket for receive messages from ZeroMQ
            :param ioprovider: Instance of IOProvider
        """
        threading.Thread.__init__(self)
        self.url = url  # endpoint url
        self.__lock = threading.Lock()  # lock for token
        self.__cancelled = False  # Cancellation token
        self.ioprovider = ioprovider  # provider for console output

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(self.url)

        with socket:
            while self.isRunning():
                message = socket.recv()  # receive message from socket
                self.ioprovider.write("Received message: %s" % message)  # print message
                socket.send("received")  # send ack

    # stop server thread via
    def stop(self):
        """
            Stops current server thread
        """
        self.ioprovider.write("Stopping...")
        with self.__lock:
            self.__cancelled = True

    # thread running flag getter, may be changed to __getattr__/__setattr__ pair
    def isRunning(self):
        """
            Returns current state of server thread: running or stopped
        """
        with self.__lock:
            return not self.__cancelled

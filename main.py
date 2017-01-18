import sys

from ConfigurationFileProvider import ConfigurationFileProvider
from IOProvider import IOProvider
from ZMQTester import ZMQTester


class CommandLine:
    """
        Description:
            Parser command line arguments
    """
    configName = 'zmqtester.cfg'  # default value of config file name
    sectionName = 'instance_1'  # default value of config section

    def process(self):
        """
            Parse cmd line arguments and set fields
        """
        cmds = {
            '--file': self.setConfigName,
            '--section': self.setSectionName
        }
        for arg in sys.argv:
            if not '=' in arg:  # if not value - skip arg
                continue
            name, value = arg.lower().split('=')  # get arg name and value
            cmd = cmds.get(name)  # try get setter
            if cmd:
                cmd(value)  # set field value

    def setConfigName(self, value):
        self.configName = value

    def setSectionName(self, value):
        self.sectionName = value


if __name__ == '__main__':
    cmdLine = CommandLine()  # command line parser
    cmdLine.process()  # parse arguments
    ioprovider = IOProvider()  # io provider

    config = ConfigurationFileProvider(source=cmdLine.configName)  # get config
    name = config.getValue(cmdLine.sectionName, 'name', 'instance')
    serverUrl = config.getValue(cmdLine.sectionName, 'localUrl', 'tcp://*:5556')
    clientUrl = config.getValue(cmdLine.sectionName, 'remoteUrl', 'tcp://localhost:5556')

    worker = ZMQTester(ioprovider, name, serverUrl, clientUrl)  # initialize tester
    worker.process()

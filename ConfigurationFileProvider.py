import ConfigParser


class ConfigurationFileProvider:
    """
        Description:
            Read values from config file
    """

    def __init__(self, source):
        """
        :param source: Path to config file
        """
        self.config = ConfigParser.RawConfigParser()
        self.config.read(source)

    def getValue(self, section, key, defaultValue=None):
        """
            Try read value from file, if no value returns defaultValue
        :param section: Section in file
        :param key: Key to read value
        :param defaultValue: Default value
        :return:
        """
        value = self.config.get(section, key)
        if not value:
            return defaultValue
        return value

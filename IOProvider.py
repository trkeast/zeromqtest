class IOProvider:
    """
        Description:
            Provide method for read/write values from/to stdin/stdout
    """

    def write(self, *args):
        """
            Print values in args to console
        """
        print ""
        for arg in args:
            print arg,
        print ""

    def read(self, prompt):
        """
            Read value string from stdin
        """
        return raw_input(prompt)

import curses

class IOProvider:
    """
        Description:
            Provide method for read/write values from/to stdin/stdout
    """

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        self.inputPromptPosition = (0, 0)
        self.outputPosition = (1, 0)

    def __raw_input(self, row, column, prompt_string):
        # non blocking input function for read string from stdin
        curses.echo()
        self.stdscr.nodelay(1)
        self.stdscr.addstr(row, column, prompt_string)
        result = []
        key = None
        while True:
            key = self.stdscr.getch()
            if key == curses.KEY_ENTER or key == 10:  # curses ENTER code
                break
            if key > 0:
                result.append(chr(key))
        res = ''.join(result)
        return res

    def write(self, *args):
        """
            Print values in args to console
        """
        y, x = self.stdscr.getyx()  # workaround - save original cursor position for restore in future
        self.stdscr.refresh()
        valstring = " ".join(args)
        self.stdscr.addstr(self.outputPosition[0], self.outputPosition[1], valstring)
        self.stdscr.move(y, x)  # workaround - return input cursor to original position

    def read(self, prompt):
        """
            Read value string from stdin
        """
        return self.__raw_input(self.inputPromptPosition[0], self.inputPromptPosition[1], prompt)

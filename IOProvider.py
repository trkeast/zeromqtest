import curses
from collections import namedtuple

class IOProvider:
    """
        Description:
            Provide method for read/write values from/to stdin/stdout
    """

    def __init__(self):
        self.stdscr = curses.initscr()
        Point = namedtuple('Point', "y x")
        self.windowSize = Point(*self.stdscr.getmaxyx())
        self.inputPromptPosition = Point(self.windowSize.y - 1, 0)
        self.outputPosition = Point(self.windowSize.y - 2, 0)
        self.stdscr.scrollok(True)
        self.stdscr.setscrreg(0, self.outputPosition.y)

    def __raw_input(self, row, column, prompt_string):
        # non blocking input function for read string from stdin
        curses.echo()
        self.stdscr.nodelay(1)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
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
        valstring = " ".join(args)
        y, x = self.stdscr.getyx()  # workaround - save original cursor position for restore in future
        valstring = " ".join(args)
        self.stdscr.addstr(self.outputPosition.y, self.outputPosition.x, valstring)
        self.stdscr.scroll(1)
        self.stdscr.move(y, x)  # workaround - return input cursor to original position

    def read(self, prompt):
        """
            Read value string from stdin
        """
        return self.__raw_input(self.inputPromptPosition.y, self.inputPromptPosition.x, prompt)

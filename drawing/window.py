import curses
from terminal_pen import TerminalPen
class Window:
    def __enter__(self):
        self.stdscr = curses.initscr()
        self.pen = TerminalPen(self.stdscr)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        return self.stdscr

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()



    def getch(self):
        return self.stdscr.getch()

    def refresh(self):
        self.stdscr.refresh()

    def clear(self):
        self.stdscr.clear()

    def addstr(self, y, x, string):
        self.stdscr.addstr(y, x, string)

    def addch(self, y, x, char):
        self.stdscr.addch(y, x, char)

    def getmaxyx(self):
        return self.stdscr.getmaxyx()

    def getbegyx(self):
        return self.stdscr.getbegyx()

    def getyx(self):
        return self.stdscr.getyx()

    def move(self, y, x):
        self.stdscr.move(y, x)

import curses

from duro.__init__ import __title__, __version__


def display_footer(screen, config):
    h, w = screen.getmaxyx()

    win = curses.newwin(1, w, h - 1, 0)
    win.bkgd(' ', config.get_color("footer"))
    win.addstr(0, 1, "Press ? for Help")
    x = w - 1

    for item in ["v" + __version__, __title__]:
        x -= len(item) + 1
        win.addstr(0, x, item)

    screen.refresh()
    win.refresh()

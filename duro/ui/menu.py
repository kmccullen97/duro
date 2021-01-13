import curses

from ..cmds.menu import menu_commands


class Menu:
    def __init__(self, title, none_text, h, w, y, x, items, display_item,
                 config):
        self.active = 0
        self.top = 0
        self.title = title
        self.none_text = none_text
        self.h = h
        self.w = w
        self.items = items
        self.display_item = display_item
        self.config = config
        self.win = curses.newwin(h, w, y, x)
        self.win.keypad(True)
        self.win.box()
        self.win.addstr(0, 2, title)
        self.display_win = curses.newwin(h - 2, w - 2, y + 1, x + 1)
        self.win.refresh()
        self.refresh = False

    def display(self, items=None):
        if items is not None:
            self.items = items
        if self.refresh:
            self.display_win.clear()
            self.active = min(self.active, len(self.items) - 1, 0)
            self.refresh = False

        if len(self.items) == 0:
            self.display_win.addstr(0, 0, self.none_text,
                                    self.config.get_color("none"))
            return self.display_win.getch()

        for i, item in enumerate(self.items[self.top:self.top + self.h - 2]):
            is_active = i + self.top == self.active
            self.display_item(self.display_win, i, item, is_active)

        key = self.display_win.getch()

        if key in menu_commands["down"]["keys"]:
            if self.active < len(self.items) - 1:
                self.active += 1
                if self.active > self.top + self.h - 3:
                    self.top += 1
                    self.refresh = True
        elif key in menu_commands["up"]["keys"]:
            if self.active > 0:
                self.active -= 1
                if self.active < self.top:
                    self.top -= 1
                    self.refresh = True

        return key

    def update_active(self):
        self.active = min(self.active, len(self.items) - 1)

    def set_active_max(self):
        self.active = len(self.items) - 1
        if self.top != 0:
            self.top = self.active - self.h - 3

    @property
    def active_item(self):
        return self.items[self.active]

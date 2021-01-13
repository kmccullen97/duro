import curses
import re


class Form:
    def __init__(self, screen, title, ok_label="Ok"):
        self.screen = screen
        self.title = title
        self.loop = True
        self.submitted = False
        self.fields = []
        self.options = []
        self.longest_label = 0
        self.spacing = 4
        self.padding = 2
        self.win_w = max(20, len(title) + 4)
        self.cur_y = 0
        self.cur_x = 0
        self.current_field = 0
        self.current_option = 0
        self.is_field_active = False
        self.char_re = r'[A-Za-z0-9 !@#$%^&*(){}|;\':",./<>?`~[\]-_]'
        self.add_option("Cancel", cancel=True)
        self.add_option(ok_label, ok=True)

    def add_field(self, label, length, value=""):
        self.fields.append({"label": label, "length": length, "value": value})
        self.longest_label = max(self.longest_label, len(label))
        self.win_w = max(self.win_w, len(label) + self.spacing + length)

    def add_option(self, label, ok=False, cancel=False):
        self.options.insert(0, {
            "label": label,
            "ok": ok,
            "cancel": cancel,
        })

    def init_win(self):
        self.win_w += self.padding * 2
        h = (len(self.fields) + self.padding) * 2 + 1
        mh, mw = self.screen.getmaxyx()
        y = (mh - h) // 2
        x = (mw - self.win_w) // 2

        self.win = curses.newwin(h, self.win_w, y, x)
        self.win.box()

    def cur_x_max(self):
        field = self.fields[self.current_field]
        return self.cur_x_min + min(len(field["value"]), field["length"] - 1)

    def handle_input(self, key):
        if self.is_field_active:
            if key == curses.KEY_DOWN or key in [curses.KEY_ENTER, 10]:
                if self.current_field == len(self.fields) - 1:
                    self.is_field_active = False
                else:
                    self.current_field += 1
                    self.cur_x = self.cur_x_max()
            elif key == curses.KEY_UP:
                if self.is_field_active:
                    if self.current_field > 0:
                        self.current_field -= 1
                        self.cur_x = self.cur_x_max()
            elif key == curses.KEY_LEFT:
                if self.cur_x > self.cur_x_min:
                    self.cur_x -= 1
            elif key == curses.KEY_RIGHT:
                if self.cur_x < self.cur_x_max():
                    self.cur_x += 1
            elif key == curses.KEY_BACKSPACE:
                if self.cur_x > self.cur_x_min:
                    field = self.fields[self.current_field]
                    index = self.cur_x - self.cur_x_min
                    if len(field["value"]) == field["length"]:
                        index += 1
                    else:
                        self.cur_x -= 1
                    field["value"] = field["value"][:index -
                                                    1] + field["value"][index:]
            else:
                field = self.fields[self.current_field]
                if len(field["value"]) < field["length"]:
                    if re.match(self.char_re, chr(key)):
                        index = self.cur_x - self.cur_x_min
                        field["value"] = field["value"][:index] + chr(
                            key) + field["value"][index:]
                        if len(field["value"]) < field["length"]:
                            self.cur_x += 1
        else:
            if key == curses.KEY_UP:
                self.is_field_active = True
            elif key == curses.KEY_LEFT:
                if self.current_option < len(self.options) - 1:
                    self.current_option += 1
            elif key == curses.KEY_RIGHT:
                if self.current_option > 0:
                    self.current_option -= 1
            elif key in [curses.KEY_ENTER, 10]:
                option = self.options[self.current_option]
                if option["ok"]:
                    self.submitted = True
                    self.loop = False
                elif option["cancel"]:
                    self.loop = False

    def edit(self):
        self.init_win()
        self.win.keypad(True)
        self.win.addstr(0, 2, self.title)

        self.cur_x_min = self.longest_label + self.spacing + self.padding
        if len(self.fields) > 0:
            self.cur_x = self.cur_x_max()
            self.is_field_active = True

        while self.loop:
            curses.curs_set(1 if self.is_field_active else 0)
            self.cur_y = (self.current_field * 2) + self.padding
            for i, field in enumerate(self.fields):
                value = field["value"] + " " * (field["length"] -
                                                len(field["value"]))
                self.win.addstr((i * 2) + self.padding, self.padding,
                                field["label"] + ":")
                self.win.addstr((i * 2) + self.padding, self.cur_x_min, value,
                                curses.A_UNDERLINE)

            option_x = self.win_w - self.padding
            options_y = (self.padding + len(self.fields) - 1) * 2
            for i, option in enumerate(self.options):
                attr = curses.A_NORMAL
                if i == self.current_option and not self.is_field_active:
                    attr = curses.A_REVERSE
                option_x -= len(option["label"])
                self.win.addstr(options_y, option_x, option["label"], attr)
                option_x -= 1
            self.win.move(self.cur_y, self.cur_x)

            key = self.win.getch()

            self.handle_input(key)

        self.win.keypad(False)
        return self.submitted

    def get_value(self, label):
        for field in self.fields:
            if field["label"] == label:
                return field["value"]
        return None

    def clear(self):
        self.win.clear()
        self.win.refresh()

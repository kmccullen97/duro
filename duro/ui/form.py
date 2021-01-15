import curses
import re

from duro.commands import Commands
from duro.cmds.form import form_commands


class Form:
    def __init__(self, screen, config, title, ok_label="Ok"):
        self.screen = screen
        self.commands = Commands(form_commands, config)
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

    def init_win(self):
        self.win_w += self.padding * 2 + 5
        h = (len(self.fields) + self.padding) * 2 + 1
        mh, mw = self.screen.getmaxyx()
        y = (mh - h) // 2
        x = (mw - self.win_w) // 2

        self.win = curses.newwin(h, self.win_w, y, x)
        self.win.box()

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

            self.display()
            self.win.move(self.cur_y, self.cur_x)

            key = self.win.getch()
            if self.is_field_active:
                self.handle_fields_input(key)
            else:
                self.handle_options_input(key)

        return self.submitted

    def display(self):
        for i, field in enumerate(self.fields):
            text = field["value"][field["offset"]:field["offset"] +
                                  field["length"]]
            value = text + " " * (field["length"] - len(text))
            self.win.addstr((i * 2) + self.padding, self.padding,
                            field["label"] + ":")
            self.win.addstr((i * 2) + self.padding, self.cur_x_min, value,
                            curses.A_UNDERLINE)

            self.win.addstr(" [{:3d}]".format(len(field["value"])))

        option_x = self.win_w - self.padding
        options_y = (self.padding + len(self.fields) - 1) * 2
        for i, option in enumerate(self.options):
            attr = curses.A_NORMAL
            if i == self.current_option and not self.is_field_active:
                attr = curses.A_REVERSE
            option_x -= len(option["label"])
            self.win.addstr(options_y, option_x, option["label"], attr)
            option_x -= 1

    def handle_fields_input(self, key):
        if self.commands.check("next", key):
            if self.current_field == len(self.fields) - 1:
                self.is_field_active = False
            else:
                self.current_field += 1
                self.cur_x = self.cur_x_max()
        elif self.commands.check("previous", key):
            if self.is_field_active:
                if self.current_field > 0:
                    self.current_field -= 1
                    self.cur_x = self.cur_x_max()
        elif self.commands.check("left", key):
            if self.cur_x > self.cur_x_min:
                self.cur_x -= 1
            elif self.field["offset"] > 0:
                self.field["offset"] -= 1
        elif self.commands.check("right", key):
            if self.cur_x < self.cur_x_max():
                self.cur_x += 1
            elif len(self.field["value"]
                     ) - self.field["offset"] > self.field["length"]:
                self.field["offset"] += 1
        elif self.commands.check("backspace", key):
            index = self.field["offset"] + self.cur_x - self.cur_x_min
            if index > 0:
                self.field["value"] = self.field[
                    "value"][:index - 1] + self.field["value"][index:]
                if self.cur_x > self.cur_x_min:
                    self.cur_x -= 1
                else:
                    self.field["offset"] -= 1
        else:
            if re.match(self.char_re, chr(key)):
                index = self.field["offset"] + self.cur_x - self.cur_x_min
                self.field["value"] = self.field["value"][:index] + chr(
                    key) + self.field["value"][index:]
                if self.cur_x + 1 > self.cur_x_min + self.field["length"]:
                    self.field["offset"] += 1
                else:
                    self.cur_x += 1

    def handle_options_input(self, key):
        if self.commands.check("previous", key):
            self.is_field_active = True
        elif self.commands.check("left", key):
            if self.current_option < len(self.options) - 1:
                self.current_option += 1
        elif self.commands.check("right", key):
            if self.current_option > 0:
                self.current_option -= 1
        elif self.commands.check("submit", key):
            option = self.options[self.current_option]
            if option["ok"]:
                self.submitted = True
                self.loop = False
            elif option["cancel"]:
                self.loop = False

    def add_field(self, label, length, value=""):
        self.fields.append({
            "label": label,
            "length": length,
            "value": value,
            "offset": 0
        })
        self.longest_label = max(self.longest_label, len(label))
        self.win_w = max(self.win_w, len(label) + self.spacing + length)

    def add_option(self, label, ok=False, cancel=False):
        self.options.insert(0, {
            "label": label,
            "ok": ok,
            "cancel": cancel,
        })

    def cur_x_max(self):
        return self.cur_x_min + min(
            len(self.field["value"]) - self.field["offset"],
            self.field["length"])

    def get_value(self, label):
        for field in self.fields:
            if field["label"] == label:
                return field["value"]
        return None

    @property
    def field(self):
        return self.fields[self.current_field]

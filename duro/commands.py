import curses

from duro.ui.menu import Menu


class Commands:
    def __init__(self, commands, config):
        self.commands = commands
        self.config = config
        self.spacing = 2
        longest_key_names = 0
        longest_description = 0

        for command in commands.values():
            keys = command["keys"]
            if type(keys) is str:
                key_names = keys
            else:
                key_names = command["key_names"]
            longest_key_names = max(longest_key_names, len(key_names))
            longest_description = max(longest_description,
                                      len(command["description"]))

        self.longest_key_names = longest_key_names
        self.longest_description = longest_description
        self.h = len(commands.keys()) + 2
        self.w = longest_key_names + self.spacing + longest_description + 2

    def check(self, name, key):
        keys = self.commands[name]["keys"]
        if type(keys) is str:
            return key == ord(keys)
        else:
            return key in keys

    def display_command(self, win, i, command, is_active):
        attr = curses.A_NORMAL
        if is_active:
            attr = self.config.active
        key_names = command["keys"] if type(
            command["keys"]) is str else command["key_names"]
        win.addstr(
            i, 0, key_names + " " *
            (self.longest_key_names + self.spacing - len(key_names)) +
            command["description"], attr)

    def display_help(self, screen):
        mh, mw = screen.getmaxyx()
        y = (mh - self.h) // 2
        x = (mw - self.w) // 2

        commands = []
        for key in self.commands.keys():
            commands.append(self.commands[key])

        menu = Menu("Help", "No commands.", self.h, self.w, y, x, commands,
                    self.display_command, self.config)
        while True:
            key = menu.display()

            if key == ord('q'):
                break

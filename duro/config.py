import curses
import yaml
import os
import datetime

from duro.__init__ import __title__

color_codes = {
    "black": curses.COLOR_BLACK,
    "blue": curses.COLOR_BLUE,
    "cyan": curses.COLOR_CYAN,
    "green": curses.COLOR_GREEN,
    "magenta": curses.COLOR_MAGENTA,
    "red": curses.COLOR_RED,
    "white": curses.COLOR_WHITE,
    "yellow": curses.COLOR_YELLOW
}

attr_codes = {
    "normal": curses.A_NORMAL,
    "bold": curses.A_BOLD,
    "reverse": curses.A_REVERSE
}

default_config = {
    "colors": {
        "default": ["white", -1, 0],
        "none": ["yellow", -1, 0],
        "id": ["cyan", -1, 0],
        "date": ["yellow", -1, 0],
        "footer": ["white", "magenta", 0],
        "active_list": ["cyan", -1, 0],
        "active_card": ["cyan", -1, 0]
    },
    "date_format": '%b %d, %Y %I:%M %p',
    "active": "bold",
    "min_list_width": 50
}


class Config:
    def __init__(self):
        config_path = Config.get_config_path()
        config_file = os.path.join(config_path, "config.yml")

        config = default_config
        data_path = Config.get_data_path()
        config["data_file"] = os.path.join(data_path, "data.db")

        if not os.path.isdir(config_path):
            os.mkdir(config_path)

        if not os.path.isdir(data_path):
            os.mkdir(data_path)

        if os.path.isfile(config_file):
            with open(config_file, "r") as f:
                user_config = yaml.load(f.read(), Loader=yaml.Loader)
                colors = config["colors"]
                config = {**config, **user_config}
                if "colors" in user_config:
                    config["colors"] = {**colors, **user_config["colors"]}

        self.data_file = config["data_file"]
        self.date_format = config["date_format"]
        self.active = Config.parse_color(attr_codes, config["active"])
        self.min_list_width = config["min_list_width"]

        self.load_color_theme(config["colors"])

    def load_color_theme(self, color_theme, fg=curses.COLOR_WHITE, bg=-1):
        self.colors = {}

        for i, key in enumerate(color_theme.keys()):
            value = color_theme[key]
            value[0] = Config.parse_color(color_codes, value[0])
            value[1] = Config.parse_color(color_codes, value[1])
            value[2] = Config.parse_color(attr_codes, value[2])
            curses.init_pair(i + 1, value[0] or fg, value[1] or bg)
            self.colors[key] = curses.color_pair(i + 1) | (value[2]
                                                           or curses.A_NORMAL)

    def get_color(self, key):
        return self.colors[key]

    def format_date(self, date):
        return datetime.datetime.fromtimestamp(date).strftime(self.date_format)

    @staticmethod
    def get_config_path():
        folder = os.path.join(os.path.expanduser("~"), ".config", __title__)

        if "ENV" in os.environ and os.environ["ENV"] == "dev":
            folder = "./data/"

        return folder

    @staticmethod
    def get_data_path():
        folder = os.path.join(os.path.expanduser("~"), ".local", "share",
                              __title__)

        if "ENV" in os.environ and os.environ["ENV"] == "dev":
            folder = "./data/"

        return folder

    @staticmethod
    def parse_color(codes, value):
        return codes[value] if type(value) is str else value

import argparse
import os
import curses

from duro.__init__ import __title__, __version__, __description__
from duro.config import Config
from duro.main import main


def run():
    parser = argparse.ArgumentParser(prog=__title__,
                                     description=__description__)
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=f"v{__version__}")
    parser.add_argument("-c",
                        "--config-path",
                        help="show path to config file",
                        action="store_true")

    args = parser.parse_args()

    if args.config_path:
        print(os.path.join(Config.get_config_path(), "config.yml"))
    else:
        curses.wrapper(main)


if __name__ == '__main__':
    run()

import os
import sys

sys.path.append(os.getcwd())

from duro.cmds.main import main_commands
from duro.cmds.boards import boards_menu_commands

spacing = 4


def get_commands_text(commands):
    longest_key_names = 0

    for command in commands.values():
        key_names = command["keys"] if type(
            command["keys"]) == str else command["key_names"]
        longest_key_names = max(longest_key_names, len(key_names))

    text = ""

    for command in commands.values():
        key_names = command["keys"] if type(
            command["keys"]) == str else command["key_names"]
        text += key_names
        text += " " * (longest_key_names - len(key_names) + spacing)
        text += command["description"]
        text += "\n"
    return text


with open("./scripts/commands-template.md", "r") as f:
    md = f.read()

md = md.replace("MAIN_COMMANDS", get_commands_text(main_commands))
md = md.replace("BOARDS_MENU_COMMANDS",
                get_commands_text(boards_menu_commands))

with open("./docs/commands.md", "w") as f:
    f.write(md)

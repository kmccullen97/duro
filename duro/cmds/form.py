import curses

form_commands = {
    "next": {
        "keys": [curses.KEY_DOWN, curses.KEY_ENTER, 10],
        "description": "move to next field or options",
        "key_names": "down, enter"
    },
    "previous": {
        "keys": [curses.KEY_UP],
        "description": "move to previous field or options",
        "key_names": "up"
    },
    "left": {
        "keys": [curses.KEY_LEFT],
        "description": "move cursor left, or option left",
        "key_names": "left"
    },
    "right": {
        "keys": [curses.KEY_RIGHT],
        "description": "move cursor right, or option right",
        "key_names": "right"
    },
    "backspace": {
        "keys": [curses.KEY_BACKSPACE],
        "description": "backspace",
        "key_names": "backspace"
    },
    "submit": {
        "keys": [curses.KEY_ENTER, 10],
        "description": "submit form if on option",
        "key_names": "enter"
    },
    "help": {
        "keys": "?",
        "description": "help"
    }
}

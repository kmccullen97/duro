import curses

menu_commands = {
    "up": {
        "keys": [ord('k'), curses.KEY_UP],
        "description": "move active up",
        "key_names": "k, up"
    },
    "down": {
        "keys": [ord('j'), curses.KEY_DOWN],
        "description": "move active down",
        "key_names": "j, down"
    }
}

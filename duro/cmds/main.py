import curses

main_commands = {
    "boards.view": {
        "keys": "b",
        "description": "view all boards"
    },
    "lists.new": {
        "keys": "c",
        "description": "add list"
    },
    "lists.active.left": {
        "keys": [ord('h'), curses.KEY_LEFT],
        "description": "list active left",
        "key_names": "h, left"
    },
    "lists.active.right": {
        "keys": [ord('l'), curses.KEY_RIGHT],
        "description": "list active right",
        "key_names": "l, right"
    },
    "lists.move.left": {
        "keys": "u",
        "description": "move list left"
    },
    "lists.move.right": {
        "keys": "i",
        "description": "move list right"
    },
    "lists.delete": {
        "keys": "x",
        "description": "delete list"
    },
    "cards.view": {
        "keys": "v",
        "description": "view card"
    },
    "cards.new": {
        "keys": "n",
        "description": "add card"
    },
    "cards.edit": {
        "keys": "e",
        "description": "edit card"
    },
    "cards.delete": {
        "keys": "d",
        "description": "delete card"
    },
    "cards.active.up": {
        "keys": [ord('k'), curses.KEY_UP],
        "description": "card active up",
        "key_names": "k"
    },
    "cards.active.down": {
        "keys": [ord('j'), curses.KEY_DOWN],
        "description": "card active down",
        "key_names": "j"
    },
    "cards.move.up": {
        "keys": "r",
        "description": "move card up"
    },
    "cards.move.down": {
        "keys": "f",
        "description": "move card down"
    },
    "cards.move.next": {
        "keys": "p",
        "description": "move card to next list"
    },
    "cards.move.previous": {
        "keys": "o",
        "description": "move card to previous list"
    },
    "help": {
        "keys": "?",
        "description": "help"
    },
    "quit": {
        "keys": "q",
        "description": "quit"
    }
}

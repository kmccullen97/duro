from .menu import menu_commands

boards_menu_commands = {
    **menu_commands,
    **{
        "board.open": {
            "keys": "o",
            "description": "open board"
        },
        "boards.new": {
            "keys": "n",
            "description": "new board"
        },
        "board.delete": {
            "keys": "d",
            "description": "delete board"
        },
        "board.edit": {
            "keys": "e",
            "description": "edit board"
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
}

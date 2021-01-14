import curses

from duro.config import Config
from duro.database import Database
from duro.boards_menu import BoardsMenu
from duro.commands import Commands
from duro.cmds.main import main_commands
from duro.board_ui import BoardUI
from duro.footer import display_footer


def main(screen):
    curses.curs_set(0)
    curses.use_default_colors()
    mh, mw = screen.getmaxyx()

    config = Config()
    db = Database(config.data_file)
    boards_menu = BoardsMenu(screen, config, db)
    commands = Commands(main_commands, config)
    board_ui = BoardUI(config, db, commands, mh - 1, mw)
    display_footer(screen, config)

    while True:
        board_ui.display()

        key = board_ui.win.getch()

        if commands.check("quit", key):
            break
        elif commands.check("help", key):
            commands.display_help(screen)
            board_ui.should_refresh = True
        elif commands.check("boards.view", key):
            board_id = boards_menu.display()
            if board_id:
                db.open_board(board_id)
            board_ui.new_board_open()
            board_ui.should_refresh = True
        elif board_ui.board is not None:
            board_ui.handle_input(key)

    db.close()

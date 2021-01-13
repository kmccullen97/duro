import curses

from duro.commands import Commands
from duro.cmds.boards import boards_menu_commands
from duro.ui.menu import Menu
from duro.ui.form import Form


class BoardsMenu:
    def __init__(self, screen, config, db):
        self.screen = screen
        self.config = config
        self.db = db
        self.commands = Commands(boards_menu_commands, config)

    def display_board(self, win, i, board, is_active):
        attr = curses.A_NORMAL
        if is_active:
            attr = self.config.active
        win.addstr(i, 0, "#" + str(board.id) + " ",
                   self.config.get_color("id") | attr)
        win.addstr(board.name + " ", self.config.get_color("default") | attr)
        win.addstr(self.config.format_date(board.date),
                   self.config.get_color("date") | attr)

    def display(self):
        mh, mw = self.screen.getmaxyx()
        h, w = 25, 80
        y = (mh - h) // 2
        x = (mw - w) // 2
        menu = Menu("Boards", "No boards yet.", h - 1, w, y, x,
                    self.db.fetch_boards(), self.display_board, self.config)

        while True:
            key = menu.display(self.db.fetch_boards())

            if self.commands.check("quit", key):
                break
            elif self.commands.check("help", key):
                self.commands.display_help(self.screen)
                menu.refresh = True
            elif self.commands.check("boards.new", key):
                board_name = self.board_form("New Board")
                if board_name:
                    self.db.add_board(board_name)
                menu.refresh = True
            elif self.commands.check("board.delete", key):
                form = Form(self.screen, "Confirm Delete", ok_label="Delete")
                form.current_option = 1
                if form.edit():
                    self.db.delete_board(menu.active_item.id)
                menu.refresh = True
            elif self.commands.check("board.edit", key):
                new_board_name = self.board_form("Edit Board",
                                                 menu.active_item.name)
                if new_board_name:
                    self.db.update_board_name(menu.active_item.id,
                                              new_board_name)
                menu.refresh = True
            elif self.commands.check("board.open", key):
                return menu.active_item.id

    def board_form(self, title, value=""):
        form = Form(self.screen, title)
        form.add_field("Name", 30, value)

        name = ""
        if form.edit():
            name = form.get_value("Name")
        form.clear()
        return name

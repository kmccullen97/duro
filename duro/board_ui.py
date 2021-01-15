import curses
import curses.textpad

from duro.ui.form import Form


class BoardUI:
    def __init__(self, config, db, commands, h, w):
        self.config = config
        self.db = db
        self.commands = commands
        self.h = h
        self.w = w

        self.should_refresh = True
        self.win = curses.newwin(h, w, 0, 0)
        self.new_board_open()

    def display(self):
        if not self.should_refresh:
            return
        self.should_refresh = False

        self.win.clear()

        if not self.board:
            self.win.addstr(0, 0, "No board selected.",
                            self.config.get_color("none"))
            return

        self.win.addstr(self.board.name, self.config.get_color("default"))
        lists_bar = "["
        lists_bar += "." * self.list_offset
        lists_bar += "X" * self.num_cols
        lists_bar += "." * (len(self.board.lists) - self.list_offset -
                            self.num_cols)
        lists_bar += "]"
        self.win.addstr(0, self.w - len(lists_bar) - 3, lists_bar,
                        self.config.get_color("default"))

        self.display_lists()

    def display_lists(self):
        list_width = max(self.w // self.num_cols - 1,
                         self.config.min_list_width)
        for i, list_item in enumerate(
                self.board.lists[self.list_offset:self.num_cols +
                                 self.list_offset]):
            is_list_active = i + self.list_offset == self.active_list
            list_item.display(self.win, list_width, self.config, i, self.h,
                              is_list_active)

    def handle_input(self, key):
        if self.commands.check("lists.new", key):
            form = Form(self.win, self.config, "New List")
            form.add_field("Name", 30)
            if form.edit():
                self.db.add_list(self.board.id, form.get_value("Name"))
            self.refresh_board()
            self.should_refresh = True
        elif self.commands.check("lists.active.left", key):
            self.set_active_list(-1)
        elif self.commands.check("lists.active.right", key):
            self.set_active_list(1)
        elif self.commands.check("lists.move.left", key):
            if self.active_list > 0:
                self.reorder_list(-1)
        elif self.commands.check("lists.move.right", key):
            if self.active_list < len(self.board.lists) - 1:
                self.reorder_list(1)
        elif self.commands.check("lists.delete", key):
            form = Form(self.win,
                        self.config,
                        "Confirm Delete List",
                        ok_label="Delete")
            form.current_option = 1
            if form.edit():
                self.db.delete_list(self.board.lists[self.active_list].id)
                self.refresh_board()
                if self.active_list > len(self.board.lists) - 1:
                    self.set_active_list(-1)
            self.should_refresh = True
        elif self.commands.check("cards.view", key):
            self.view_card()
            self.should_refresh = True
        elif self.commands.check("cards.new", key):
            name = self.card_form("New Card")
            if name:
                self.db.add_card(self.board.lists[self.active_list].id, name)
                self.refresh_board()
            self.should_refresh = True
        elif self.commands.check("cards.edit", key):
            name = self.card_form("Edit Card",
                                  self.active_list_item.card_item().name)
            if name:
                self.db.edit_card(self.active_list_item.card_item().id, name)
                self.refresh_board()
            self.should_refresh = True
        elif self.commands.check("cards.delete", key):
            form = Form(self.win,
                        self.config,
                        "Confirm Delete Card",
                        ok_label="Delete")
            form.current_option = 1
            if form.edit():
                self.db.delete_card(self.active_list_item.card_item().id)
                self.refresh_board()
            self.should_refresh = True
        elif self.commands.check("cards.move.next", key):
            if self.active_list < len(self.board.lists) - 1:
                self.db.move_cards_list(
                    self.active_list_item.card_item().id,
                    self.board.lists[self.active_list + 1].id)
                self.board.lists[self.active_list].refresh_cards()
                self.board.lists[self.active_list + 1].refresh_cards()
                self.active_list += 1
                self.should_refresh = True
        elif self.commands.check("cards.move.previous", key):
            if self.active_list > 0:
                self.db.move_cards_list(
                    self.active_list_item.card_item().id,
                    self.board.lists[self.active_list - 1].id)
                self.active_list_item.refresh_cards()
                self.board.lists[self.active_list - 1].refresh_cards()
                self.active_list -= 1
                self.should_refresh = True

        self.should_refresh = self.active_list_item.handle_input(
            self.commands, key) or self.should_refresh

    def card_form(self, title, value=""):
        form = Form(self.win, self.config, title)
        form.add_field("Name", 50, value)
        if form.edit():
            return form.get_value("Name")

    def reorder_list(self, diff):
        self.db.reorder_list(self.board.lists[self.active_list],
                             self.board.lists[self.active_list + diff])
        self.set_active_list(diff)
        self.refresh_board()
        self.should_refresh = True

    def set_active_list(self, diff):
        new_active_list = self.active_list + diff
        if new_active_list >= 0 and new_active_list < len(self.board.lists):
            self.active_list = new_active_list
            if self.active_list < self.list_offset or self.list_offset + self.num_cols > len(
                    self.board.lists):
                self.list_offset -= 1
            elif self.active_list > self.list_offset + self.num_cols - 1:
                self.list_offset += 1
            active_list_cards_len = len(
                self.board.lists[self.active_list].cards)
            if active_list_cards_len > 0:
                self.active_list_item.active_card = min(
                    active_list_cards_len - 1,
                    self.active_list_item.active_card)
            self.should_refresh = True

    def view_card(self):
        card = self.active_list_item.card_item()
        w = 50
        h = card.get_card_details_height(w - 4) + 4
        y = (self.h - h) // 2
        x = (self.w - w) // 2
        card_win = curses.newwin(h, w, y, x)
        card_win.box()
        card_win.addstr(0, 2, "Card Details")
        card_content = curses.newwin(h - 4, w - 4, y + 2, x + 2)
        card_content.addstr(card.name + "\n", self.config.get_color("default"))
        card_content.addstr(self.config.format_date(card.date),
                            self.config.get_color("date"))
        self.win.refresh()
        card_win.refresh()
        while True:
            card_key = card_content.getch()
            if card_key == ord('q'):
                break

    @property
    def active_list_item(self):
        return self.board.lists[self.active_list]

    def new_board_open(self):
        self.list_offset = 0
        self.active_list = 0
        self.num_cols = 0
        self.refresh_board()

    def refresh_board(self):
        self.board = self.db.fetch_open_board()
        self.update_num_cols()

    def update_num_cols(self):
        if not self.board or not self.board.lists:
            return
        self.num_cols = min(self.w // self.config.min_list_width,
                            len(self.board.lists))

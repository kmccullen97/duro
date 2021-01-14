import curses
import curses.textpad


class ListUI:
    def __init__(self, values, cards, db):
        self.id = values[0]
        self.name = values[1]
        self.board_id = values[2]
        self.pos = values[3]
        self.cards = cards
        self.db = db
        self.card_offset = 0
        self.active_card = 0
        self.h = 1
        self.w = 1

    def display(self, win, list_width, config, i, h, is_list_active):
        self.h = h
        self.w = list_width - 2
        self.update_num_cards()
        start_x = list_width * i

        if is_list_active:
            win.attron(config.get_color("active_list"))

        curses.textpad.rectangle(win, 1, start_x, h - 1, start_x + list_width)
        win.addstr(1, start_x + 2, self.name)
        if len(self.cards) > self.num_cards:
            win.addstr(
                h - 1, start_x + 2,
                f"{self.card_offset+1} - {self.card_offset+self.num_cards} of {len(self.cards)}"
            )

        if is_list_active:
            win.attroff(config.get_color("active_list"))

        self.display_cards(win, h, list_width - 2, start_x + 1, is_list_active,
                           config)

    def display_cards(self, win, h, w, x, is_list_active, config):
        y = 3
        displayed_cards = self.cards[self.card_offset:self.card_offset +
                                     self.num_cards]
        for i, card in enumerate(displayed_cards):
            card_height = card.get_card_height(w - 1)
            if y + card_height > h - 1:
                break
            card_win = curses.newwin(card_height, w - 1, y, x + 1)
            card_win.addstr(0, 0, card.name, config.get_color("default"))
            is_card_active = is_list_active and i + self.card_offset == self.active_card
            if is_card_active:
                win.attron(config.get_color("active_card"))
            curses.textpad.rectangle(win, y - 1, x, y + card_height, x + w)
            if is_card_active:
                win.attroff(config.get_color("active_card"))

            win.refresh()
            card_win.refresh()
            y += card_height + 2

    def handle_input(self, commands, key):
        if commands.check("cards.active.up", key):
            if self.active_card > 0:
                self.active_card -= 1
                if self.active_card < self.card_offset:
                    self.card_offset -= 1
                self.update_num_cards()
                return True
        elif commands.check("cards.active.down", key):
            if self.active_card < len(self.cards) - 1:
                self.active_card += 1
                if self.active_card > self.card_offset + self.num_cards - 1:
                    self.card_offset += 1
                self.update_num_cards()
                return True
        elif commands.check("cards.move.up", key):
            if self.active_card > 0:
                self.db.move_card(self.card_item(), self.card_item(-1))
                self.active_card -= 1
                self.refresh_cards()
                return True
        elif commands.check("cards.move.down", key):
            if self.active_card < len(self.cards) - 1:
                self.db.move_card(self.card_item(), self.card_item(1))
                self.active_card += 1
                self.refresh_cards()
                return True

        return False

    def refresh_cards(self):
        self.cards = self.db.fetch_cards(self.id)
        self.update_num_cards()

    def update_num_cards(self):
        self.num_cards = len(self.cards) - self.card_offset
        h = 0
        for i, card in enumerate(self.cards[self.card_offset:]):
            card_height = card.get_card_height(self.w) + 2
            if h + card_height >= self.h - 2:
                self.num_cards = i
                break
            h += card_height

    def card_item(self, diff=0):
        return self.cards[self.active_card + diff]

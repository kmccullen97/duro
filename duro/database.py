import sqlite3
import datetime

from duro.models.board import BoardItem
from duro.list_ui import ListUI
from duro.models.card import CardItem


class Database:
    def __init__(self, data_file):
        self.data_file = data_file
        self.conn = sqlite3.connect(self.data_file)
        self.conn.execute("PRAGMA foreign_keys = ON")
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS boards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date INTEGER,
                open INTEGER
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                board_id INTEGER,
                pos INTEGER,
                FOREIGN KEY(board_id) REFERENCES boards(id) ON DELETE CASCADE
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER,
                name TEXT,
                date INTEGER,
                pos INTEGER,
                FOREIGN KEY(list_id) REFERENCES lists(id) ON DELETE CASCADE
            )""")
        self.conn.commit()

    def fetch_boards(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM boards ORDER BY open DESC")
        return [BoardItem(values) for values in cursor.fetchall()]

    def fetch_open_board(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM boards ORDER BY open DESC LIMIT 1")
        data = cursor.fetchone()
        if data is not None:
            board = BoardItem(data)
            board.lists = self.fetch_lists(board.id)
            return board
        return None

    def add_board(self, name):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO boards (name, date, open) VALUES (?, ?, ?)",
            (name, int(datetime.datetime.now().timestamp()), 0))
        self.conn.commit()
        board_id = cursor.lastrowid
        list_names = ["To Do", "Doing", "Done"]
        for list_name in list_names:
            self.add_list(board_id, list_name)

    def delete_board(self, board_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM boards WHERE id = ?", (board_id, ))
        self.conn.commit()

    def update_board_name(self, board_id, board_name):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE boards SET name = ? WHERE id = ?",
                       (board_name, board_id))
        self.conn.commit()

    def open_board(self, board_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(open) FROM boards")
        max_open = cursor.fetchone()[0]
        cursor.execute("UPDATE boards SET open = ? WHERE id = ?",
                       (max_open + 1, board_id))
        self.conn.commit()

    def fetch_lists(self, board_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM lists WHERE board_id = ? ORDER BY pos",
                       (board_id, ))
        lists = []
        for values in cursor.fetchall():
            new_list = ListUI(values, self.fetch_cards(values[0]), self)
            lists.append(new_list)
        return lists

    def add_list(self, board_id, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(pos) FROM lists WHERE board_id = ?",
                       (board_id, ))
        max_pos = cursor.fetchone()[0]
        if not max_pos:
            max_pos = 0
        cursor.execute(
            "INSERT into lists (board_id, name, pos) VALUES (?, ?, ?)",
            (board_id, name, max_pos + 1))
        self.conn.commit()

    def reorder_list(self, list_1, list_2):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE lists set pos = ? WHERE id = ?",
                       (list_1.pos, list_2.id))
        cursor.execute("UPDATE lists set pos = ? WHERE id = ?",
                       (list_2.pos, list_1.id))
        self.conn.commit()

    def delete_list(self, list_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM lists WHERE id = ?", (list_id, ))
        self.conn.commit()

    def fetch_cards(self, list_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE list_id = ? ORDER BY pos",
                       (list_id, ))
        return [CardItem(values) for values in cursor.fetchall()]

    def add_card(self, list_id, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(pos) FROM cards WHERE list_id = ?",
                       (list_id, ))
        max_pos = cursor.fetchone()[0] or 0
        cursor.execute(
            "INSERT INTO cards (list_id, name, date, pos) VALUES (?, ?, ?, ?)",
            (list_id, name, int(
                datetime.datetime.now().timestamp()), max_pos + 1))
        self.conn.commit()

    def edit_card(self, card_id, name):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE cards set name = ? WHERE id = ?",
                       (name, card_id))
        self.conn.commit()

    def move_card(self, card_1, card_2):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE cards SET pos = ? WHERE id = ?",
                       (card_1.pos, card_2.id))
        cursor.execute("UPDATE cards SET pos = ? WHERE id = ?",
                       (card_2.pos, card_1.id))
        self.conn.commit()

    def move_cards_list(self, card_id, list_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MIN(pos) FROM cards WHERE list_id = ?",
                       (list_id, ))
        min_pos = cursor.fetchone()[0]
        if min_pos is None:
            min_pos = 1
        cursor.execute("UPDATE cards SET list_id = ?, pos = ? WHERE id = ?",
                       (list_id, min_pos - 1, card_id))
        self.conn.commit()

    def delete_card(self, card_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id, ))
        self.conn.commit()

    def close(self):
        self.conn.close()

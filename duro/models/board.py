class BoardItem:
    def __init__(self, values, lists=[]):
        self.id = values[0]
        self.name = values[1]
        self.date = values[2]
        self.open = values[3]
        self.lists = lists

class CardItem:
    def __init__(self, values):
        self.id = values[0]
        self.list_id = values[1]
        self.name = values[2]
        self.date = values[3]
        self.pos = values[4]

    def get_card_height(self, w):
        return len(self.name) // w + 1  # card name

    def get_card_details_height(self, w):
        h = self.get_card_height(w)
        h += 1  # card date
        return h

from src.deck_data.card import Card


class Deck(dict):
    deck_list: dict[str, list[Card]]

    def __init__(self, deck_list: dict[str, list[Card]] | None):
        if deck_list is None:
            self.deck_list = {}
        else:
            self.deck_list = deck_list
        super().__init__(self.deck_list)

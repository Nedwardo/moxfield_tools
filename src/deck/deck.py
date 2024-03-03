from src.deck.card import Card


class Deck(dict):
    deck_list: dict[str, list[Card]]

    def __init__(self, deck_list: dict[str, list[Card]] | None):
        if deck_list is None:
            self.deck_list = {}
        else:
            self.deck_list = deck_list
        super().__init__(self.deck_list)
        
    def from_json(json: dict[str, list[dict]]) -> "Deck":
        deck_as_card_dict: dict[str, list[Card]] = {}
        for board in ["maindeck", "commanders"]:
            deck_as_card_dict[board] = []
            for card_as_json in json[board]:
                card = Card.from_json(card_as_json)
                deck_as_card_dict[board].append(card)

        return Deck(deck_as_card_dict)

    @property
    def maindeck(self) -> list[Card]:
        return self.deck_list["maindeck"]

    @property
    def commanders(self) -> list[Card]:
        return self.deck_list["commanders"]

    def contains(
        self, card_name: str, search_main_deck=True, search_commanders=False
    ) -> bool:

        search_space = []
        if search_main_deck:
            search_space += self.maindeck
        if search_commanders:
            search_space += self.commanders

        return any(card_name == card["name"] for card in search_space)

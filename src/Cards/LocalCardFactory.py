import json
from decimal import Decimal

from src.Cards.Card import Card
from src.Cards.CardTypes.CardFactory import build_card
from src.Cards.DeckFactory import DeckFactory


class LocalCardFactory(DeckFactory):
    def __init__(
        self,
        price_filename: str = "prices.json",
        cards_dir: str = "cards",
        deck_list_filename: str = "decklist.json",
    ):
        with open(price_filename) as f:
            self.price_dict = json.load(f)
        self.cards_dir = cards_dir
        with open(deck_list_filename) as f:
            self.deck_list = json.load(f)

    def read_card(self, card_name: str) -> Card:
        with open(f"{self.cards_dir}/{card_name}.json", mode="r") as f:
            card_as_json = json.load(f)
        price = Decimal(0)
        if card_name in self.price_dict.keys():
            price = self.price_dict[card_name]
        return build_card(card_name, card_as_json, price)

    def read_deck_list(self) -> dict[str, list[str]]:
        return self.deck_list

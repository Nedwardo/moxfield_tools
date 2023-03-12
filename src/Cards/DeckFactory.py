from abc import ABC, abstractmethod

from src.Cards.Card import Card


class DeckFactory(ABC):
    def build_decklist(self) -> dict[str, list[Card]]:
        string_deck_list = self.read_deck_list()
        card_deck_list: dict[str, list[Card]] = {"commanders": [], "mainboard": []}
        for board in card_deck_list.keys():
            for card_name in string_deck_list[board]:
                card_deck_list[board].append(self.read_card(card_name))

        return card_deck_list

    @abstractmethod
    def read_deck_list(self) -> dict[str, list[str]]:
        pass

    @abstractmethod
    def read_card(self, card_name: str) -> Card:
        pass

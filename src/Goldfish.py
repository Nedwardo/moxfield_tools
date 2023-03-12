from __future__ import annotations

from src.DeckList import DeckList, get_rog_si_deck_list
from src.Hand import CardList
from src.ShuffledLibrary import ShuffledLibrary


class Goldfish:
    def __init__(self):
        self.deck = get_rog_si_deck_list()
        self.library = ShuffledLibrary(self.deck)
        self.hand = CardList(self.library)

    def game_state(self) -> tuple[ShuffledLibrary, CardList]:
        return self.library, self.hand

    def get_hand(self) -> CardList:
        return self.hand

    def get_library(self) -> ShuffledLibrary:
        return self.library

    def get_deck(self) -> DeckList:
        return self.deck

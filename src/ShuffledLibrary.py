import random

from src.Cards.Card import Card
from src.Cards.CardList import CardList
from src.DeckList import DeckList


class ShuffledLibrary(CardList):
    def __init__(self, decklist: DeckList) -> None:
        super().__init__()
        self.decklist: DeckList = decklist
        self.shuffle()

    def shuffle(self):
        self.cards = self.decklist.mainboard.copy().to_list()
        random.shuffle(self.cards)

    def draw_starting_hand(self) -> CardList:
        self.shuffle()
        starting_hand: CardList = CardList(self.cards[:7])
        self.cards = self.cards[7:]
        return starting_hand

    def draw(self) -> Card:
        card: Card = self.cards[0]
        self.cards = self.cards[1:]
        return card

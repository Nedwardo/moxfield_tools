from src.Cards.Card import Card
from src.Cards.CardList import CardList
from src.ShuffledLibrary import ShuffledLibrary


class Hand(CardList):
    def __init__(
        self,
        cards: list[Card] = [],
        library: ShuffledLibrary | None = None,
        init: bool = True,
    ) -> None:
        super().__init__(cards)
        self.library: ShuffledLibrary | None = library

        if not cards and library and init:
            self.mulligan()

    def set_library(self, library: ShuffledLibrary) -> None:
        self.library = library

    def unset_library(self) -> None:
        self.library = None

    def mulligan(self, library: ShuffledLibrary | None = None) -> None:
        if library is not None:
            self.cards = library.draw_starting_hand().to_list()
        elif self.library is not None:
            self.cards = self.library.draw_starting_hand().to_list()
        else:
            raise NoLibraryException("No library configured")

    def draw(self, library: ShuffledLibrary | None = None) -> None:
        if library is not None:
            self.cards.append(library.draw())
        elif self.library is not None:
            self.cards.append(self.library.draw())
        else:
            raise NoLibraryException("No library configured")


# TODO add tests
class NoLibraryException(RuntimeError):
    pass

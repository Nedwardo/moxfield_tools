if False:  # pragma: no cover (mypy) # NOSONAR
    from typing import TYPE_CHECKING  # type: ignore
else:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import SupportsIndex, overload
else:
    from typing_extensions import overload, SupportsIndex

from typing import Any, Callable, Iterator

from src.Cards.Card import Card


class CardList(list):
    def __init__(self, card_list: "CardList | list[Card] | None" = None):
        if card_list is None:
            self.cards: list[Card] = []
        elif isinstance(card_list, CardList):
            self.cards = card_list.cards.copy()
        else:
            self.cards = card_list
        super().__init__([])

    def land_count(self) -> int:
        return sum(int(card.is_land()) for card in self.cards)

    def has_payoff(self, can_tutor: bool = False) -> bool:
        return self.has_tag("Win condition", can_tutor)

    def has_one_card_win_con(self, can_tutor: bool = False) -> bool:
        return self.has_tag("one card win con", can_tutor)

    def has_card_advantage(self, can_tutor: bool = False) -> bool:
        return self.has_tag("Ridiculous card advantage engines", can_tutor)

    def has_tag(self, tag: str, can_tutor: bool = False) -> bool:
        return self.raw_has_tag(tag) or (can_tutor and self.has_tutor())

    def has_tutor(self) -> bool:
        return self.raw_has_tag("Tutor")

    def all_tagged(self, tag: str) -> "CardList":
        return self.filter(lambda card: card.has_tag(tag))

    def count_tag(self, tag: str) -> int:
        return len(self.all_tagged(tag))

    def raw_has_tag(self, tag: str) -> bool:
        return self.count_tag(tag) != 0

    def filter(self, filter_method: Callable[[Card], bool]) -> "CardList":
        return CardList(list(filter(filter_method, self.cards)))

    def non_lands(self) -> "CardList":
        return self.filter(lambda card: not card.is_land())

    def mana_sources(self) -> "CardList":
        return self.filter(lambda card: not card.is_mana_source)

    def rocks(self) -> "CardList":
        return self.filter(lambda card: card.is_rock())

    def rituals(self) -> "CardList":
        return self.filter(lambda card: card.is_ritual())

    def lands(self) -> "CardList":
        return self.filter(lambda card: card.is_land())

    @overload
    def __getitem__(self, index: SupportsIndex) -> Card:
        ...

    @overload
    def __getitem__(self, index: str) -> Card:
        ...

    @overload
    def __getitem__(self, index: slice) -> "CardList":
        ...

    def __getitem__(self, index: SupportsIndex | str | slice) -> "Card | CardList":
        if isinstance(index, str):
            return [card for card in self.cards if card.name == index][0]
        elif isinstance(index, SupportsIndex):
            return self.cards[index]
        else:
            return CardList(self.cards[index])

    def copy(self) -> "CardList":
        return CardList(self.cards.copy())

    def __str__(self) -> str:
        return str([str(card) for card in self.cards])

    def __repr__(self) -> str:
        return str(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def to_list(self) -> list[Card]:
        return self.cards

    def __add__(self, other: "CardList | list[Any]") -> "CardList":
        if isinstance(other, list):
            return CardList(self.cards + other)
        elif isinstance(other, CardList):
            return CardList(self.cards + other.cards)
        raise TypeError(f"Cannot concat {type(other)} to CardList")

    def __iter__(self) -> Iterator[Card]:
        return self.cards.__iter__()

    def __radd__(self, other: "int | CardList") -> "CardList":
        if isinstance(other, int):
            return self
        return self.__add__(other)

from abc import ABC, abstractmethod

from src.cacher import Cacher
from src.deck_data.deck import Deck


class DeckSource(ABC):
    cacher: Cacher

    def __init__(self):
        self.cacher = Cacher()

    @abstractmethod
    def is_valid_target(self, uri: str) -> bool: ...

    def get_deck(self, uri: str) -> Deck | None:
        if self.cacher.is_deck_cached(self.get_id(uri)):
            deck = self.cacher.get_cached_deck(uri)
            if deck is not None:
                return deck
        deck = self._get(uri)
        if deck is None:
            return None
        self._cache_deck(self.get_id(uri), deck)
        return deck

    def _cache_deck(self, uri: str, deck: Deck):
        self.cacher.cache_deck(uri, deck)

    @abstractmethod
    def _get(self, uri: str) -> Deck | None: ...

    @abstractmethod
    def get_id(self, uri: str) -> str: ...

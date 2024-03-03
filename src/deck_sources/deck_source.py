from abc import ABC, abstractmethod
from typing import Any
from logging import Logger, getLogger
from src.cacher import Cacher
from src.deck.deck import Deck


class DeckSource(ABC):
    cacher: Cacher
    name: str
    logger: Logger

    def __init__(self):
        self.logger = getLogger(f"{self.name} deck source")
        self.cacher = Cacher()

    @abstractmethod
    def is_valid_target(self, uri: str) -> bool: ...

    def get_deck(self, uri: str) -> Deck | None:
        if self.cacher.is_deck_cached(self.get_id(uri)):
            self.logger.info(f"{uri} is cached, obtaining cached file")
            deck = self.cacher.get_cached_deck(uri)
            if deck is not None:
                return deck
            self.logger.info(f"{uri} is cached, and corrupted, deleting cached file")
            self.cacher.delete_cache_entry(uri)

        self.logger.info(f"{uri} is not cached, making request")
        response = self._get(uri)
        if response is None:
            return None

        deck = self._build_deck(response)
        if deck is None:
            return None
        self._cache_deck(self.get_id(uri), deck)
        return deck

    def _cache_deck(self, uri: str, deck: Deck):
        self.cacher.cache_deck(uri, deck)

    @abstractmethod
    def _get(self, uri: str) -> Any | None: ...

    @abstractmethod
    def _build_deck(self, data: Any) -> Deck | None: ...

    @abstractmethod
    def get_id(self, uri: str) -> str: ...

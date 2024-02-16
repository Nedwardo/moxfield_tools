from src.deck_data.deck import Deck
from src.deck_sources.deck_source import DeckSource
from src.deck_sources.moxfield_source import MoxfieldSource


class DeckSourceFactory:
    deck_sources: list[DeckSource]

    def __init__(self):
        self.deck_sources = [MoxfieldSource()]

    def get_deck(self, uri: str) -> Deck | None:
        for deck_source in self.deck_sources:
            if deck_source.is_valid_target(uri):
                return deck_source.get_deck(uri)
        return None

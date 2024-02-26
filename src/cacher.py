from glob import glob
import json
import os
from pathvalidate import sanitize_filename

from src.deck.deck import Deck


class Cacher:
    base_dir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cache_dir: str = "_cache"

    def clean_key_name(self, key: str) -> str:
        return sanitize_filename(key)

    def get_filename(self, key: str) -> str:
        return f"{self.base_dir}/{self.cache_dir}/{self.clean_key_name(key)}.json"

    def cache_deck(self, key: str, value: Deck) -> None:
        with open(
            self.get_filename(key),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(value, f)

    def is_deck_cached(self, key: str) -> bool:
        return len(glob(self.get_filename(key))) > 0

    def get_cached_deck(self, key: str) -> None | Deck:
        if not self.is_deck_cached(key):
            return None

        with open(
            self.get_filename(key),
            encoding="utf-8",
        ) as f:
            return Deck(json.load(f))

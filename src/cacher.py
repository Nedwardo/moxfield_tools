from glob import glob
import json
import os

from src.deck_data.deck import Deck


class Cacher:
    base_dir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cache_dir: str = "_cache"

    def cache_deck(self, key: str, value: Deck) -> None:
        with open(
            f"{self.base_dir}/{self.cache_dir}/{key}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(value, f)

    def is_deck_cached(self, key: str) -> bool:
        return len(glob(f"{self.base_dir}/{self.cache_dir}/{key}.json")) > 0

    def get_cached_deck(self, key: str) -> None | Deck:
        if not self.is_deck_cached(key):
            return None

        with open(
            f"{self.base_dir}/{self.cache_dir}/{key}.json", encoding="utf-8"
        ) as f:
            return Deck(json.load(f))

from glob import glob
from pathlib import Path
import json
import os
from typing import Any
from pathvalidate import sanitize_filename
from src.deck.card import Card

from src.deck.deck import Deck


class Cacher:
    base_dir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cache_dir: str = "_cache"
    
    def __init__(self) -> None:
        Path(self._get_cache_dir()).mkdir(parents=True, exist_ok=True)

    def clean_key_name(self, key: str) -> str:
        return sanitize_filename(key)
    
    def _get_cache_dir(self) -> str:
        return f"{self.base_dir}/{self.cache_dir}"

    def get_filename(self, key: str) -> str:
        return f"{self._get_cache_dir()}/{self.clean_key_name(key)}.json"

    def cache_deck(self, key: str, value: Deck) -> None:
        with open(
            self.get_filename(key),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(value, f, indent=4)

    def is_deck_cached(self, key: str) -> bool:
        return len(glob(self.get_filename(key))) > 0

    def get_cached_deck(self, key: str) -> None | Deck:
        if not self.is_deck_cached(key):
            return None

        with open(
            self.get_filename(key),
            encoding="utf-8",
        ) as f:
            return Deck.from_json(json.load(f))
    
    def delete_cache_entry(self, key: str) -> None:
        if not self.is_deck_cached(key):
            return None

        os.remove(self.get_filename(key))

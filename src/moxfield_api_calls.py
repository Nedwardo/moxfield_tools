import json
from typing import Any, Union

import requests


class Session:
    instance: Union["Session", None] = None

    def __new__(cls, *args, **kwargs) -> "Session":
        if cls.instance:
            return cls.instance
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        self.request_session = requests.Session()

    def get(self, url) -> requests.Response:
        return self.request_session.get(url)


def fetch_deck_list(url: str) -> dict[str, Any]:
    with open("cached_api.json", "w") as f:
        json.dump(Session().get(url).json(), f, indent=4)
    return Session().get(url).json()


def rog_si_deck_url() -> str:
    return "https://api2.moxfield.com/v2/decks/all/XoUTuCXSgkascuFLZcckUA"


def cache_rog_si() -> None:
    cache_deck(rog_si_deck_url(), "cached_api.json")


def cache_deck(url: str, filename: str) -> None:
    deck_as_json = fetch_deck_list(url)
    with open(filename) as f:
        json.dump(deck_as_json, f)

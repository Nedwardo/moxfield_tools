from json import JSONDecodeError
import re
from src.deck_data.deck import Deck
from src.session import Session

from src.deck_sources.deck_source import DeckSource


class MoxfieldSource(DeckSource):
    api_base_url: str
    moxfield_base_url: str
    moxfield_regex: str
    session: Session
    headers: dict

    def __init__(self):
        super().__init__()
        self.api_base_url = "https://api2.moxfield.com/v3/decks/all/"
        self.moxfield_base_url = "https://www.moxfield.com/decks/"
        self.moxfield_regex = rf"{self.moxfield_base_url}([1-9A-z]*)"
        self.session = Session()
        self.headers = {
            "authority": "api2.moxfield.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer undefined",
            "cache-control": "no-cache",
            "dnt": "1",
            "origin": "https://www.moxfield.com",
            "pragma": "no-cache",
            "referer": "https://www.moxfield.com/",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "x-moxfield-version": "2024.02.14.1",
        }

    def is_valid_target(self, uri: str):
        return re.match(self.moxfield_regex, uri) is not None

    def _convert_to_api_url(self, uri: str):
        api_url = uri.replace(self.moxfield_base_url, self.api_base_url)
        return api_url

    def _get(self, uri: str) -> Deck | None:
        url = self._convert_to_api_url(uri)
        response = self.session.get(url, headers=self.headers)
        try:
            return Deck(response.json())
        except JSONDecodeError:
            return None

    def get_id(self, uri: str) -> str:
        return f"moxfield-{uri.replace(self.moxfield_base_url, '')}"

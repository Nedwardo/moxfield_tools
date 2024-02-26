from json import JSONDecodeError
import re
from typing import Any
from src.deck.card import Card
from src.deck.deck import Deck
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
            "sec-ch-ua": '"Not A(Brand";v="99", "Google " + \
            "Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "x-moxfield-version": "2024.02.14.1",
        }

    def is_valid_target(self, uri: str):
        return re.match(self.moxfield_regex, uri) is not None

    def _convert_to_api_url(self, uri: str):
        api_url = uri.replace(self.moxfield_base_url, self.api_base_url)
        return api_url

    def _get(self, uri: str) -> Any | None:
        url = self._convert_to_api_url(uri)
        response = self.session.get(url, headers=self.headers)
        try:
            return response.json()
        except JSONDecodeError:
            return None

    def get_id(self, uri: str) -> str:
        return f"moxfield-{uri.replace(self.moxfield_base_url, '')}"

    def _build_deck(self, data: Any) -> Deck | None:
        if "boards" not in data.keys():
            return None
        json: dict = data
        deck_as_card_dict: dict[str, list[Card]] = {"mainboard": [], "commanders": []}
        for board in ["mainboard", "commanders"]:
            for card_name in json["boards"][board]["cards"]:
                card_as_json = json["boards"][board]["cards"][card_name]["card"]
                card = self._build_card(card_name, card_as_json)
                if card is not None:
                    deck_as_card_dict[board].append(card)

        deck_as_card_dict["maindeck"] = deck_as_card_dict["mainboard"]
        del deck_as_card_dict["mainboard"]
        if (
            len(deck_as_card_dict["maindeck"]) + len(deck_as_card_dict["commanders"])
            == 100
        ):
            return Deck(deck_as_card_dict)
        return None

    def _build_card(self, card_name: str, card_as_json: dict) -> Card | None:
        card_info = self.get_card_info_from_card_as_json(card_as_json)
        return Card(card_name, card_info)

    def get_generic_card_info_from_card_json(
        self, card_as_json: dict
    ) -> dict[str, str]:
        if (
            "oracle_text" not in card_as_json.keys()
            and "card_faces" in card_as_json.keys()
        ):
            card_as_json["oracle_text"] = card_as_json["card_faces"]

        if "mana_cost" not in card_as_json.keys():
            card_as_json["mana_cost"] = 0

        return {
            "name": card_as_json["name"],
            "cmc": card_as_json["cmc"],
            "type_line": str(card_as_json.get("type_line")),
            "oracle_text": str(card_as_json.get("oracle_text")),
            "mana_cost": card_as_json["mana_cost"],
        }

    def get_creature_stats_from_card_as_json(
        self, card_as_json: dict
    ) -> dict[str, str] | None:
        try:
            card_info = {}
            card_info["power"] = card_as_json["power"]
            card_info["toughness"] = card_as_json["toughness"]
            return card_info
        except KeyError:
            return None

    def get_alternate_cmc_from_card_as_json(
        self, card_as_json: dict
    ) -> dict[str, str] | None:
        try:
            card_info = {}
            card_info["cmc"] = card_as_json["cmcOverride"]
            card_info["mana_cost"] = card_as_json["manaCostOverride"]
            return card_info
        except KeyError:
            return None

    def get_card_info_from_card_as_json(self, card_as_json: dict) -> dict[str, Any]:
        try:
            card_info_dict: dict[str, Any] = self.get_generic_card_info_from_card_json(
                card_as_json
            )
        except KeyError:
            print(card_as_json)

        creature_stats_dict = self.get_creature_stats_from_card_as_json(card_as_json)
        if creature_stats_dict:
            card_info_dict = {**card_info_dict, **creature_stats_dict}

        alternate_casting_cost_dict = self.get_alternate_cmc_from_card_as_json(
            card_as_json
        )
        if alternate_casting_cost_dict:
            card_info_dict["Alternative cost"] = alternate_casting_cost_dict
        return card_info_dict

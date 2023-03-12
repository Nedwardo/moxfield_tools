import json
from decimal import Decimal
from typing import Any

from src.Cards.Card import Card
from src.Cards.CardTypes.CardFactory import build_card
from src.Cards.DeckFactory import DeckFactory


class ApiCardFactory(DeckFactory):
    def __init__(
        self,
        api_response: dict[str, Any],
        custom_tags_file: str = "tags/custom_tags.json",
    ):
        super().__init__()
        self.api_response = api_response
        with open(custom_tags_file) as f:
            self.custom_tags = json.load(f)

    def read_moxfield_tags(self) -> dict[str, list[str]]:
        return self.api_response["authorTags"]

    def read_custom_tags(self) -> dict[str, list[str]]:
        return self.custom_tags

    def is_commander(self, card_name: str) -> bool:
        return card_name in self.api_response["commanders"].keys()

    def get_card_info_messy_dict(self, card_name: str) -> dict[str, Any]:
        if self.is_commander(card_name):
            return self.api_response["commanders"][card_name]
        else:
            return self.api_response["mainboard"][card_name]

    def read_price(self, card_name: str) -> Decimal:
        try:
            float_price = self.get_card_info_messy_dict(card_name)["prices"]["eur"]
            return round(Decimal.from_float(float_price), 2)
        except KeyError:
            return Decimal(0)

    def read_generic_card_properties(self, card_name: str) -> dict[str, str]:
        messy_card_info_dict = self.get_card_info_messy_dict(card_name)
        return {
            "name": card_name,
            "cmc": messy_card_info_dict["cmc"],
            "type_line": messy_card_info_dict["type_line"],
            "oracle_text": messy_card_info_dict["oracle_text"],
            "mana_cost": messy_card_info_dict["mana_cost"],
        }

    def read_creature_stats(self, card_name: str) -> dict[str, str] | None:
        messy_card_info_dict = self.get_card_info_messy_dict(card_name)
        try:
            card_info = {}
            card_info["power"] = messy_card_info_dict["power"]
            card_info["toughness"] = messy_card_info_dict["toughness"]
            return card_info
        except KeyError:
            return None

    def read_alternate_casting_cost(self, card_name: str) -> dict[str, str] | None:
        messy_card_info_dict = self.get_card_info_messy_dict(card_name)
        try:
            card_info = {}
            card_info["cmc"] = messy_card_info_dict["cmcOverride"]
            card_info["mana_cost"] = messy_card_info_dict["manaCostOverride"]
            return card_info
        except KeyError:
            return None

    def read_card_info(self, card_name: str) -> dict[str, Any]:
        card_info_dict: dict[str, Any] = self.read_generic_card_properties(card_name)

        creature_stats_dict = self.read_creature_stats(card_name)
        if creature_stats_dict:
            card_info_dict = {**card_info_dict, **creature_stats_dict}

        alternate_casting_cost_dict = self.read_alternate_casting_cost(card_name)
        if alternate_casting_cost_dict:
            card_info_dict["Alternative cost"] = alternate_casting_cost_dict

        card_info_dict["moxfield_tags"] = self.read_moxfield_tags()[card_name]
        card_info_dict["custom_tags"] = self.read_custom_tags()[card_name]
        return card_info_dict

    def read_card(self, card_name: str) -> Card:
        card_info = self.read_card_info(card_name)
        price = self.read_price(card_name)
        return build_card(card_name, card_info, price)

    def read_deck_list(self) -> dict[str, list[str]]:
        commanders = self.api_response["commanders"].keys()
        mainboard = self.api_response["mainboard"].keys()
        return {"commanders": commanders, "mainboard": mainboard}

import re
from decimal import Decimal
from typing import Any

from src.Cards.Card import Card
from src.Cards.CardTypes.Land import Land
from src.Cards.CardTypes.ManaRock import ManaRock
from src.Cards.CardTypes.ManaSource import ManaSource
from src.Cards.CardTypes.Ritual import Ritual


def build_card(name: str, card_info: dict[str, Any], price: Decimal) -> Card:
    for tag_source in ("moxfield_tags", "custom_tags"):
        if tag_source in card_info.keys():
            for tag in card_info[tag_source]:
                if len(re.findall(r"\+(\d) mana", tag)) > 0:
                    return build_mana_source(name, card_info, price)
    return Card(name, card_info, price)


def build_mana_source(
    name: str, card_info: dict[str, Any], price: Decimal
) -> ManaSource:
    if "land" in card_info["type_line"].lower():
        return Land(name, card_info, price)
    elif "artifact" in card_info["type_line"].lower():
        return ManaRock(name, card_info, price)
    return Ritual(name, card_info, price)

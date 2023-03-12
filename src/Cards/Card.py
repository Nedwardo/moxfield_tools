from decimal import Decimal
from typing import Any


class Card:
    def __init__(
        self,
        name: str,
        card_info: dict[str, Any],
        price: Decimal,
    ):
        self.name = name
        self.card_info = card_info
        self.price = price

    def cmc(self, allow_alternate=True) -> int:
        alternate_cost_key = "Alternative cost"
        if allow_alternate and alternate_cost_key in self.card_info.keys():
            alternate_mana_cost = self.card_info[alternate_cost_key]["cmc"]
            return min(self.card_info["cmc"], alternate_mana_cost)
        return self.card_info["cmc"]

    def set_moxfield_tags(self, moxfield_tags: list[str]) -> None:
        self.card_info["moxfield_tags"] = moxfield_tags

    def set_custom_tags(self, custom_tags: list[str]) -> None:
        self.card_info["custom_tags"] = custom_tags

    def add_moxfield_tags(self, moxfield_tags: list[str]) -> None:
        if "moxfield_tags" not in self.card_info.keys():
            self.card_info["moxfield_tags"] = []

        self.card_info["moxfield_tags"] += moxfield_tags

    def add_custom_tags(self, custom_tags: list[str]) -> None:
        if "custom_tags" not in self.card_info.keys():
            self.card_info["custom_tags"] = []

        self.card_info["custom_tags"] += custom_tags

    def tags(self) -> list[str]:
        if (
            "moxfield_tags" in self.card_info.keys()
            and "custom_tags" in self.card_info.keys()
        ):
            return self.card_info["moxfield_tags"] + self.card_info["custom_tags"]
        if "moxfield_tags" in self.card_info.keys():
            return self.card_info["moxfield_tags"]
        if "custom_tags" in self.card_info.keys():
            return self.card_info["custom_tags"]
        return []

    def contains_text(self, sub_string: str) -> bool:
        return sub_string in self.card_info["oracle_text"]

    def has_tag(self, tag: str, tag_group: str = "") -> bool:
        if tag_group:
            if tag_group == "moxfield":
                return tag in self.card_info["moxfield_tags"]
            if tag_group == "custom":
                return tag in self.card_info["custom_tags"]
        return tag in self.tags()

    def is_land(self) -> bool:
        return False

    def mana_generated_per_turn(self) -> int:
        return 0

    def ritual_mana_generation(self) -> int:
        return 0

    def is_mana_source(self) -> bool:
        return False

    def is_ritual(self) -> bool:
        return False

    def is_rock(self) -> bool:
        return False

    def get_moxfield_tags(self) -> list[str]:
        if "moxfield_tags" in self.card_info.keys():
            return self.card_info["moxfield_tags"]
        return []

    def get_custom_tags(self) -> list[str]:
        if "custom_tags" in self.card_info.keys():
            return self.card_info["custom_tags"]
        return []

    def is_permanent(self) -> bool:
        return not (
            "Instant" in self.card_info["type_line"]
            or "Sorcery" in self.card_info["type_line"]
        )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self.card_info)

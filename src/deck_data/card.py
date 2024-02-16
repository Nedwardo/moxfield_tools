import re
from typing import Any


class Card(dict):
    def __init__(
        self,
        name: str,
        card_info: dict[str, Any],
    ):
        self.name = name
        self.card_info = card_info
        super().__init__(self.card_info)

    def cmc(self, allow_alternate=True) -> int:
        alternate_cost_key = "Alternative cost"
        if allow_alternate and alternate_cost_key in self.card_info.keys():
            alternate_mana_cost = self.card_info[alternate_cost_key]["cmc"]
            return min(self.card_info["cmc"], alternate_mana_cost)
        return self.card_info["cmc"]

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

    def contains_oracle_text(self, sub_string: str, regex: bool = False) -> bool:
        return is_sub_string_in_base_string(
            self.card_info["oracle_text"], sub_string, regex
        )

    def has_tag(self, tag: str, tag_group: str = "") -> bool:
        if tag_group:
            if tag_group == "moxfield":
                return tag in self.get_moxfield_tags()
            if tag_group == "custom":
                return tag in self.get_custom_tags()
        return tag in self.tags()

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

    @property
    def __dict__(self):
        return self.card_info


def is_sub_string_in_base_string(
    base_string: str, sub_string: str, regex: bool = False
) -> bool:
    if not regex:
        return sub_string in base_string
    else:
        return re.match(sub_string, base_string) is not None

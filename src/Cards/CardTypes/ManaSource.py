import re
from decimal import Decimal
from typing import Any

from src.Cards.Card import Card


class ManaSource(Card):
    def __init__(self, name: str, card_info: dict[str, Any], price: Decimal):
        super().__init__(name, card_info, price)
        for tag in self.tags():
            mana_generated_regex = re.match(r"\+(\d) mana", tag)
            if mana_generated_regex is not None:
                self.mana_generated = int(mana_generated_regex.group(1))

    def is_mana_source(self) -> bool:
        return True

    def ritual_mana_generation(self) -> int:
        return self.mana_generated - self.cmc()

    def mana_generated_per_turn(self) -> int:
        return self.mana_generated

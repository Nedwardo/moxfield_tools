from decimal import Decimal
from typing import Any

from src.Cards.CardTypes.ManaSource import ManaSource


class Ritual(ManaSource):
    def __init__(self, name: str, card_info: dict[str, Any], price: Decimal):
        super().__init__(name, card_info, price)

    def is_ritual(self) -> bool:
        return True

    def mana_generated_per_turn(self) -> int:
        return self.mana_generated - self.cmc()

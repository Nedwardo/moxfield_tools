from decimal import Decimal
from typing import Any

from src.Cards.CardTypes.ManaSource import ManaSource


class ManaRock(ManaSource):
    def __init__(self, name: str, card_info: dict[str, Any], price: Decimal):
        super().__init__(name, card_info, price)

    def is_rock(self) -> bool:
        return True

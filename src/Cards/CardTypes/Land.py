from decimal import Decimal
from typing import Any

from src.Cards.CardTypes.ManaSource import ManaSource


class Land(ManaSource):
    def __init__(self, name: str, card_info: dict[str, Any], price: Decimal):
        super().__init__(name, card_info, price)

    def cmc(self, allow_alternate=True) -> int:
        del allow_alternate
        return 0

    def is_land(self) -> bool:
        return True

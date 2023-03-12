from typing import List

from src.Cards.CardList import CardList
from src.Cards.CardTypes.Land import Land
from src.Cards.CardTypes.ManaRock import ManaRock
from src.Cards.CardTypes.ManaSource import ManaSource
from src.Cards.CardTypes.Ritual import Ritual
from src.ManaSources import ManaSources


class Board:
    lands: dict[Land, bool]
    rocks: dict[ManaRock, bool]

    def __init__(self):
        self.lands = {}
        self.rocks = {}
        self.has_made_land_drop = False

    def get_total_mana(self):
        return self.get_total_land_mana() + self.get_total_rock_mana()

    def get_total_land_mana(self) -> int:
        return get_total_mana_production(self.spendable_lands())

    def get_total_rock_mana(self) -> int:
        return get_total_mana_production(self.spendable_rocks())

    def spendable_lands(self) -> List[Land]:
        return [land for land in self.lands.keys() if self.lands[land]]

    def spendable_rocks(self) -> List[ManaRock]:
        return [rock for rock in self.rocks.keys() if self.rocks[rock]]

    def play_land(self, land: Land):
        if not self.has_made_land_drop:
            self.lands[land] = False
            self.has_made_land_drop = True
        else:
            raise InvalidOperationException("Already made land drop")

    def play_rock(self, rock: ManaRock, rituals: ManaSources):
        self.spend_mana(rock.cmc(), rituals)
        self.rocks[rock] = False

    def spend_mana(self, cmc: int, rituals: ManaSources) -> ManaSources:
        if self.get_total_mana() + get_total_mana_production(rituals) < cmc:
            raise InvalidOperationException("Not enough mana")

        rituals.sort(key=Ritual.ritual_mana_generation)

        return rituals  # TODO finish this

    def get_sorted_mana_production(self) -> List[ManaSource]:
        mana_sources: List[ManaSource] = list(
            list(self.spendable_lands()) + list(self.spendable_rocks())
        )
        mana_sources.sort(key=ManaSource.mana_generated_per_turn)
        return mana_sources


def get_total_mana_production(
    mana_sources: List[ManaSource] | List[Ritual] | List[ManaRock] | List[Land],
) -> int:
    return ManaSources(CardList(list(mana_sources))).get_max_mana()


class InvalidOperationException(Exception):
    pass

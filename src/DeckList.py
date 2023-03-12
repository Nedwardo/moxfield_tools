import json
import os
from decimal import Decimal
from typing import Union

from src.Cards.CardList import CardList
from src.Cards.DeckFactory import DeckFactory
from src.Cards.DeckFactoryFactory import get_card_factory


class DeckList:
    def __init__(self, card_factory: DeckFactory):
        decklist = card_factory.build_decklist()
        self.commanders = CardList(decklist["commanders"])
        self.mainboard = CardList(decklist["mainboard"])
        if len(self.commanders) > 2:
            raise ValueError("Commanders and main deck wrong way around")

        self.moxfield_tags: dict[str, list[str]] = {}
        self.custom_tags: dict[str, list[str]] = {}
        self.load_tags_from_cards()
        self.generate_deck_dictionary()

    def tag_cards(self) -> None:
        for card in self.get_deck_list():
            if card.name in self.moxfield_tags.keys():
                card.set_moxfield_tags(self.moxfield_tags[card.name])

            if card.name in self.custom_tags.keys():
                card.set_custom_tags(self.custom_tags[card.name])

    def write_card_info(
        self,
        deck_list_filename: str = "deck/decklist.json",
        card_info_dir: str = "cards",
        price_filename: str = "deck/prices.json",
        tags_dir: str = "tags",
    ) -> None:
        if deck_list_filename:
            with open(deck_list_filename, "w") as f:
                json.dump(self.get_decklist_as_json(), f, indent=4)

        if price_filename:
            with open(price_filename, "w") as f:
                json.dump(self.get_prices_dict(), f, indent=4)

        if card_info_dir:
            if not os.path.exists(card_info_dir):
                os.makedirs(card_info_dir)

            for card in self.get_deck_list():
                with open(f"{card_info_dir}/{str(card)}.json", "w") as f:
                    json.dump(card.card_info, f, indent=4)

        if tags_dir:
            if not os.path.exists(tags_dir):
                os.makedirs(tags_dir)
            with open(f"{tags_dir}/moxfield_tags.json", "w") as f:
                json.dump(self.moxfield_tags, f, indent=4)

            with open(f"{tags_dir}/custom_tags.json", "w") as f:
                json.dump(self.custom_tags, f, indent=4)

    def get_deck_list(self) -> CardList:
        return self.mainboard + self.commanders

    def get_decklist_as_json(self) -> dict[str, list[str]]:
        deck_list: dict[str, list[str]] = {}
        deck_list["commanders"] = [str(commander) for commander in self.commanders]
        deck_list["mainboard"] = [str(card) for card in self.mainboard]
        return deck_list

    def get_prices_dict(self) -> dict[str, float]:
        prices_dict: dict[str, float] = {
            str(card): float(card.price) for card in self.get_deck_list()
        }
        prices_dict["total"] = float(self.get_total_price())
        return prices_dict

    def get_total_price(self) -> Decimal:
        return Decimal(sum(card.price for card in self.get_deck_list()))

    def generate_deck_dictionary(self) -> None:
        self.dictionary = {card.name: card for card in self.get_deck_list()}

    def add_new_tag(self, tag_name: str, cards_affected: Union[str, list[str]]) -> None:
        if isinstance(cards_affected, str):
            cards_affected = [cards_affected]
        for card_name in cards_affected:
            if card_name not in self.custom_tags.keys():
                self.custom_tags[card_name] = []
            self.custom_tags[card_name].append(tag_name)
        self.tag_cards()

    def load_tags_from_cards(self) -> None:
        for card in self.get_deck_list():
            self.moxfield_tags[card.name] = card.get_moxfield_tags()
            self.custom_tags[card.name] = card.get_custom_tags()

    def read_tags_from_local_dir(
        self,
        tags_dir: str = "tags",
    ) -> None:
        with open(f"{tags_dir}/custom_tags.json", "r") as f:
            self.custom_tags = json.load(f)

        self.tag_cards()

    def average_mana_total(self) -> float:
        return sum(card.mana_generated_per_turn() for card in self.mainboard) / len(
            self.mainboard
        )

    def __str__(self) -> str:
        return str(self.get_deck_list())


def get_rog_si_deck_list(source: str = "local") -> DeckList:
    return DeckList(get_card_factory(source))

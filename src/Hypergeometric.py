import random
from typing import Callable

from src.Cards.CardList import CardList
from src.DeckList import DeckList
from src.Goldfish import Goldfish
from src.Hand import Hand
from src.ManaSources import ManaSources
from src.ShuffledLibrary import ShuffledLibrary


def hypergeometric_simulation(collection: list, samples: int) -> list:
    output = []
    sampled_collection = collection.copy()
    for _ in range(samples):
        sample_index = random.randrange(0, len(sampled_collection))
        output.append(sampled_collection.pop(sample_index))
    return output


def is_keepable_cards(cards: CardList) -> bool:
    mana_sources = ManaSources(cards)
    hand = Hand(cards)
    return (
        (hand.has_one_card_win_con(True) or hand.has_tag("Wheel"))
        and len(mana_sources.lands()) < 3
        and mana_sources.get_max_mana() > 4
    )


def get_hand_odds(
    hand_statement: Callable[[CardList], bool] = is_keepable_cards,
    library: ShuffledLibrary = Goldfish().get_library(),
    sample_size: int = 1000,
) -> list[CardList]:
    successes = []
    for _ in range(sample_size):
        hand = library.draw_starting_hand()
        if hand_statement(CardList(hand)):
            successes.append(hand)
    return successes


def average_mana_total_with_max_lands(decklist: DeckList, hand_size=7, turn=0) -> float:
    deck_size = len(decklist.mainboard)
    mana_sources = ManaSources(decklist.mainboard)
    non_land_count = len(decklist.mainboard.non_lands())
    land_count = len(decklist.mainboard.lands())

    lands_mana_value = mana_sources.land_mana(turn) / land_count
    non_lands_mana_value = mana_sources.non_land_mana(turn) / non_land_count

    non_land_deck_ratio = non_land_count / deck_size
    expected_non_lands = non_land_deck_ratio * hand_size
    expected_lands = hand_size - expected_non_lands
    return expected_non_lands * non_lands_mana_value + lands_mana_value * expected_lands


# Maybe functions and specific / min values from those functions
# TODO then run hyper geometric simulation to calculate rough odds,
# much much later run calculator to work out exact odds

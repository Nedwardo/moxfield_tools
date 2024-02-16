from src.deck_sources.deck_source_factory import DeckSourceFactory
from src.tournament_result_sources.edh_top_16_source import EdhTop16Source
import pandas as pd


class EdhTop16Transform:
    tournament_source: EdhTop16Source
    deck_list_source_factory: DeckSourceFactory

    def __init__(self):
        self.tournament_source = EdhTop16Source()
        self.deck_list_source_factory = DeckSourceFactory()

    def get_all_deck_info(self) -> pd.DataFrame:
        top_16_deck_urls = self.tournament_source.get_all_decks()
        top_16_deck_urls = top_16_deck_urls[["winRate", "wins", "standing", "decklist"]]
        top_16_deck_urls["deck"] = top_16_deck_urls["decklist"].apply(
            self.deck_list_source_factory.get_deck
        )
        return top_16_deck_urls

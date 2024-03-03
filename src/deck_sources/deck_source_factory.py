from logging import Logger, getLogger
from src.deck.deck import Deck
from src.deck_sources.deck_source import DeckSource
from src.deck_sources.moxfield_source import MoxfieldSource
import os


class DeckSourceFactory:
    deck_sources: list[DeckSource]
    failed_lookups_file: str | None = "failed_lookups.txt"
    logger: Logger = getLogger("DeckSourceFactory")

    def __init__(self):
        self.deck_sources = [MoxfieldSource()]
        if self.failed_lookups_file:
            if not os.path.exists(self.failed_lookups_file):
                os.mknod(self.failed_lookups_file)
            

    def get_deck(self, uri: str) -> Deck | None:
        if not isinstance(uri, str):
            return None

        uri = uri.strip()
        if self._is_failure(uri):
            return None

        for deck_source in self.deck_sources:
            if deck_source.is_valid_target(uri):
                deck = deck_source.get_deck(uri)
                if deck is not None:
                    self.logger.info(f"Obtaining uri: {uri} from {deck_source.name} was successful")
                    return deck
                else:
                    self.logger.info(f"Obtaining uri: {uri} from {deck_source.name} was unsuccessful")
                    
        self._log_out_failed_lookup(uri)
        return None
    
    def _log_out_failed_lookup(self, uri: str) -> None:
        if (not self._is_failure(uri) and self.failed_lookups_file):
            self.logger.info(f"Could not find valid source for uri: {uri}, logging to file {self.failed_lookups_file}")

            with open(self.failed_lookups_file, "a") as f:
                f.write(f"{uri}\n")

    def _is_failure(self, uri: str) -> bool:
        if not self.failed_lookups_file:
            return False

        with open(self.failed_lookups_file, "r") as f:
            failed_lookups = f.readlines()

        return uri in failed_lookups
        

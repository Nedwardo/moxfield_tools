import json

from src.Cards.ApiCardFactory import ApiCardFactory
from src.Cards.DeckFactory import DeckFactory
from src.Cards.LocalCardFactory import LocalCardFactory
from src.moxfield_api_calls import cache_rog_si


def get_card_factory(source: str = "local") -> DeckFactory:
    if source == "api":
        return remote_api_card_factory()
    if source == "cached":
        return cached_remote_api_card_factory()
    if source == "local":
        return local_api_factory()
    raise ValueError(
        f"Source not recognized, received = {source}, expected: [api, cached, local]"
    )


def remote_api_card_factory() -> DeckFactory:
    cache_rog_si()
    return local_api_factory()


def cached_remote_api_card_factory(
    cached_file_address: str = "cached_api.json",
) -> DeckFactory:
    with open(cached_file_address) as f:
        cached_json = json.load(f)
    return ApiCardFactory(cached_json)


def local_api_factory() -> DeckFactory:
    return LocalCardFactory()

from abc import ABC, abstractmethod

import pandas as pd


class TournamentResultSource(ABC):
    base_url: str

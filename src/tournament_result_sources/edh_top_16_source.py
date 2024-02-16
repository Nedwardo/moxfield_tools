from io import StringIO
import pandas as pd
from src.session import Session


class EdhTop16Source:
    base_url: str
    headers: dict
    session: Session

    def __init__(self):
        self.base_url = "https://edhtop16.com/api"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session = Session()

    def get_all_decks(self) -> pd.DataFrame:
        data = {
            "standing": {"$lte": 16},
        }
        return self._make_api_request("req", data)

    def get_all_tournaments(self) -> pd.DataFrame:
        data = {"tournamentName": {"$regex": r""}}
        return self._make_api_request("list_tourneys", data)

    def _make_api_request(self, target_endpoint: str, data: dict) -> pd.DataFrame:
        target_url = f"{self.base_url}/{target_endpoint}"
        response = self.session.post(
            target_url,
            headers=self.headers,
            json=data,
            timeout=200,
        ).text
        if response[0] == "<":
            print(
                f"Bad request: {response} for request: POST {target_url}"
                f", headers={self.headers}, json={data}"
            )
            raise TypeError(
                f"Bad request: {response} for request: POST {target_url}"
                f", headers={self.headers}, json={data}"
            )
        return pd.read_json(
            StringIO(
                self.session.post(
                    target_url,
                    headers=self.headers,
                    json=data,
                    timeout=200,
                ).text
            )
        )

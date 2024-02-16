from typing import Union
import requests


class Session:
    instance: Union["Session", None] = None

    def __new__(cls, *args, **kwargs) -> "Session":
        if cls.instance:
            return cls.instance
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        self.request_session = requests.Session()

    def get(self, url: str, headers: dict | None) -> requests.Response:
        if headers:
            return self.request_session.get(url, headers=headers)
        return self.request_session.get(url)

    def post(
        self, url: str, headers: dict, json: dict, timeout: int = 20
    ) -> requests.Response:
        return self.request_session.post(
            url, headers=headers, json=json, timeout=timeout
        )

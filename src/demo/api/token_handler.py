import os
import time
import json
import requests
from typing import Dict

from src.demo.api.constants import (
    VISMA_CONNECT_CLIENT_ID,
    VISMA_CONNECT_TOKEN_URL,
    VISMA_CONNECT_KEY_STAGE,
    VISMA_CONNECT_API_SCOPE,
)

class TokenHandler:
    """
    Class for handling logic related to fetching API tokens from Visma Connect.
    Initialize a TokenHandler, and call the get_token method whenever a token is needed.
    """

    def __init__(self) -> None:
        self.visma_connect_client_secret = os.environ.get(VISMA_CONNECT_KEY_STAGE)
        self._fetch_new_token()

    def get_token(self):
        current_time = time.time()
        if (
            self.token != None
            and self.token_fetched_time != None
            and current_time - self.token_fetched_time <= self.expires_in
        ):
            return self.token
        else:
            self._fetch_new_token()
            return self.token

    def _fetch_new_token(self) -> None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = (
            f"client_secret={self.visma_connect_client_secret}"
            f"&client_id={VISMA_CONNECT_CLIENT_ID}"
            f"&grant_type=client_credentials"
            f"&Scope={VISMA_CONNECT_API_SCOPE}"
        )
        response = requests.post(VISMA_CONNECT_TOKEN_URL, headers=headers, data=payload)

        if response.status_code == 200:
            result: Dict = json.loads(response.text)
            self.token = result["access_token"]
            self.expires_in = result["expires_in"]
            self.token_fetched_time = time.time()
        else:
            print("Something went wrong when fetching token from Visma Connect")

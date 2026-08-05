import os


class PubMedApiClient:
    api_key = os.environ("pub_med_API_key")

    def __init__(self, api_key: str):
        self.api_key = api_key

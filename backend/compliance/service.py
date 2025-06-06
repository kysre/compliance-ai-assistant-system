import os
from enum import Enum

import requests
from system_prompt import SystemPromptProvider


class LightRagMode(Enum):
    NAIVE = "naive"
    LOCAL = "local"
    GLOBAL = "global"
    HYBRID = "hybrid"
    MIX = "mix"
    BYPASS = "bypass"


class LightRagClient:
    def __init__(self):
        self.host = os.getenv("LIGHTRAG_HOST", "http://lightrag:9621")
        self.headers = {
            "Content-Type": "application/json",
        }
        self.system_prompt_provider = SystemPromptProvider()

    def query(
        self,
        query: str,
        mode: LightRagMode,
        system_prompt_type: str = "chat",
        system_prompt: str = None,
    ) -> str:
        url = f"{self.host}/query"

        user_prompt = self.system_prompt_provider.get_system_prompt(
            system_prompt_type, system_prompt
        )

        response = requests.post(
            url,
            headers=self.headers,
            json=self._get_query_request(query, mode, user_prompt),
        )
        if response.status_code != 200:
            raise error(response.json()["detail"][0]["msg"])
        return response.json()["response"]

    @classmethod
    def _get_query_request(
        cls, query: str, mode: LightRagMode, user_prompt: str = None
    ) -> dict:
        # TODO: add history support for queries
        """
        "top_k": 1,
        "conversation_history": [
        {
            "additionalProp1": {}
        }
        ],
        "history_turns": 0,
        """
        data = {
            "query": query,
            "mode": mode.value,
        }
        if user_prompt:
            data["user_prompt"] = user_prompt
        return data

    def insert_texts(
        self, texts: [str], sources: [str] = None, ids: [str] = None
    ) -> None:
        url = f"{self.host}/document/texts"
        response = requests.post(
            url,
            headers=self.headers,
            json=self._get_insert_texts_request(texts, sources, ids),
        )
        if response.status_code != 200:
            raise error(response.json()["detail"][0]["msg"])

    @classmethod
    def _get_insert_texts_request(
        cls, texts: [str], sources: [str] = None, ids: [str] = None
    ) -> dict:
        data = {
            "texts": texts,
        }
        if sources:
            data["file_sources"] = sources
        if ids:
            data["ids"] = ids
        return data

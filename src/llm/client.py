from abc import abstractmethod, ABC
import httpx
from typing import AsyncGenerator, Optional, Any

class BaseLLMClient(ABC):

    @abstractmethod
    async def complete(
            self,
            query: str,
            system: Optional[str] = None,
            response_format: Optional[str] = None,
    ) -> Any:
        pass

    @abstractmethod
    async def stream(
            self,
            query: str,
            system: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        pass


class OpenAICompatibleClient(BaseLLMClient):

    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        self.http_client = http_client
        self.base_url = base_url

    @staticmethod
    def _extract_text(data: dict) -> str:
        if "choices" in data:
            choice = data["choices"][0]

            if "message" in choice:
                return choice["message"]["content"]

            if "text" in choice:
                return choice["text"]

        if "content" in data:
            return data["content"]

        raise ValueError(f"Unknown response format: {data}")

    async def complete(self, query, system=None, response_format=None):

        payload = {
            "messages": [
                {"role": "system", "content": system} if system else None,
                {"role": "user", "content": query},
            ],
            "stream": False,
        }

        if response_format:
            payload["response_format"] = {"type": response_format}

        payload["messages"] = [m for m in payload["messages"] if m]

        resp = await self.http_client.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload
        )
        resp.raise_for_status()

        data = resp.json()

        return self._extract_text(data)

    async def stream(self, query, system=None):

        payload = {
            "messages": [
                {"role": "system", "content": system} if system else None,
                {"role": "user", "content": query},
            ],
            "stream": True,
        }

        payload["messages"] = [m for m in payload["messages"] if m]

        async with self.http_client.stream(
            "POST",
            f"{self.base_url}/v1/chat/completions",
            json=payload
        ) as resp:
            resp.raise_for_status()

            async for line in resp.aiter_lines():
                if not line:
                    continue

                # для SSE формата (data: {...})
                if line.startswith("data:"):
                    line = line[len("data:"):].strip()

                if line == "[DONE]":
                    break

                yield line


class SimpleCompletionClient(BaseLLMClient):

    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        self.http_client = http_client
        self.base_url = base_url

    async def complete(self, query, system=None, response_format=None):

        prompt = query
        if system:
            prompt = f"{system}\n\n{query}"

        payload = {
            "prompt": prompt,
            "n_predict": 256
        }

        resp = await self.http_client.post(
            f"{self.base_url}/completion",
            json=payload
        )
        resp.raise_for_status()

        data = resp.json()

        return data.get("content") or data.get("text")

    async def stream(self, query, system=None):
        raise NotImplementedError("Streaming not supported")


class LLMClientFactory:

    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    def create(self, base_url: str):
        return SimpleCompletionClient(
            http_client=self.http_client,
            base_url=base_url
        )

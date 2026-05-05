from typing import Optional, AsyncGenerator

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

# провайдеры (можно менять)
from langchain_openai import ChatOpenAI


class AssistantService:
    def __init__(
        self,
        url_llm: str,
        model: str,
        provider: str = "openai",

        temperature: float = 0.2,
    ):
        self.url_llm = url_llm
        self.provider = provider
        self.model_name = model
        self.temperature = temperature

        self.llm: BaseChatModel = self._init_llm()

    def _init_llm(self) -> BaseChatModel:
        if self.provider == "openai":
            return ChatOpenAI(
                base_url=self.url_llm,
                model=self.model_name,
                temperature=self.temperature,
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=prompt))

        response = await self.llm.ainvoke(messages)

        return response.content

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:

        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=prompt))

        async for chunk in self.llm.astream(messages):
            if chunk.content:
                yield chunk.content

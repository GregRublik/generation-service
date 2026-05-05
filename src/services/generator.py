from typing import Callable

from services.prompt import PromptService
from services.unit_of_work import UnitOfWork
from llm.client import BaseLLMClient

from schemas.responses import GenerateRequest
from schemas.prompt import BuildPrompt, BuildPromptResponse


class GeneratorService:

    def __init__(
            self,
            prompt_service: PromptService,
            uow: UnitOfWork,
            llm_client: BaseLLMClient
    ):
        self.prompt_service = prompt_service
        self.llm_client = llm_client
        self.uow = uow

        self.mapping_methods = {
            "chat": self._chat,
            "generate": self._generate,
            "structured": self._structured,
            "summarize": self._summarize,
        }

    async def run(self, data: GenerateRequest):
        handler: Callable = self.mapping_methods.get(data.mode)

        if not handler:
            raise ValueError(f"Unknown mode: {data.mode}")

        return await handler(data)

    async def _generate(self, data: GenerateRequest):
        system_prompt = await self._build_prompt(data)
        if data.stream:

            return self.llm_client.stream(
                query=data.query,
                system=system_prompt.prompt
            )
        return await self.llm_client.complete(
            query=data.query,
            system=system_prompt.prompt
        )

    async def _chat(self, data: GenerateRequest):
        system_prompt = await self._build_prompt(data)
        return await self.llm_client.complete(
            query=data.query,
            system=system_prompt.prompt
        )

    async def _structured(self, data: GenerateRequest):
        system_prompt = await self._build_prompt(data)
        return await self.llm_client.complete(
            query=data.query,
            system=system_prompt.prompt,
            response_format="json"  # условный режим
        )

    async def _summarize(self, data: GenerateRequest):
        system_prompt = await self._build_prompt(data)
        return await self.llm_client.complete(
            query=data.query,
            system=system_prompt.prompt
        )

    async def _build_prompt(self, data: GenerateRequest) -> BuildPromptResponse:
        build_prompt_data = BuildPrompt(fields=data.fields)
        return await self.prompt_service.build_prompt(
            data.prompt_id,
            prompt_data=build_prompt_data
        )

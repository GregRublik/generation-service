from typing import Callable

from services import prompt, unit_of_work
from llm.client import LLMClient

from schemas.responses import GenerateRequest
from schemas.prompt import BuildPrompt

class GeneratorService:

    def __init__(
            self,
            prompt_service: prompt.PromptService,
            uow: unit_of_work.UnitOfWork,
            llm_client: LLMClient
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

    async def _generate(self, data):
        await self.llm_client.complete()


    async def _chat(self, data):
        pass

    async def _structured(self, data):
        pass
    async def _summarize(self, data):
        pass

    async def run(self, data: GenerateRequest):
        handler: Callable = self.mapping_methods.get(data.mode)

        if not handler:
            raise ValueError(f"Unknown mode: {data.mode}")

        return await handler(data)



    # async def generate(self, data: PayloadGenerate):
    #     build_prompt_data = BuildPrompt(
    #         fields=data.fields
    #     )
    #
    #     system_prompt = await self.prompt_service.build_prompt(data.prompt_id, prompt_data=build_prompt_data)
    #
    #     response = await self.assistant_service.generate(ready_prompt.prompt)
    #
    #     return response


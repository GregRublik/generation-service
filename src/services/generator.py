from services import prompt, unit_of_work, assistant

from schemas.generator import PayloadGenerate
from schemas.prompt import BuildPrompt

class GeneratorService:

    def __init__(
            self,
            prompt_service: prompt.PromptService,
            uow: unit_of_work.UnitOfWork,
            assistant_service: assistant.AssistantService
    ):
        self.prompt_service = prompt_service
        self.assistant_service = assistant_service
        self.uow = uow

    async def generate(self, data: PayloadGenerate):
        build_prompt_data = BuildPrompt(
            fields={
                "query": data.query,
                "contexts": data.contexts,
            }
        )

        ready_prompt = await self.prompt_service.build_prompt(data.prompt_id, prompt_data=build_prompt_data)

        response = await self.assistant_service.


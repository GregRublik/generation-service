from repositories.prompt import PromptRepository
from services.unit_of_work import UnitOfWork

from schemas.prompt import CreatePrompt, ChangePrompt


class PromptService:

    def __init__(self, prompt_repository: PromptRepository, uow: UnitOfWork):
        self.prompt_repository = prompt_repository
        self.uow = uow

    async def get_prompt(self, prompt_id: int):
        async with self.uow:
            return await self.prompt_repository.get_by_id(self.uow.session, prompt_id)

    async def get_prompts(self):
        async with self.uow:
            return await self.prompt_repository.get_all(self.uow.session)

    async def create_prompt(self, prompt_data: CreatePrompt):
        async with self.uow:
            return await self.prompt_repository.add_one(self.uow.session, prompt_data.model_dump(exclude_unset=True))

    async def change_prompt(self, prompt_id: int, prompt_data: ChangePrompt):
        async with self.uow:
            return await self.prompt_repository.change_one(
                self.uow.session, prompt_id, prompt_data.model_dump(exclude_unset=True)
            )

    async def delete_prompt(self, prompt_id: int):
        async with self.uow:
            return await self.prompt_repository.delete_by_id(self.uow.session, prompt_id)

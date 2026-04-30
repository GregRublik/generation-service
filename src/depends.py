from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.prompt import PromptRepository

from services.prompt import PromptService
from services.unit_of_work import UnitOfWork

from db.database import get_db_session


def get_prompt_repository() -> PromptRepository:
    return PromptRepository()

def get_uow_service(
    session: AsyncSession = Depends(get_db_session),
) -> UnitOfWork:
    return UnitOfWork(
        session=session,
    )

def get_prompt_service(
    prompt_repository: PromptRepository = Depends(get_prompt_repository),
    uow: UnitOfWork = Depends(get_uow_service),
) -> PromptService:
    return PromptService(
        prompt_repository=prompt_repository,
        uow=uow
    )
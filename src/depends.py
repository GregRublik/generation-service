from fastapi import Depends
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.prompt import PromptRepository
from services.generator import GeneratorService

from services.prompt import PromptService
from services.unit_of_work import UnitOfWork

from llm.client import LLMClientFactory

from db.database import get_db_session

from config import settings, SessionManager


def get_http_session(
        http_session: ClientSession = Depends(SessionManager.get_session),
) -> ClientSession:
    return http_session

# REPO
def get_prompt_repository() -> PromptRepository:
    return PromptRepository()


# SERVICES
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

def get_generator_service(
    prompt_service: PromptService = Depends(get_prompt_service),
    uow: UnitOfWork = Depends(get_uow_service),
    http_session: ClientSession = Depends(get_http_session),
) -> GeneratorService:

    factory = LLMClientFactory(
        http_session
    )
    client = factory.create(
        settings.llm.dsn
    )

    return GeneratorService(
        prompt_service,
        uow,
        llm_client=client
    )
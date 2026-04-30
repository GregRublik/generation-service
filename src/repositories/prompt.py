from repositories.base import SQLAlchemyRepository

from models.prompt import Prompt

class PromptRepository(SQLAlchemyRepository):
    model = Prompt
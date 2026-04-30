from repositories.base import SQLAlchemyRepository

from models.prompt import PromptT

class PromptRepository(SQLAlchemyRepository):
    model = Prompt
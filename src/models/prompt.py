from sqlalchemy import Column, String, JSON, Integer

from db.database import Base


class Prompt(Base):
    __tablename__ = 'generation_prompts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)

    fields = Column(JSON, nullable=False)

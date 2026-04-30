from pydantic import BaseModel

class BasePrompt(BaseModel):
    id: int

class PromptResponse(BasePrompt):
    name: str
    text: str

    fields: list[str]


class CreatePrompt(BaseModel):
    name: str
    text: str

    fields: list[str]

class ChangePrompt(CreatePrompt):
    pass

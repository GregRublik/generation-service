from pydantic import BaseModel

class BasePrompt(BaseModel):
    id: int

class PromptResponse(BasePrompt):
    name: str
    text: str

    fields: dict


class CreatePrompt(BaseModel):
    name: str
    text: str

    fields: dict

class ChangePrompt(CreatePrompt):
    pass

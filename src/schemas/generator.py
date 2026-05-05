from pydantic import BaseModel

class PayloadGenerate(BaseModel):
    prompt_id: int
    query: str
    contexts: dict


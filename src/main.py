from fastapi import FastAPI
import uvicorn

from api.v1.endpoints import prompts, responses
from config import settings

app = FastAPI()

app.include_router(prompts.router, tags=["prompts"])
app.include_router(responses.router, tags=["inference"])

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)

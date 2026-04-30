from fastapi import FastAPI
import uvicorn

from api.v1.endpoints import prompts
from config import settings

app = FastAPI()

app.include_router(prompts.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)

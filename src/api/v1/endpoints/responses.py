from typing import Any
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from schemas.responses import GenerateRequest
from services.generator import GeneratorService
from depends import get_generator_service

from schemas.response import ok

router = APIRouter(prefix="/responses")


@router.post("/generate")
async def generate(
    payload: GenerateRequest,
    generator_service: GeneratorService = Depends(get_generator_service),
):
    """Standard generation"""

    result = await generator_service.run(payload)

    # если stream → возвращаем StreamingResponse
    if payload.stream:

        async def event_stream():
            async for chunk in result:
                yield chunk

        return StreamingResponse(event_stream(), media_type="text/plain")

    return ok(result)

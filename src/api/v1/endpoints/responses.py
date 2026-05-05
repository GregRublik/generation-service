from fastapi import APIRouter, Depends
from schemas.responses import GenerateRequest

from services.generator import GeneratorService
from depends import get_generator_service

router = APIRouter(tags=["inference"], prefix="/responses")

@router.post("/generate")
async def generate(
    payload: GenerateRequest,
    generator_service: GeneratorService = Depends(get_generator_service),
):
    """Классическая генерация"""
    return await generator_service.run(payload)

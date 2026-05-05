from fastapi import APIRouter, Depends
from schemas.generator import PayloadGenerate

from services.generator import GeneratorService
from depends import get_generator_service

router = APIRouter(tags=["generate"], prefix="/generate")

@router.post("/")
async def generate(
    data: PayloadGenerate,
    generator_service: GeneratorService = Depends(get_generator_service),
):
    """Классическая генерация"""
    return await generator_service.generate(data)

@router.post("/chat")
async def generate_chat(
    # data: PayloadGenerate,
):
    """Генерация с историей чата"""
    pass

@router.post("/summary")
async def generate_summary():
    """Суммаризация найденых документов"""
    pass

@router.post("/structured")
async def generate_structured():
    """Герерация определенной структуры json"""
    pass

@router.post("/stream")
async def generate_stream():
    """стриминг токенов"""
    pass

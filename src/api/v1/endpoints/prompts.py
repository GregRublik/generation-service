from fastapi import APIRouter, Depends, status
from services.prompt import PromptService
from schemas.prompt import PromptResponse, ChangePrompt, CreatePrompt, BuildPrompt, BuildPromptResponse

from depends import get_prompt_service


router = APIRouter(tags=["prompts"], prefix="/prompts")


@router.get("/", response_model=list[PromptResponse])
async def get_prompts(
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Получить промпт"""
    return await prompt_service.get_prompts()


@router.post("/")
async def create_prompt(
    prompt_data: CreatePrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Создать промпт"""
    return await prompt_service.create_prompt(prompt_data)


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: int,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Получить промпт"""
    return await prompt_service.get_prompt(prompt_id)


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    prompt_data: ChangePrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Обновить промпт"""
    return await prompt_service.change_prompt(prompt_id, prompt_data)


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: int,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Удалить промпт"""
    await prompt_service.delete_prompt(prompt_id)


@router.post("/build-prompt/{prompt_id}", response_model=BuildPromptResponse)
async def build_prompt(
    prompt_id: int,
    prompt_data: BuildPrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Метод для проверки генерации промпта по данным"""
    return await prompt_service.build_prompt(prompt_id, prompt_data)
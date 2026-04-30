from fastapi import APIRouter, Depends, status
from services.prompt import PromptService
from schemas.prompt import PromptResponse, ChangePrompt, CreatePrompt

from depends import get_prompt_service


router = APIRouter(tags=["prompts"])


@router.get("/prompts", response_model=list[PromptResponse])
async def get_prompts(
    prompt_service: PromptService = Depends(get_prompt_service),
):
    return await prompt_service.get_prompts()


@router.post("/prompts")
async def create_prompt(
    prompt_data: CreatePrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    return await prompt_service.create_prompt(prompt_data)


@router.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: int,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    return await prompt_service.get_prompt(prompt_id)


@router.put("/prompts/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    prompt_data: ChangePrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    return await prompt_service.change_prompt(prompt_id, prompt_data)


@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: int,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    await prompt_service.delete_prompt(prompt_id)

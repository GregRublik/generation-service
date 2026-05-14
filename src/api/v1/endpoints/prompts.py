from typing import List

from fastapi import APIRouter, Depends, status
from services.prompt import PromptService
from schemas.prompt import PromptResponse, ChangePrompt, CreatePrompt, BuildPrompt, BuildPromptResponse
from schemas.response import APIResponse, ok

from depends import get_prompt_service




router = APIRouter(prefix="/prompts")


@router.get("/", response_model=APIResponse[List[PromptResponse]])
async def get_prompts(
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Get prompts"""
    return ok(await prompt_service.get_prompts())


@router.post("/", response_model=APIResponse[PromptResponse])
async def create_prompt(
    prompt_data: CreatePrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Create prompt"""
    return ok(await prompt_service.create_prompt(prompt_data))


@router.get("/{prompt_id}", response_model=APIResponse[PromptResponse])
async def get_prompt(
    prompt_id: int,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Get prompt"""
    return ok(await prompt_service.get_prompt(prompt_id))


@router.put("/{prompt_id}", response_model=APIResponse[PromptResponse])
async def update_prompt(
    prompt_id: int,
    prompt_data: ChangePrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Update prompt"""
    prompt = await prompt_service.change_prompt(prompt_id, prompt_data)
    return ok(prompt)


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: int,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Delete prompt"""
    await prompt_service.delete_prompt(prompt_id)


@router.post("/build/{prompt_id}", response_model=APIResponse[BuildPromptResponse])
async def build_prompt(
    prompt_id: int,
    prompt_data: BuildPrompt,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Build prompt and check"""
    building_prompt = await prompt_service.build_prompt(prompt_id, prompt_data)
    return ok(building_prompt)
from fastapi import APIRouter, HTTPException
from app.models import schemas
import logging

router = APIRouter()
logger = logging.getLogger("autochefpythonservice")


@router.post("/generate-recipe", response_model=schemas.RecipeResponse)
async def generate_recipe(request: schemas.RecipeRequest):
    if not request.prompt or not request.prompt.strip():
        # return structured invalid prompt error
        raise HTTPException(status_code=400, detail={"code": "INVALID_PROMPT", "message": "Prompt is required and cannot be blank."})

    try:
        # Minimal mock implementation: echo prompt as a simple recipe title
        recipe = schemas.Recipe(
            title=f"Recipe for: {request.prompt}",
            ingredients=[schemas.Ingredient(name="Salt", quantity=1, unit="tsp")],
            instructions="Mix ingredients and cook.",
            cookTimeMinutes=10,
        )

        return schemas.RecipeResponse(recipes=[recipe])
    except Exception as e:
        logger.error(f"Generation failed for prompt: {request.prompt}", exc_info=True)
        raise HTTPException(status_code=500, detail={"code": "GENERATION_FAILED", "message": "Failed to generate recipe."})

from fastapi import APIRouter, HTTPException
from app.models import schemas
from app.services.bedrock_service import BedrockService
import logging

router = APIRouter()
logger = logging.getLogger("autochefpythonservice")

# Initialize BedrockService
bedrock_service = BedrockService()


@router.post("/generate-recipe", response_model=schemas.RecipeResponse)
async def generate_recipe(request: schemas.RecipeRequest):
    
    try:
        # Use BedrockService to generate real recipe
        recipe = bedrock_service.generate_recipe(
            prompt=request.prompt,
            dietary_preferences=request.dietaryPreferences,
            locale=request.locale
        )

        return schemas.RecipeResponse(recipes=[recipe])
    except Exception as e:
        logger.error(f"Generation failed for prompt: {request.prompt}", exc_info=True)
        raise HTTPException(status_code=500, detail={"code": "GENERATION_FAILED", "message": "Failed to generate recipe."})

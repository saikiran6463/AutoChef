from fastapi import APIRouter, HTTPException
from app.models import schemas

router = APIRouter()


@router.post("/generate-recipe", response_model=schemas.RecipeResponse)
async def generate_recipe(request: schemas.RecipeRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt is required")

    # Minimal mock implementation: echo prompt as a simple recipe title
    recipe = schemas.Recipe(
        title=f"Recipe for: {request.prompt}",
        ingredients=[schemas.Ingredient(name="Salt", quantity=1, unit="tsp")],
        instructions="Mix ingredients and cook.",
        cookTimeMinutes=10,
    )

    return schemas.RecipeResponse(recipes=[recipe])

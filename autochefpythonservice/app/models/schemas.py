from typing import List, Optional
from pydantic import BaseModel


class RecipeRequest(BaseModel):
    prompt: str
    dietaryPreferences: Optional[List[str]] = None
    locale: Optional[str] = None


class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None


class Recipe(BaseModel):
    title: str
    ingredients: List[Ingredient]
    instructions: str
    cookTimeMinutes: Optional[int] = None


class RecipeResponse(BaseModel):
    recipes: List[Recipe]


class ErrorResponse(BaseModel):
    code: str
    message: str

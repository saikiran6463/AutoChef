package com.autochef.autochefjavaservice.service;

import com.autochef.autochefjavaservice.dto.RecipeRequest;
import com.autochef.autochefjavaservice.dto.RecipeResponse;

public interface RecipeService {
    RecipeResponse generateRecipe(RecipeRequest request);
}

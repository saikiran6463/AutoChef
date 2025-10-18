package com.autochef.autochefjavaservice.controller;

import com.autochef.autochefjavaservice.dto.RecipeRequest;
import com.autochef.autochefjavaservice.dto.RecipeResponse;
import com.autochef.autochefjavaservice.service.RecipeService;
import com.autochef.autochefjavaservice.service.ValidationService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class RecipeController {

    private final RecipeService recipeService;
    private final ValidationService validationService;

    public RecipeController(RecipeService recipeService, ValidationService validationService) {
        this.recipeService = recipeService;
        this.validationService = validationService;
    }

    @PostMapping("/generate-recipe")
    public RecipeResponse generateRecipe(@RequestBody RecipeRequest request) {
        // Validate the request - will throw ValidationException if invalid
        validationService.validateRecipeRequest(request);
        
        // Process the request - will throw DownstreamServiceException if downstream fails
        return recipeService.generateRecipe(request);
    }
}

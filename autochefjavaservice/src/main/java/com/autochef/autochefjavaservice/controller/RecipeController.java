package com.autochef.autochefjavaservice.controller;

import com.autochef.autochefjavaservice.dto.RecipeRequest;
import com.autochef.autochefjavaservice.dto.RecipeResponse;
import com.autochef.autochefjavaservice.service.RecipeService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class RecipeController {

    private final RecipeService recipeService;

    public RecipeController(RecipeService recipeService) {
        this.recipeService = recipeService;
    }



    @PostMapping("/generate-recipe")
    public RecipeResponse generateRecipe(@RequestBody RecipeRequest request) {
        return recipeService.generateRecipe(request);
    }
}

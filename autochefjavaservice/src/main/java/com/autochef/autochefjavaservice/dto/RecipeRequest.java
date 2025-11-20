package com.autochef.autochefjavaservice.dto;

import java.util.List;

import com.autochef.autochefjavaservice.config.CuisineDeserializer;
import com.autochef.autochefjavaservice.enums.Cuisine;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

/**
 * Represents the request body for generating a new recipe.
 * This DTO defines the contract for the data clients must send.
 */
public record RecipeRequest(
    String prompt,
    List<String> dietaryPreferences,
    @JsonDeserialize(using = CuisineDeserializer.class)
    Cuisine cuisine
) {}

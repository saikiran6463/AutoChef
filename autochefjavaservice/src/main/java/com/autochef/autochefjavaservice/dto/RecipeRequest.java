package com.autochef.autochefjavaservice.dto;

import java.util.List;

/**
 * Represents the request body for generating a new recipe.
 * This DTO defines the contract for the data clients must send.
 */
public record RecipeRequest(
    String prompt,
    List<String> dietaryPreferences,
    String locale
) {}

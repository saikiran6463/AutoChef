package com.autochef.autochefjavaservice.dto;

import java.util.List;

/**
 * Represents a single recipe.
 * This DTO is composed of other DTOs (a List of Ingredients).
 */
public record Recipe(
    String title,
    List<Ingredient> ingredients,
    String instructions,
    Integer cookTimeMinutes
) {}

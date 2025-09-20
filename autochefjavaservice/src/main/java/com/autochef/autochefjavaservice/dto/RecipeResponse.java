package com.autochef.autochefjavaservice.dto;

import java.util.List;

/**
 * Acts as a wrapper for API responses that return a list of recipes.
 * This is a best practice for API design to allow for future additions of metadata
 * (e.g., pagination details) without creating breaking changes.
 */
public record RecipeResponse(
    List<Recipe> recipes
) {}

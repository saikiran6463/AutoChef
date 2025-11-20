package com.autochef.autochefjavaservice.service;

import com.autochef.autochefjavaservice.constants.ErrorCode;
import com.autochef.autochefjavaservice.dto.RecipeRequest;
import com.autochef.autochefjavaservice.enums.Cuisine;
import com.autochef.autochefjavaservice.exception.ValidationException;
import org.springframework.stereotype.Service;

/**
 * Service responsible for validating incoming requests.
 * Centralizes validation logic for better maintainability.
 */
@Service
public class ValidationService {

    /**
     * Validates a RecipeRequest to ensure all required fields are present and valid.
     * 
     * @param request the RecipeRequest to validate
     * @throws ValidationException if validation fails
     */
    public void validateRecipeRequest(RecipeRequest request) {
        validatePrompt(request.prompt());
        validateCuisine(request.cuisine());
        // Future validations can be added here (e.g., dietary preferences, locale)
    }

    /**
     * Validates that the prompt is not null, empty, or only whitespace.
     * 
     * @param prompt the prompt to validate
     * @throws ValidationException if prompt is invalid
     */
    private void validatePrompt(String prompt) {
        if (prompt == null || prompt.trim().isEmpty()) {
            throw new ValidationException(ErrorCode.INVALID_PROMPT);
        }
    }

    /*
     * Validates that the cuisine is not null and is a valid enum value.
     *
     * @param cuisine the cuisine to validate
     * @throws ValidationException if cuisine is invalid
     */
    private void validateCuisine(Cuisine cuisine) {
        if (cuisine == null) {
            throw new ValidationException(ErrorCode.INVALID_CUISINE);
        }
    }
}
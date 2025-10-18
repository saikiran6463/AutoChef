package com.autochef.autochefjavaservice.constants;

/**
 * Defines standardized error codes and messages for the AutoChef API.
 * This ensures consistent error handling across the application.
 */
public enum ErrorCode {
    INVALID_PROMPT("INVALID_PROMPT", "Prompt is required and cannot be blank."),
    BAD_REQUEST("BAD_REQUEST", "Malformed request or invalid JSON."),
    LLM_DOWN("LLM_DOWN", "Failed to reach recipe generation service."),
    LLM_TIMEOUT("LLM_TIMEOUT", "Recipe generation service timed out."),
    INTERNAL_ERROR("INTERNAL_ERROR", "An unexpected error occurred.");

    private final String code;
    private final String message;

    ErrorCode(String code, String message) {
        this.code = code;
        this.message = message;
    }

    public String getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }
}
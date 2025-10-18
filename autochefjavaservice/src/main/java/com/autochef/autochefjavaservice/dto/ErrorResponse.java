package com.autochef.autochefjavaservice.dto;

/**
 * Represents a standardized error response body.
 * Using a consistent error structure across the API is a best practice.
 */
public record ErrorResponse(
    int status,
    String code,
    String message
) {}

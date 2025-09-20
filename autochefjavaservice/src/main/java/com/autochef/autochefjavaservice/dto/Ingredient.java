package com.autochef.autochefjavaservice.dto;

/**
 * Represents a single ingredient with its quantity and unit.
 * This is a Data Transfer Object (DTO) used as part of the Recipe DTO.
 * Using a record for immutability and conciseness.
 */
public record Ingredient(
    String name,
    double quantity,
    String unit
) {}

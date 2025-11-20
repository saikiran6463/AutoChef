package com.autochef.autochefjavaservice.enums;

public enum Cuisine {
    ITALIAN,
    MEXICAN,
    INDIAN,
    THAI,
    OTHER;

    //Method to handle case-insensitive parsing of string to Cuisine enum
    public static Cuisine fromString(String cuisineStr) {
        if (cuisineStr == null) {
            return null;
        }
        try {
            return Cuisine.valueOf(cuisineStr.trim().toUpperCase());
        } catch (IllegalArgumentException e) {
            return null; // Return null for invalid values
        }
    }
}





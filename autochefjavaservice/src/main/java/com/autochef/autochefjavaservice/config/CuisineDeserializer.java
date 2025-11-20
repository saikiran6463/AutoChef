package com.autochef.autochefjavaservice.config;

import com.autochef.autochefjavaservice.enums.Cuisine;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import java.io.IOException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;

public class CuisineDeserializer extends StdDeserializer<Cuisine> {
    
    public CuisineDeserializer() {
        super(Cuisine.class);
    }

    @Override
    public Cuisine deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
        String cuisineStr = p.getValueAsString();
        return Cuisine.fromString(cuisineStr);
    }

    
}

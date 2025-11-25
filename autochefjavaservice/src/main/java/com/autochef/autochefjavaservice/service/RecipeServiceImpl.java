package com.autochef.autochefjavaservice.service;

import com.autochef.autochefjavaservice.constants.ErrorCode;
import com.autochef.autochefjavaservice.dto.Recipe;
import com.autochef.autochefjavaservice.dto.RecipeRequest;
import com.autochef.autochefjavaservice.dto.RecipeResponse;
import com.autochef.autochefjavaservice.entity.RecipeEntity;
import com.autochef.autochefjavaservice.exception.DownstreamServiceException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.time.Duration;
import java.util.concurrent.TimeoutException;

@Service
public class RecipeServiceImpl implements RecipeService {

    private final WebClient webClient;
    private final DynamoDBService dynamoDBService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public RecipeServiceImpl(WebClient webClient, DynamoDBService dynamoDBService) {
        this.webClient = webClient;
        this.dynamoDBService = dynamoDBService;
    }

    @Override
    @Cacheable(value = "recipes")
    public RecipeResponse generateRecipe(RecipeRequest request) {
        try {
           RecipeResponse recipeResponse = webClient.post()
                    .uri("") // The base URL is already configured in the WebClient bean
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(RecipeResponse.class)
                    .timeout(Duration.ofSeconds(30)) // 30 second timeout
                    .block(); // Block to wait for the response

           // Convert RecipeResponse to RecipeEntity and save to DynamoDB
           if (recipeResponse != null && !recipeResponse.recipes().isEmpty()) {
            Recipe recipe = recipeResponse.recipes().get(0); // Get the first recipe from the response

            RecipeEntity recipeEntity = new RecipeEntity();
            recipeEntity.setRecipeId(java.util.UUID.randomUUID().toString()); // Generate a unique ID
            recipeEntity.setTitle(recipe.title());
            
            // Convert ingredients list to JSON string
            try {
                String ingredientsJson = objectMapper.writeValueAsString(recipe.ingredients());
                recipeEntity.setIngredients(ingredientsJson);
            } catch (JsonProcessingException e) {
                throw new RuntimeException("Failed to serialize ingredients", e);
            }
            
            recipeEntity.setInstructions(recipe.instructions());
            recipeEntity.setCookTimeMinutes(recipe.cookTimeMinutes());
            recipeEntity.setPrompt(request.prompt());
            recipeEntity.setTimestamp(java.time.Instant.now().toString());
            recipeEntity.setCuisine(request.cuisine().name());
            recipeEntity.setDietaryPreferences(request.dietaryPreferences());
            
            dynamoDBService.saveRecipe(recipeEntity); // Save to DynamoDB
           }        

            return recipeResponse; // Return the original response to the client
                    
        } catch (WebClientRequestException ex) {
            // Connection issues, DNS problems, network failures
            throw new DownstreamServiceException(ErrorCode.LLM_DOWN, ex);
            
        } catch (WebClientResponseException ex) {
            // HTTP error responses from downstream service (4xx, 5xx)
            if (ex.getStatusCode().is5xxServerError()) {
                // Python service returned 500, 502, 503, etc.
                throw new DownstreamServiceException(ErrorCode.LLM_DOWN, ex);
            } else {
                // Python service returned 400, 401, 404, etc. 
                // This might indicate our request was malformed
                throw new DownstreamServiceException(ErrorCode.LLM_DOWN, ex);
            }
            
        } catch (Exception ex) {
            // Check if it's a timeout exception (can be wrapped in other exceptions)
            if (ex.getCause() instanceof TimeoutException || 
                ex instanceof TimeoutException ||
                ex.getMessage().contains("timeout") || 
                ex.getMessage().contains("Timeout")) {
                throw new DownstreamServiceException(ErrorCode.LLM_TIMEOUT, ex);
            }
            // For any other unexpected exception
            throw new DownstreamServiceException(ErrorCode.LLM_DOWN, ex);
        }
    }
}

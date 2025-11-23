package com.autochef.autochefjavaservice.service;

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;

import java.util.List;

import org.springframework.stereotype.Service;

import com.autochef.autochefjavaservice.entity.RecipeEntity;

@Service
public class DynamoDBService {
    // This class will contain methods to interact with DynamoDB
    // such as saving a recipe, retrieving a recipe, etc.

    private final DynamoDbEnhancedClient dynamoDbEnhancedClient;

    // Creating RecipeEntity reference
     private final DynamoDbTable<RecipeEntity> recipeTable;

    public DynamoDBService(DynamoDbEnhancedClient dynamoDbEnhancedClient) {
        this.dynamoDbEnhancedClient = dynamoDbEnhancedClient;
        this.recipeTable = dynamoDbEnhancedClient.table("AutoChef-Recipes", TableSchema.fromBean(RecipeEntity.class));
    }

    // Method to save a recipe
    public void saveRecipe(RecipeEntity recipe) {
        recipeTable.putItem(recipe);
    }

    // Method to retrieve a recipe by ID
    public RecipeEntity getRecipeById(String recipeId) {
        return recipeTable.getItem(r -> r.key(k -> k.partitionValue(recipeId)));
    }

    // Method to get all recipes
    public List<RecipeEntity> getAllRecipes() {
        return recipeTable.scan().items().stream().toList();
    }
}

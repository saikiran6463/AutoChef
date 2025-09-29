package com.autochef.autochefjavaservice.service;

import com.autochef.autochefjavaservice.dto.RecipeRequest;
import com.autochef.autochefjavaservice.dto.RecipeResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class RecipeServiceImpl implements RecipeService {

    private final WebClient webClient;

    public RecipeServiceImpl(WebClient webClient) {
        this.webClient = webClient;
    }

    @Override
    public RecipeResponse generateRecipe(RecipeRequest request) {
        return webClient.post()
                .uri("") // The base URL is already configured in the WebClient bean
                .bodyValue(request)
                .retrieve()
                .bodyToMono(RecipeResponse.class)
                .block(); // Block to wait for the response
    }
}

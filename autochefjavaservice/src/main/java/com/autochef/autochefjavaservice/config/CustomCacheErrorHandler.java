package com.autochef.autochefjavaservice.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.cache.Cache;
import org.springframework.stereotype.Component;
import org.springframework.cache.interceptor.CacheErrorHandler;

@Component
public class CustomCacheErrorHandler implements CacheErrorHandler {

    private static final Logger logger = LoggerFactory.getLogger(CustomCacheErrorHandler.class);

    @Override
    public void handleCacheGetError(RuntimeException exception, Cache cache, Object key) {
        logger.warn("Failed to GET from cache {} for key {}: {}", cache.getName(), key, exception.getMessage());
        // So we can continue without cache and fall back to bedrock
    }

    @Override
    public void handleCachePutError(RuntimeException exception, Cache cache, Object key, Object value) {
        logger.warn("Failed to PUT to cache {} for key {}: {}", cache.getName(), key, exception.getMessage());
        // So we can continue without cache
    }

    @Override
    public void handleCacheEvictError(RuntimeException exception, Cache cache, Object key) {
        logger.warn("Failed to EVICT from cache {} for key {}: {}", cache.getName(), key, exception.getMessage());
        // So we can continue without cache
    }

    @Override
    public void handleCacheClearError(RuntimeException exception, Cache cache) {
        logger.warn("Failed to CLEAR cache {}: {}", cache.getName(), exception.getMessage());
        // So we can continue without cache and fall back to bedrock
} 
}
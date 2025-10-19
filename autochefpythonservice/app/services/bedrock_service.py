"""
BedrockService - AWS Bedrock integration for AutoChef recipe generation.

This service handles all interactions with AWS Bedrock Claude models,
providing a clean interface for recipe generation.
"""

import boto3
import json
import logging
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError
from .prompt_builder import PromptBuilder
from ..models.schemas import Recipe, Ingredient

logger = logging.getLogger("autochefpythonservice.bedrock")


class BedrockService:
    """
    Service class for AWS Bedrock Claude model interactions.
    
    Handles:
    - Bedrock client initialization
    - Recipe generation prompts
    - Response parsing and validation
    - Error handling for Bedrock-specific issues
    """
    
    def __init__(self):
        """Initialize the Bedrock service with client and configuration."""
        self.region_name = 'us-east-1'
        self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
        
        # Initialize prompt builder for all prompt engineering
        self.prompt_builder = PromptBuilder()
        
        # Initialize Bedrock Runtime client
        try:
            self.bedrock_runtime = boto3.client(
                'bedrock-runtime', 
                region_name=self.region_name
            )
            logger.info(f"BedrockService initialized successfully with model: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    def generate_recipe(self, prompt: str, dietary_preferences: Optional[List[str]] = None, locale: Optional[str] = None) -> Recipe:
        """
        Generate a recipe using Claude 3 Haiku based on the provided prompt.
        
        Args:
            prompt (str): User's recipe request (e.g., "I have chicken and garlic")
            dietary_preferences (list, optional): Dietary restrictions/preferences
            locale (str, optional): Cooking style/locale preference
            
        Returns:
            Recipe: Parsed recipe DTO from Claude's response
            
        Raises:
            ClientError: When Bedrock API call fails
            Exception: For other unexpected errors
        """
        # Log prompt summary for debugging
        prompt_summary = self.prompt_builder.get_prompt_summary(prompt, dietary_preferences, locale)
        logger.info(f"Generating recipe - Base: '{prompt}', Dietary: {prompt_summary['dietary_preferences']}, Locale: {prompt_summary['locale']}")
        
        try:
            # Use PromptBuilder to create the combined prompt
            combined_prompt = self.prompt_builder.build_combined_prompt(prompt, dietary_preferences, locale)
            messages = [
                {
                    "role": "user",
                    "content": [{"text": combined_prompt}]
                }
            ]
            
            # Call Bedrock with our prompt
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig={
                    'maxTokens': 1000,    # Allow longer responses for recipes
                    'temperature': 0.3    # Slightly creative but still focused
                }
            )
            
            # Extract the response text
            response_text = response['output']['message']['content'][0]['text']
            
            # Log token usage for monitoring
            input_tokens = response['usage']['inputTokens']
            output_tokens = response['usage']['outputTokens']
            logger.info(f"Recipe generated successfully. Tokens - Input: {input_tokens}, Output: {output_tokens}")
            
            # Fix common JSON issues (fractions like 1/2 -> 0.5)
            import re
            fixed_text = re.sub(r'"quantity":\s*(\d+)/(\d+)', 
                               lambda m: f'"quantity": {int(m.group(1)) / int(m.group(2))}', 
                               response_text)
            
            # Simple JSON parsing - let it fail fast if invalid
            try:
                recipe_data = json.loads(fixed_text)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {e}")
                logger.error(f"Original response: {response_text[:200]}...")
                logger.error(f"Fixed response: {fixed_text[:200]}...")
                raise
            
            # Convert to Recipe DTO - let Pydantic handle validation
            recipe = Recipe(**recipe_data)
            
            return recipe
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"Bedrock ClientError - {error_code}: {error_message}")
            raise
            
        except Exception as e:
            logger.error(f"Unexpected error in recipe generation: {e}")
            raise
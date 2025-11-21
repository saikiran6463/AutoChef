"""
PromptBuilder - Handles all prompt engineering for AutoChef recipe generation.

This class is responsible for:
- Building system prompts that define AutoChef's persona
- Constructing user prompts with dynamic requirements
- Combining prompts for Bedrock API compatibility
- Managing prompt templates and variations
"""

from typing import List, Optional


class PromptBuilder:
    """
    Handles all prompt engineering logic for AutoChef recipe generation.
    
    Separates prompt construction from Bedrock API interaction to improve
    code organization, testability, and maintainability.
    """
    
    def __init__(self):
        """Initialize the PromptBuilder."""
        # Could add configuration here later (prompt templates, etc.)
        pass
    
    def build_system_prompt(self) -> str:
        """
        Build the system prompt that defines AutoChef's persona and output format.
        
        This prompt establishes:
        - AutoChef's identity as an expert culinary assistant
        - Consistent JSON output format requirements
        - Quality guidelines for recipe generation
        
        Returns:
            str: The complete system prompt
        """
        return """You are AutoChef, an expert culinary assistant with extensive knowledge of cooking techniques, flavor combinations, and practical recipe development.

Your role is to create detailed, practical recipes that home cooks can successfully execute. You have expertise in:
- International cuisines and cooking techniques
- Ingredient substitutions and dietary adaptations
- Proper cooking times and temperatures
- Kitchen equipment and cooking methods
- Food safety and preparation best practices

CRITICAL: You must respond with ONLY valid JSON in this exact format:
{
    "title": "Creative, appetizing recipe name",
    "ingredients": [
        {"name": "ingredient name", "quantity": number, "unit": "measurement unit"},
        {"name": "ingredient name", "quantity": number, "unit": "measurement unit"}
    ],
    "instructions": "Clear, step-by-step cooking directions with specific techniques and timing",
    "cookTimeMinutes": number
}

Guidelines for your responses:
- Create practical recipes using common, accessible ingredients
- Provide specific quantities and measurements
- Write clear, detailed cooking instructions
- Include realistic cooking times
- Ensure recipes are achievable for home cooks
- Be creative with titles while keeping them descriptive
- Do not include any text outside the JSON response"""

    def build_user_prompt(self, prompt: str,  cuisine: str, dietary_preferences: Optional[List[str]] = None) -> str:
        """
        Build the user prompt that incorporates specific recipe requirements.
        
        Args:
            prompt (str): User's recipe request
            dietary_preferences (list, optional): Dietary restrictions
            cuisine (str): Cuisine type (e.g., "INDIAN", "ITALIAN", "MEXICAN", "THAI")
        Returns:
            str: The complete user prompt with all requirements
        """
        # Start with the base request
        user_prompt = f"Create a recipe based on this request: {prompt}"
        
        # Add dietary preferences if provided
        if dietary_preferences and len(dietary_preferences) > 0:
            preferences_text = ", ".join(dietary_preferences)
            user_prompt += f"\n\nDietary requirements: {preferences_text}"
            user_prompt += "\nEnsure the recipe accommodates these dietary needs."
        
        # Add cuisine preference
        if cuisine:
            user_prompt += f"\n\nCuisine preference: {cuisine}"
            user_prompt += "\nFocus on this cuisine style in the recipe."
        
        # Final JSON reminder
        user_prompt += "\n\nProvide your response as valid JSON only, following the exact format specified above."
        
        return user_prompt

    def build_combined_prompt(self, prompt: str,  cuisine: str, dietary_preferences: Optional[List[str]] = None) -> str:
        """
        Build a combined prompt that includes both system instructions and user request.
        
        Since Bedrock converse API only supports user/assistant roles, we combine
        the system prompt and user prompt into a single user message.
        
        Args:
            prompt (str): User's recipe request
            dietary_preferences (list, optional): Dietary restrictions
            cuisine (str): Cuisine type (e.g., "INDIAN", "ITALIAN", "MEXICAN", "THAI")            
        Returns:
            str: The complete combined prompt ready for Bedrock API
        """
        # Start with system instructions (AutoChef persona)
        combined_prompt = self.build_system_prompt()
        
        # Add clear separator and user request section
        combined_prompt += "\n\n" + "="*50 + "\n"
        combined_prompt += "USER REQUEST:\n"

        # Add the user-specific prompt
        user_section = self.build_user_prompt(prompt, dietary_preferences, cuisine)
        combined_prompt += user_section
        
        return combined_prompt

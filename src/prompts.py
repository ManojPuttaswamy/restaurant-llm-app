from langchain_core.prompts import PromptTemplate

BRAND_KIT_JSON_SCHEMA = """
Return ONLY valid JSON (no markdown, no backticks) with this exact structure:
{{
  "restaurant_name": string,
  "tagline": string,
  "brand_story": string,
  "ambience": {{
    "vibe_keywords": [string, string, string, string, string],
    "music": string,
    "interior": string
  }},
  "target_customer": {{
    "persona": string,
    "why_they_come": string
  }}
}}
"""

MENU_JSON_SCHEMA = """
Return ONLY valid JSON (no markdown, no backticks) with this exact structure:
{{
  "menu": [
    {{
      "category": "Starter" | "Main" | "Dessert" | "Drink",
      "item": string,
      "description": string,
      "price_usd": number
    }}
  ]
}}
Rules:
- Exactly 10 items total
- At least: 2 Starters, 4 Mains, 2 Desserts, 2 Drinks
- No duplicates
- Prices should be sensible for the selected price range
"""

def brand_kit_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["cuisine", "theme", "price_range"],
        template=(
            "You are creating a premium restaurant concept.\n"
            "Cuisine: {cuisine}\n"
            "Theme: {theme}\n"
            "Price range: {price_range}\n\n"
            f"{BRAND_KIT_JSON_SCHEMA}\n\n"
            "Make the name feel brandable and memorable."
        ),
    )

def menu_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["restaurant_name", "cuisine", "theme", "price_range", "dietary_notes"],
        template=(
            "Create a menu for the restaurant.\n"
            "Restaurant name: {restaurant_name}\n"
            "Cuisine: {cuisine}\n"
            "Theme: {theme}\n"
            "Price range: {price_range}\n"
            "Dietary constraints (if any): {dietary_notes}\n\n"
            f"{MENU_JSON_SCHEMA}\n\n"
            "Ensure items match the cuisine + theme. If dietary constraints exist, adapt items accordingly."
        ),
    )
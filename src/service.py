from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from .prompts import brand_kit_prompt, menu_prompt
from .utils import extract_json

SYSTEM = "You are a JSON generator. You must output ONLY valid JSON. No markdown, no code fences, no commentary."

def _call_llm_json(llm, text: str) -> Dict[str, Any]:
    out = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=text)])
    raw = out.content if hasattr(out, "content") else str(out)
    return extract_json(raw)

def generate_brand_kit(llm, cuisine: str, theme: str, price_range: str) -> Dict[str, Any]:
    prompt = brand_kit_prompt()
    text = prompt.format(cuisine=cuisine, theme=theme, price_range=price_range)
    return _call_llm_json(llm, text)

def generate_menu(
    llm,
    restaurant_name: str,
    cuisine: str,
    theme: str,
    price_range: str,
    dietary_notes: str,
) -> Dict[str, Any]:
    prompt = menu_prompt()
    text = prompt.format(
        restaurant_name=restaurant_name,
        cuisine=cuisine,
        theme=theme,
        price_range=price_range,
        dietary_notes=dietary_notes or "None",
    )
    return _call_llm_json(llm, text)

def generate_full_concept(llm, cuisine: str, theme: str, price_range: str, dietary_notes: str = "") -> Dict[str, Any]:
    brand = generate_brand_kit(llm, cuisine, theme, price_range)
    restaurant_name = (brand.get("restaurant_name") or "").strip() or f"{cuisine} House"
    menu = generate_menu(llm, restaurant_name, cuisine, theme, price_range, dietary_notes)
    return {"brand": brand, "menu": menu}
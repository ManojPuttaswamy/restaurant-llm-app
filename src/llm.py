from langchain_openai import ChatOpenAI

def build_llm(openai_api_key: str, temperature: float = 0.6) -> ChatOpenAI:
    return ChatOpenAI(
        temperature=temperature,
        api_key=openai_api_key,
        model="gpt-4o-mini",
        model_kwargs={"response_format": {"type": "json_object"}},
    )
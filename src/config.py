import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise ValueError("OPENAI_API_KEY is missing. Add it to .env (local) or Secrets (deployment).")
    return key
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"

def generate(prompt: str, system: str = "", max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system if system else None,
                    temperature=0.3,
                    max_output_tokens=2048,
                ),
            )
            return response.text
        except Exception as e:
            wait = 2 ** attempt
            print(f"[Retry {attempt + 1}/{max_retries}] Error: {e} — waiting {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"[LLM Failed] All {max_retries} attempts failed.")

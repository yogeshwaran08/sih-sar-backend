import base64
import json
import requests

from app.config import settings

GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_MODEL = "gemini-1.5-flash"  # you can change to gemini-1.5-pro if needed


def call_gemini_image_and_text(prompt: str, image_bytes: bytes, mime_type: str = "image/png") -> str:
    """
    Calls Gemini (REST API) with an image + text prompt and returns the generated text.
    """

    # v1 endpoint (important: NOT v1beta)
    url = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"

    # Encode image as base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64,
                        }
                    },
                    {
                        "text": prompt
                    },
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 1.0,
            "topK": 32,
            "maxOutputTokens": 4096,
        },
    }

    params = {"key": GEMINI_API_KEY}
    headers = {"Content-Type": "application/json"}

    resp = requests.post(url, params=params, headers=headers, data=json.dumps(payload), timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # Basic extraction of first candidate text
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"No candidates returned from Gemini. Raw response: {data}")

    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        raise RuntimeError(f"No content parts in first candidate. Raw response: {data}")

    # Usually the first part contains the text
    return parts[0].get("text", "")

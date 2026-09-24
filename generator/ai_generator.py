import json
import os
from google import genai


def generate_ai_tests(test_cases):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an API test automation engineer.

Given these API test cases:

{json.dumps(test_cases, indent=2)}

Generate additional useful API tests.

Focus on:
- invalid input
- missing required fields
- boundary values
- unauthorized requests
- invalid IDs
- incorrect HTTP methods

Return ONLY valid JSON.

Format:
[
  {{
    "name": "...",
    "method": "GET",
    "url": "...",
    "headers": {{}},
    "body": null,
    "expected_status": 400,
    "reason": "..."
  }}
]
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def save_ai_tests(test_cases, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2)
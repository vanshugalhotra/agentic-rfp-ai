from typing import Dict
import json
import re


NORMALIZED_KEYS = [
    "category",
    "cable_type",
    "armored",
    "conductor_material",
    "conductor_size",
    "voltage_rating",
    "standards"
]


def normalize_spec_block_llm(llm_client, raw_text: str) -> Dict:
    """
    Uses LLM to normalize unstructured spec text into structured fields.
    """

    prompt = f"""
You are a technical specification normalization assistant.

TASK:
Extract and normalize cable specifications into structured fields.

STRICT RULES:
- Use ONLY the provided text
- Do NOT invent values
- If a value is missing, return null
- Output VALID JSON ONLY
- No explanations, no markdown

FIELDS:
{NORMALIZED_KEYS}

TEXT:
{raw_text}
"""

    response = llm_client.generate(prompt)

    # Defensive JSON extraction
    match = re.search(r"\{.*\}", response, re.S)
    if not match:
        print("⚠️ LLM did not return valid JSON")
        return {}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        print("⚠️ Failed to parse LLM JSON output")
        return {}

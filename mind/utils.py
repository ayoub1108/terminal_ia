import json

def safe_parse_json(text: str):
    """Safely extract JSON even if model returns extra text."""
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
    return {"command": "", "description": "Failed to parse JSON output."}

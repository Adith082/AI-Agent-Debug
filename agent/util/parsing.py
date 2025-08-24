import json, re

def extract_json(text: str):
    fences = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.S)
    if fences:
        try: return json.loads(fences[0])
        except: pass
    m = re.search(r"(\{.*\})", text, flags=re.S)
    if m:
        try: return json.loads(m.group(1))
        except: return None
    return None
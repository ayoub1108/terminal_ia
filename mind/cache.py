import os, json, hashlib
from pathlib import Path

CACHE_DIR = Path(os.getenv("MIND_CACHE_DIR", "~/.cache/mind-cli")).expanduser()
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _key_for(prompt: str, backend: str, shell: str):
    h = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    return CACHE_DIR / f"{backend}_{shell}_{h}.json"

def get(prompt: str, backend: str, shell: str):
    p = _key_for(prompt, backend, shell)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            return None
    return None

def set_cache(prompt: str, backend: str, shell: str, value):
    p = _key_for(prompt, backend, shell)
    try:
        p.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass

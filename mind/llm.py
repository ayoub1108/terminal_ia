import os
import json

def call_openai_chat(prompt_messages, model="gpt-4o-mini", temperature=0.0):
    """Simple OpenAI chat wrapper."""
    import openai
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Please export your OPENAI_API_KEY before using this tool.")
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt_messages,
        max_tokens=400,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']


def call_local_llm(prompt_text):
    """Dummy local model fallback (replace with your own later)."""
    return json.dumps({
        "command": "echo 'Local LLM not configured'",
        "description": "Local AI model is not available yet."
    }, ensure_ascii=False)


def run_model(user_prompt, backend='openai', shell='bash', model_name=None):
    """Dispatch the prompt to the correct model backend."""
    from .prompts import PROMPT_TEMPLATE, SYSTEM_INSTRUCTION

    prompt = PROMPT_TEMPLATE.format(shell=shell, user_prompt=user_prompt)

    if backend == 'openai':
        system_msg = {"role": "system", "content": SYSTEM_INSTRUCTION}
        user_msg = {"role": "user", "content": prompt}
        model = model_name or os.getenv("MIND_MODEL", "gpt-4o-mini")
        return call_openai_chat([system_msg, user_msg], model=model)
    elif backend == 'local':
        return call_local_llm(prompt)
    else:
        raise ValueError(f"Unsupported backend: {backend}")

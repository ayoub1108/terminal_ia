import subprocess
import time
from .llm import run_model
from .utils import safe_parse_json
from .cache import get as cache_get, set_cache

def generate_command(prompt_text, model_backend='openai', shell='bash', model_name=None,
                     use_cache=True, verbose=False, interactive=True):
    """Main logic: query model, parse output, show, and optionally execute."""

    if use_cache:
        cached = cache_get(prompt_text, model_backend, shell)
        if cached:
            if verbose:
                print("[cache] found cached result")
            return cached

    start = time.time()
    raw = run_model(user_prompt=prompt_text, backend=model_backend, shell=shell, model_name=model_name)
    elapsed = time.time() - start

    if verbose:
        print(f"[llm raw output after {elapsed:.2f}s]:\n{raw}\n")

    result = safe_parse_json(raw)
    result["_meta"] = {"backend": model_backend, "elapsed_s": elapsed}

    if use_cache:
        set_cache(prompt_text, model_backend, shell, result)

    if interactive:
        show_and_execute(result)

    return result


def show_and_execute(result):
    """Display command and prompt user to confirm execution."""
    command = result.get("command", "").strip()
    description = result.get("description", "").strip()

    print("\nSuggested command:")
    print(command)
    print(f"\nDescription: {description}")

    choice = input("\nExecute this command? (y/n): ").strip().lower()
    if choice == 'y':
        print("\nRunning command...\n")
        try:
            subprocess.run(command, shell=True, check=True)
            print("\n✅ Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Command failed with exit code {e.returncode}.")
    else:
        print("\n🚫 Command not executed.")

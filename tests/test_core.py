from mind.core import generate_command

def test_generate_command_local():
    result = generate_command("echo hello", model_backend="local", interactive=False, use_cache=False)
    assert "command" in result

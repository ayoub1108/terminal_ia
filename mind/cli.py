import click

from mind.core import generate_command

@click.command()
@click.option('-h', '--help-text', 'help_text', required=True,
              help='Describe what you want to do (in quotes). Example: "ping 8.8.8.8 five times".')
@click.option('-m', '--model', default='openai', help='Model backend: openai or local.')
@click.option('-s', '--shell', default='bash', help='Target shell (bash, zsh, etc.).')
@click.option('--no-interactive', is_flag=True, default=False, help='Disable interactive execution prompt.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose debug logs.')
def cli(help_text, model, shell, no_interactive, verbose):
    """mind -h "text"
    Converts natural language into Linux commands using AI.
    """
    generate_command(
        prompt_text=help_text,
        model_backend=model,
        shell=shell,
        verbose=verbose,
        interactive=not no_interactive
    )

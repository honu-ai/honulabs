import readline # <- do not remove, this lifts the 1024 char input limit on Mac
import traceback

import shutil

import urllib

import cmd
import inspect
from typing import Callable, Dict, Optional

from tabulate import tabulate

from cli.api_client import HonulabsAPIClient
from cli.utils.handle_business_generation import handle_business_generation
from cli.utils.job_manager import JobManager
from cli.utils.pick_business import pick_business
from cli.utils.token import HonulabsToken

# Storage for registered commands
_COMMANDS: Dict[str, Callable] = {}
NOT_LOGGED_IN_HEADER = " -- User is not logged in \U0001F611 --"
LOGGED_IN_HEADER = ' -- User is logged in \U0001F642 --'
TABLE_STYLE = 'double_grid'

def command(name: Optional[str] = None, help_text: str = ""):
    """Decorator to register a function as a CLI command."""
    def decorator(func: Callable) -> Callable:
        cmd_name = name or func.__name__
        _COMMANDS[cmd_name] = func
        func._help_text = help_text  # type: ignore
        return func
    return decorator

class HonulabsCommandPrompt(cmd.Cmd):
    """Interactive CLI that executes decorated functions."""

    intro = "Welcome to the Honulabs CLI. Type 'help' or '?' for help, 'exit' to quit."
    prompt = "\n🐢 > "

    def __init__(self):
        super().__init__()
        self.use_rawinput = False  # Disable readline to remove autocomplete
        # Register all commands
        for cmd_name, func in _COMMANDS.items():
            setattr(self, f"do_{cmd_name}", self._create_command_handler(cmd_name, func))

    def _check_token(self):
        honulabs_token = HonulabsToken()
        if honulabs_token.token is None:
            print(NOT_LOGGED_IN_HEADER)
        else:
            api_client = HonulabsAPIClient(honulabs_token.token)
            if api_client.check_token():
                print(LOGGED_IN_HEADER)
            else:
                print(NOT_LOGGED_IN_HEADER)

    def cmdloop(self):
        """Ultra simple command loop."""
        print("""
                         _       _         
  /\\  /\\___  _ __  _   _| | __ _| |__  ___ 
 / /_/ / _ \\| '_ \\| | | | |/ _` | '_ \\/ __|
/ __  / (_) | | | | |_| | | (_| | |_) \\__ \\
\\/ /_/ \\___/|_| |_|\\__,_|_|\\__,_|_.__/|___/
""")

        print(self.intro)
        self._check_token()
        running = True
        while running:
            try:
                line = input(self.prompt)
            except (KeyboardInterrupt, EOFError):
                line = 'exit'
            if not line:
                continue

            cmd, *args = line.split(maxsplit=1)
            args = args[0] if args else ""

            if cmd in ("exit", "quit"):
                running = False
            elif hasattr(self, f"do_{cmd}"):
                getattr(self, f"do_{cmd}")(args)
            else:
                print(f"Unknown command: {cmd}")

    def _create_command_handler(self, cmd_name: str, func: Callable) -> Callable:
        """Create a command handler for the given function."""
        def handler(arg: str) -> None:
            try:
                args = arg.split() if arg else []
                sig = inspect.signature(func)
                params = list(sig.parameters.values())

                # Simple argument count check
                min_args = sum(1 for p in params if p.default == inspect.Parameter.empty)
                if len(args) < min_args:
                    print(f"Error: Not enough arguments. Need at least {min_args}")
                    self._print_usage(cmd_name, func)
                    return

                result = func(*args)
                if result is not None:
                    print(result)
            except Exception:
                traceback.print_exc()
        return handler

    def _print_usage(self, cmd_name: str, func: Callable) -> None:
        """Print usage information for a command."""
        sig = inspect.signature(func)
        params = []
        for param in sig.parameters.values():
            if param.default == inspect.Parameter.empty:
                params.append(f"<{param.name}>")
            else:
                params.append(f"[{param.name}={param.default}]")
        print(f"Usage: {cmd_name} {' '.join(params)}")
        help_text = getattr(func, "_help_text", "")
        if help_text:
            print(help_text)

    def do_help(self, arg: str) -> None:
        """List available commands or show help for a specific command."""
        print("\nAvailable commands:")
        commands = sorted(list(_COMMANDS.keys()) + ["exit", "quit", "help"])
        for command in commands:
            if command in _COMMANDS:
                func = _COMMANDS[command]
                help_text = getattr(func, "_help_text", "")

                # Get a simplified signature for overview
                sig = inspect.signature(func)
                params = []
                for param in sig.parameters.values():
                    if pHTTP_202_ACCEPTEDaram.default == inspect.Parameter.empty:
                        params.append(f"<{param.name}>")
                    else:
                        params.append(f"[{param.name}]")

                param_str = " ".join(params)
                print(f"  {command} {param_str}")
                print(f"    {help_text}\n")
            elif command in ("exit", "quit"):
                print(f"  {command}")
                print("    Exit the CLI\n")
            elif command == "help":
                print("  help")
                print("    List commands\n")


# Commands
@command(help_text="Set token for API usage")
def login(token: str):
    # Check token
    api_client = HonulabsAPIClient(token)
    if api_client.check_token():
        print(LOGGED_IN_HEADER)
        HonulabsToken(token)
    else:
        print('Token was invalid, please try again')


@command(help_text='List your Businesses')
def list_businesses():
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    businesses = api_client.list_businesses()
    if not businesses:
        print('You have no businesses yet!')
        return

    print(tabulate(
        ({'id': biz.business_id, 'name': biz.name} for biz in businesses),
        headers='keys',
        tablefmt=TABLE_STYLE,
    ))


@command(help_text='Create new Business record')
def create_business(*name: str):
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    name = ' '.join(name)
    biz = api_client.create_business(name)
    print(f'Business record "{biz.name}" created!')


@command(help_text='Delete Business')
def delete_business():
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return

    # Set up the job to delete the business
    job = api_client.delete_business(business_id)
    print('Deletion job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
    manager = JobManager(job)
    try:
        manager.await_job_completion()
    except (KeyboardInterrupt, EOFError):
        manager.spinner.stop()
        print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')


@command(help_text='Begin generation of Business Plan')
def generate_business_plan():
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    handle_business_generation(business_id)


@command(help_text='Deploy latest landing page for Business')
def deploy_landing_page():
    ...


@command(help_text='Upload secret variables for your app')
def upload_secrets():
    ...

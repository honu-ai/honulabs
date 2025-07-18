import cmd
import inspect
import traceback
from typing import Callable, Dict, Optional

from halo import Halo
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from tabulate import tabulate

from cli.api_client import HonulabsAPIClient
from cli.auth_client import HonulabsAuthClient, spinup_single_use_server
from cli.schema import Collaborator, Collaborators, JobStatus, VercelSecrets
from cli.utils.handle_business_generation import BusinessPlanGeneration
from cli.utils.handle_idea_generation import IdeaGeneration
from cli.utils.job_manager import JobManager
from cli.utils.mcp_setup import (
    claude_desktop_mcp_connection_string,
    cursor_mcp_connection_string,
)
from cli.utils.pick_business import pick_business
from cli.utils.prompts import prompt_with_default
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
        session = PromptSession(history=InMemoryHistory())
        completer = WordCompleter(list(_COMMANDS.keys()) + ['help', 'exit', 'quit'], ignore_case=True)
        while running:
            try:
                line = session.prompt(self.prompt, completer=completer)
            except (KeyboardInterrupt, EOFError):
                line = 'exit'
            if not line:
                continue

            cmd, *args = line.split(maxsplit=1)
            args = args[0] if args else ""

            if cmd in ("exit", "quit"):
                running = False
            elif cmd == '?':
                self.do_help(args)
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
        for cmd_name in commands:
            if cmd_name in _COMMANDS:
                func = _COMMANDS[cmd_name]
                help_text = getattr(func, "_help_text", "")

                # Get a simplified signature for overview
                sig = inspect.signature(func)
                params = []
                for param in sig.parameters.values():
                    if param.default == inspect.Parameter.empty:
                        params.append(f"<{param.name}>")
                    else:
                        params.append(f"[{param.name}]")

                param_str = " ".join(params)
                print(f"  {cmd_name} {param_str}")
                print(f"    {help_text}\n")
            elif cmd_name in ("exit", "quit"):
                print(f"  {cmd_name}")
                print("    Exit the CLI\n")
            elif cmd_name == "help":
                print("  help")
                print("    List commands\n")


# Commands
@command(help_text="Set token for API usage manually")
def token_login(token: str):
    # Check token
    api_client = HonulabsAPIClient(token)
    with Halo(text='Checking Token', spinner='dots'):
        if api_client.check_token():
            print(LOGGED_IN_HEADER)
            HonulabsToken(token)
        else:
            print('Token was invalid, please try again')


@command(help_text='List your Projects')
def list_projects():
    token = HonulabsToken()
    with Halo(text='Fetching Projects', spinner='dots'):
        api_client = HonulabsAPIClient(token.token)
        businesses = api_client.list_businesses()
        if not businesses:
            print('You have no Projects yet! Please use `create_project` to make one!')
            return

    print(tabulate(
        ({'id': biz.business_id, 'name': biz.name} for biz in businesses),
        headers='keys',
        tablefmt=TABLE_STYLE,
    ))


@command(help_text='Create new Project')
def create_project(*name: str):
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    name = ' '.join(name)
    with Halo(text='Creating Project', spinner='dots'):
        biz = api_client.create_business(name)
    print(f'Project "{biz.name}" created!')


@command(help_text='Delete Project and deployed services')
def delete_project():
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    # Set up the job to delete the business
    job = api_client.delete_business(business_id)
    print('Deletion job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
    manager = JobManager(job)
    try:
        manager.await_job_completion()
    except (KeyboardInterrupt, EOFError):
        manager.spinner.stop()
        print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')


@command(help_text='Generate a Business Plan for a Project')
def generate_business_plan():
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    generator = BusinessPlanGeneration(business_id, TABLE_STYLE)
    generator.run()


@command(help_text='Deploy latest landing page for Project')
def deploy_app():
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    # Set up the job
    job = api_client.deploy_landing_page(business_id)
    print('Deployment job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
    manager = JobManager(job)

    try:
        job = manager.await_job_completion()
        result = job.result
        if result is None:
            return

        app_links = result['app_links']
        print()
        print("🚀 Your app is ready!")
        print()
        print("📱 Access your app at:")
        for i, link in enumerate(app_links, 1):
            print(f"   {i}. {link}")
        print()

    except (KeyboardInterrupt, EOFError):
        manager.spinner.stop()
        print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')


@command(help_text='Upload secret variables for your app')
def upload_secrets():
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    secrets = {}
    print('Input secret names and values. Leaving any input blank will continue to the upload portion.')
    while True:
        secret_name = input('Secret Name: ').strip()
        if secret_name == '':
            break
        secret_value = input('Secret Value: ').strip()
        if secret_value == '':
            break
        secrets[secret_name] = secret_value

    if not secrets:
        print('Not uploading any secrets!')
        return

    print()
    print(tabulate(
        ({'Name': k, 'Value': v} for k, v in secrets.items()),
        'keys',
        TABLE_STYLE,
    ))
    print()
    print('Please double check that all variables are correct.')
    proceed = prompt_with_default('Upload these variables?')
    if not proceed:
        print('Exiting')
        return

        # Set up the job
    job = api_client.deploy_secrets_to_vercel(business_id, VercelSecrets(secrets=secrets))
    print('Deployment job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
    manager = JobManager(job)
    try:
        manager.await_job_completion()
    except (KeyboardInterrupt, EOFError):
        manager.spinner.stop()
        print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')


@command(help_text='Check on the status of any Jobs that are currently in progress')
def pending_jobs():

    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    pending_jobs = api_client.get_jobs(business_id, job_status=JobStatus.IN_PROGRESS)
    if not pending_jobs:
        print('No pending jobs!')
        return

    data = {
        str(num): job
        for num, job in enumerate(pending_jobs, start=1)
    }
    print(tabulate(
        (
            {'Number': num, 'ID': job.job_id, 'Type': job.job_type, 'Started At': job.started_at.isoformat(),
             'Message': job.message or 'None!'}
            for num, job in data.items()
        ),
        'keys',
        TABLE_STYLE,
    ))
    try:
        print('If you would like to wait for one to complete, please type the number, or just press ENTER to return to the menu.')
        selected_num = input('> ').strip()
        if selected_num == '':
            return

        while selected_num not in data:
            print('That number is not a valid choice, please select a valid choice or press ENTER to cancel.')
            selected_num = input('> ').strip()
            if selected_num == '':
                return

        manager = JobManager(data[selected_num])
        manager.await_job_completion()
    except (KeyboardInterrupt, EOFError):
        return

@command(help_text="Invite user to the project GitHub repository")
def invite_to_repo():
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    invitees= []
    print('Enter usernames to invite (press Enter on empty line to finish):\n')
    while True:
        invitee = input('username: ').strip()
        if invitee == '':
            break
        invitees.append(Collaborator(username=invitee))
        print(f'✓ Added "{invitee}"\n')
        print()

    if not invitees:
        print('Not inviting anyone!')
        return

    # Confirmation
    print(f'\n📋 Ready to invite {len(invitees)} user(s):')
    for i, collab in enumerate(invitees, 1):
        print(f'   {i}. {collab.username}')

    # Set up the job
    job = api_client.invite_collaborators(business_id, Collaborators(collaborators=invitees))
    print('Job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
    manager = JobManager(job)
    try:
        result = manager.await_job_completion()
        repo_name = result.result['repo']
        print()
        print(f"✅ Invitations sent for repository: {repo_name}")
        print("📧 Please check your email for the invitation. If you don't receive it within")
        print("   a few minutes, please try again or contact us for assistance.")
        print()

    except (KeyboardInterrupt, EOFError):
        manager.spinner.stop()
        print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')

@command(help_text="Login to the Honu platform")
def login():
    """ Login to the platform using the CLI """
    auth_client = HonulabsAuthClient()
    url = auth_client.get_login_url()

    print()
    print("=" * 60)
    print()
    print("🐢 HONU CONNECTION")
    print()
    print("Cmd + click (or copy/paste) to login:")
    print(f"🔗 {url}")
    print()
    print("=" * 60)
    print()

    code = spinup_single_use_server()
    with Halo(text='Checking Token', spinner='dots'):
        auth_client.exchange_token(code)
        print(LOGGED_IN_HEADER)

@command(help_text="generate a new idea for a business")
def new_business_idea():
    token = HonulabsToken()
    HonulabsAPIClient(token.token)
    business_id = pick_business(TABLE_STYLE)
    if business_id is None:
        return
    business_id = business_id.id

    idea_generator = IdeaGeneration(business_id, TABLE_STYLE)
    new_idea = idea_generator.run()

    generator = BusinessPlanGeneration(business_id, TABLE_STYLE)
    generator.run(new_idea)


@command(help_text="Print the configuration json to connect to the Honu MCP server")
def mcp_config_string():
    business = pick_business(TABLE_STYLE)
    if business is None:
        return
    model_ref = business.model_ref

    token = HonulabsToken().token
    claude_desktop_connection_string = claude_desktop_mcp_connection_string(token, model_ref)
    cursor_connection_string = cursor_mcp_connection_string(token, model_ref)

    print("=" * 64)
    print()
    print("  HONU MCP SERVER CONFIGURATION 🔧")
    print()
    print("  Add this configuration to your desktop tools")
    print()
    print("=" * 64)
    print()
    print("📋 CLAUDE DESKTOP CONFIGURATION")
    print()
    print(claude_desktop_connection_string)
    print()
    print("=" * 64)
    print()
    print("🔍 CURSOR CONFIGURATION")
    print()
    print(cursor_connection_string)
    print()
    print("=" * 64)
    print()
    print("💡 Copy and paste the appropriate JSON above into your tool's MCP settings")
    print()
import socket
import urllib
from pathlib import Path

import httpx
from starlette import status

from cli.api_client import HonulabsAPIClient
from cli.settings import Settings
from cli.utils.token import HonulabsToken


def handle_request(client_socket):
    """Handle a single HTTP request"""
    code = None

    try:
        # Receive the request
        request = client_socket.recv(1024).decode('utf-8')
        path_query = request.split('\n')[0].split(' ')[1]
        parsed = urllib.parse.urlparse(path_query)
        query = urllib.parse.parse_qs(parsed.query)
        code = query['code'][0]

        # Send a simple HTTP response
        success_page_path = Path(__file__).parent / 'utils/templates/success_page.html'
        content = open(success_page_path).read()
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(content)}

{content}"""

        client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

    return code

def spinup_single_use_server():
    """ Spinup local server """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    code = None
    try:
        server_socket.bind((Settings.CLI_SERVER_HOST, Settings.CLI_SERVER_PORT))
        server_socket.listen(1)
        print(f"Server listening on {Settings.CLI_SERVER_HOST}:{Settings.CLI_SERVER_PORT}")
        print("Waiting for first request...")

        # Accept the first connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Handle the request
        code = handle_request(client_socket)
        print('Request handled, shutting down server')

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

    return code


class HonulabsAuthClient:

    def __init__(self, token: str | None = None):
        self.token = token

    def get_login_url(self):
        base_url = f"https://{Settings.AUTH0_DOMAIN}"
        path = "/authorize"
        params = dict(
            response_type="code",
            client_id=Settings.AUTH0_FE_APP_CLIENT_ID,
            redirect_uri=Settings.REDIRECT_URI,
            scope="openid profile email offline_access",
            audience=Settings.AUTH0_API_IDENTIFIER_AUDIENCE,
        )

        url = urllib.parse.urljoin(base_url, path)
        query_string = urllib.parse.urlencode(params, doseq=False)
        url = f"{url}?{query_string}"

        return url

    def exchange_token(self, code: str):
        """ Take the code from the first step and exchange that for the token"""

        # Now that I have the code exchange this for the token in the auth platform
        honu_auth_base_url = Settings.AUTH_URL
        get_token_path = "/v1/token/get_token"
        url = urllib.parse.urljoin(honu_auth_base_url, get_token_path)
        response = httpx.post(url, params=dict(code=code), timeout=240)
        if response.status_code != status.HTTP_200_OK:
            print(f"There was a problem getting the token from the server {response.status_code} : {response.text}")

        response = response.json()
        token = response['access_token']
        api_client = HonulabsAPIClient(token)

        if api_client.check_token():
            HonulabsToken(token)
        else:
            print('Token was invalid, please try again')
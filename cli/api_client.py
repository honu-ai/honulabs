import httpx
from starlette import status

from cli.settings import Settings


class HonulabsAPIClient:

    def __init__(self, token: str):
        self.token = token

    @property
    def client(self):
        return httpx.Client(base_url=Settings.API_URL, headers={'Authorization': f'Bearer {self.token}'}, timeout=120)

    def check_token(self) -> bool:
        response = self.client.get('/v1/organisations')
        return response.status_code == status.HTTP_200_OK

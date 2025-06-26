import httpx
from starlette import status

from cli.schema import HonulabsBusiness
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

    def list_businesses(self) -> list[HonulabsBusiness]:
        response = self.client.get('/v1/businesses')
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f'Could not retrieve businesses: {response.text}')
        return [HonulabsBusiness(**r) for r in response.json()]

    def create_business(self, name: str) -> HonulabsBusiness:
        response = self.client.post('/v1/businesses', json={'name': name})
        if response.status_code != status.HTTP_201_CREATED:
            raise Exception(f'Could not create business: {response.text}')
        return HonulabsBusiness(**response.json())

import httpx
from starlette import status

from cli.schema import HonulabsBusiness, HonulabsJob
from cli.settings import Settings


class HonulabsAPIClient:

    def __init__(self, token: str | None):
        if token is None:
            raise Exception('Please login with a valid token first')
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

    def delete_business(self, business_id: str) -> HonulabsJob:
        response = self.client.delete(f'/v1/businesses/{business_id}')
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise Exception(f'Could not delete business: {response.text}')
        return HonulabsJob(**response.json())

    def get_job(self, business_id: str, job_id: str) -> HonulabsJob:
        response = self.client.get(f'/v1/businesses/{business_id}/jobs/{job_id}')
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f'Could not read job: {response.text}')
        return HonulabsJob(**response.json())

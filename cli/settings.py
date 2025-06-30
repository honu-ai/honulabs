from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    API_URL: str = 'https://honulabs-api.honu.ai'

Settings = _Settings()

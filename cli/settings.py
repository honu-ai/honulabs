from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    API_URL: str = 'http://localhost:8092'

Settings = _Settings()

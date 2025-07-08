from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    API_URL: str = 'http://localhost:8092' #'https://honulabs-api.honu.ai'
    AUTH_URL: str = "http://localhost:8042" #'https://auth.honu.ai'

    AUTH0_DOMAIN: str = "honu-dev-1.uk.auth0.com"
    AUTH0_FE_APP_CLIENT_ID: str = "o4hMGS9xKTrQExXwssiDGvnJpEoFg6Fy"
    AUTH0_API_IDENTIFIER_AUDIENCE: str = "https://auth.honutech.dev"

    CLI_SERVER_HOST: str = "localhost"
    CLI_SERVER_PORT: int = 8181
    REDIRECT_URI: str = f"http://{CLI_SERVER_HOST}:{CLI_SERVER_PORT}"

Settings = _Settings()

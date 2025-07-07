from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    API_URL: str = 'http://localhost:8092' #'https://honulabs-api.honu.ai'
    AUTH0_FE_APP_CLIENT_ID: str = "o4hMGS9xKTrQExXwssiDGvnJpEoFg6Fy"
    REDIRECT_URI: str = "http://localhost:8181" # This is always localhost:8181, it's the local server the cli sping to listen for the code
    CLI_SERVER_HOST: str = "http://localhost"
    CLI_SERVER_PORT: int = 8181
    AUTH0_DOMAIN: str = "honu-dev-1.uk.auth0.com"
    AUTH0_API_IDENTIFIER_AUDIENCE: str = "https://auth.honutech.dev"
    HONU_AUTH_URL: str = "http://localhost:8042"


Settings = _Settings()

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    API_URL: str = 'https://honulabs-api.honu.ai'
    AUTH_URL: str = 'https://auth.honu.ai'
    HAP_URL: str = 'https://happi.honu.ai'
    MCP_SERVER_URL: str = 'https://mcp.honu.ai/mcp/'

    AUTH0_DOMAIN: str = "honu-prod-1.uk.auth0.com"
    AUTH0_FE_APP_CLIENT_ID: str = "y9lJHJQFUCxXF8ejpKulQR4EUbdShPQ8"
    AUTH0_API_IDENTIFIER_AUDIENCE: str = "https://auth.honu.ai"

    CLI_SERVER_HOST: str = "localhost"
    CLI_SERVER_PORT: int = 8181
    REDIRECT_URI: str = f"http://{CLI_SERVER_HOST}:{CLI_SERVER_PORT}"

Settings = _Settings()

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    # Local
    API_URL: str = 'http://localhost:8092' #'https://honulabs-api.honutech.dev'
    AUTH_URL: str = 'http://localhost:8042' #'https://auth.honutech.dev'
    HAP_URL: str = 'http://localhost:8080' #'https://happi.honutech.dev'
    MCP_SERVER_URL: str = 'http://localhost:8282/mcp/' #'https://mcp.honutech.dev/mcp/'

    AUTH0_DOMAIN: str = "honu-dev-1.uk.auth0.com"
    AUTH0_FE_APP_CLIENT_ID: str = "o4hMGS9xKTrQExXwssiDGvnJpEoFg6Fy"
    AUTH0_API_IDENTIFIER_AUDIENCE: str = "https://auth.honutech.dev"

    CLI_SERVER_HOST: str = "localhost"
    CLI_SERVER_PORT: int = 8181
    REDIRECT_URI: str = f"http://{CLI_SERVER_HOST}:{CLI_SERVER_PORT}"

    # # DEV
    # API_URL: str = 'https://honulabs-api.honutech.dev'
    # AUTH_URL: str = 'https://auth.honutech.dev'
    # HAP_URL: str = 'https://happi.honutech.dev'
    # MCP_SERVER_URL: str = 'https://mcp.honutech.dev/mcp/'
    #
    # AUTH0_DOMAIN: str = "honu-dev-1.uk.auth0.com"
    # AUTH0_FE_APP_CLIENT_ID: str = "o4hMGS9xKTrQExXwssiDGvnJpEoFg6Fy"
    # AUTH0_API_IDENTIFIER_AUDIENCE: str = "https://auth.honutech.dev"
    #
    # CLI_SERVER_HOST: str = "localhost"
    # CLI_SERVER_PORT: int = 8181
    # REDIRECT_URI: str = f"http://{CLI_SERVER_HOST}:{CLI_SERVER_PORT}"

    # # Prod
    # API_URL: str = 'https://honulabs-api.honu.ai'
    # AUTH_URL: str = 'https://auth.honu.ai'
    # HAP_URL: str = 'https://happi.honu.ai'
    # MCP_SERVER_URL: str = 'https://mcp.honu.ai/mcp/'
    #
    # AUTH0_DOMAIN: str = "honu-prod-1.uk.auth0.com"
    # AUTH0_FE_APP_CLIENT_ID: str = "y9lJHJQFUCxXF8ejpKulQR4EUbdShPQ8"
    # AUTH0_API_IDENTIFIER_AUDIENCE: str = "https://auth.honu.ai"
    #
    # CLI_SERVER_HOST: str = "localhost"
    # CLI_SERVER_PORT: int = 8181
    # REDIRECT_URI: str = f"http://{CLI_SERVER_HOST}:{CLI_SERVER_PORT}"

Settings = _Settings()

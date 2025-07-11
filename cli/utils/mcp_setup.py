import json

from cli.settings import Settings

def mcp_connection_string(token: str):
    mcp_server_url = Settings.MCP_SERVER_URL
    config = {
        "mcpServers": {
            "cloud-run": {
                "command": "npx",
                "args": [
                    "-y",
                    "mcp-remote",
                    mcp_server_url,
                    "--header",
                    f"Authorization: Bearer {token}"
                ]
            }
        }
    }

    return json.dumps(config)

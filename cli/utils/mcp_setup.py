import json

from cli.settings import Settings

def claude_desktop_mcp_connection_string(token: str):
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

def cursor_mcp_connection_string(token: str):
    mcp_server_url = Settings.MCP_SERVER_URL
    config = {
        "mcpServers": {
            "server-name": {
                "url": mcp_server_url,
                "headers": {
                    "Authorization": f"Bearer {token}"
                }
            }
        }
    }
    return json.dumps(config)
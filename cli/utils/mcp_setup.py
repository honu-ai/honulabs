import json

from cli.settings import Settings
MCP_SERVER_NAME = "Honu-MCP-server"

def claude_desktop_mcp_connection_string(token: str, model_ref: str):
    mcp_server_url = Settings.MCP_SERVER_URL
    config = {
        "mcpServers": {
            MCP_SERVER_NAME: {
                "command": "npx",
                "args": [
                    "-y",
                    "mcp-remote",
                    mcp_server_url,
                    "--header",
                    f"Authorization: Bearer {token}",
                    "--header",
                    f"X-HONU-MODEL: {model_ref}"
                ]
            }
        }
    }

    return json.dumps(config)

def cursor_mcp_connection_string(token: str, model_ref: str):
    mcp_server_url = Settings.MCP_SERVER_URL
    config = {
        "mcpServers": {
            MCP_SERVER_NAME: {
                "url": mcp_server_url,
                "headers": {
                    "Authorization": f"Bearer {token}",
                    "X-HONU-MODEL": model_ref
                }
            }
        }
    }
    return json.dumps(config)
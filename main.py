from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Evoliz")

@mcp.tool()
def get_clients() -> str:
    """Liste les clients Evoliz"""
    return "Connexion Evoliz OK"

@mcp.tool()
def get_invoices() -> str:
    """Liste les factures Evoliz"""
    return "Connexion Evoliz OK"

import os

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )

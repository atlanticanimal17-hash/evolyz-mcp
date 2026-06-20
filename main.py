from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Evoliz")

...

if __name__ == "__main__":
    mcp.run(transport="sse")

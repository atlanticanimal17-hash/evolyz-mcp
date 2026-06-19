from fastapi import FastAPI

app = FastAPI(
    title="Evoliz MCP",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "name": "evoliz-mcp",
        "status": "ok"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

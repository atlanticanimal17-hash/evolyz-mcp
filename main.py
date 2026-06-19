from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "name": "evoliz-mcp",
        "status": "ok",
        "protocol": "mcp"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/tools")
def tools():
    return {
        "tools": []
    }

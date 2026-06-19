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
        "tools": [
            {
                "name": "get_clients",
                "description": "Liste les clients Evoliz"
            },
            {
                "name": "get_invoices",
                "description": "Liste les factures Evoliz"
            }
        ]
    }

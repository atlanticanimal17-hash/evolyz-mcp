from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def root():
    return {
        "name": "evolyz-mcp",
        "status": "ok",
        "company_id": os.getenv("EVOLIZ_COMPANY_ID")
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/config")
def config():
    return {
        "company_id": os.getenv("EVOLIZ_COMPANY_ID"),
        "public_key_present": bool(os.getenv("EVOLIZ_PUBLIC_KEY")),
        "secret_key_present": bool(os.getenv("EVOLIZ_SECRET_KEY"))
    }


@app.get("/tools")
def tools():
    return {
        "tools": [
            "clients",
            "factures",
            "impayes",
            "chiffre_affaires",
            "recherche_client",
            "creer_facture"
        ]
    }

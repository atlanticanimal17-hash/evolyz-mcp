from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

API_KEY = os.getenv("EVOLIZ_API_KEY")
COMPANY_ID = os.getenv("EVOLIZ_COMPANY_ID")

BASE_URL = f"https://api.evoliz.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}


@app.get("/")
def root():
    return {
        "name": "evoliz-mcp",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/clients")
def clients():
    r = requests.get(
        f"{BASE_URL}/companies/{COMPANY_ID}/customers",
        headers=HEADERS
    )

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


@app.get("/factures")
def factures():
    r = requests.get(
        f"{BASE_URL}/companies/{COMPANY_ID}/invoices",
        headers=HEADERS
    )

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


@app.get("/dashboard")
def dashboard():

    factures = requests.get(
        f"{BASE_URL}/companies/{COMPANY_ID}/invoices",
        headers=HEADERS
    ).json()

    return {
        "nombre_factures": len(factures)
    }

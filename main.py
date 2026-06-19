from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

PUBLIC_KEY = os.getenv("EVOLIZ_PUBLIC_KEY")
SECRET_KEY = os.getenv("EVOLIZ_SECRET_KEY")
COMPANY_ID = os.getenv("EVOLIZ_COMPANY_ID")


def get_token():
    url = "https://www.evoliz.io/api/login"

    payload = {
        "public_key": PUBLIC_KEY,
        "secret_key": SECRET_KEY
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()["access_token"]


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/token")
def token():
    token = get_token()

    return {
        "token_ok": True,
        "token_preview": token[:20] + "..."
    }


@app.get("/factures")
def factures():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/invoices"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()
@app.get("/clients")
def clients():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/clients"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()

@app.get("/impayes")
def impayes():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/invoices"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    factures = response.json()["data"]

    impayes = []

    total_restant = 0

    for facture in factures:

        if facture["status"] != "paid":

            montant = facture["total"]["net_to_pay"]

            total_restant += montant

            impayes.append({
                "numero": facture["document_number"],
                "client": facture["client"]["name"],
                "montant": montant,
                "statut": facture["status"]
            })

    return {
        "nombre_factures_impayees": len(impayes),
        "montant_total_restant": round(total_restant, 2),
        "factures": impayes
    }

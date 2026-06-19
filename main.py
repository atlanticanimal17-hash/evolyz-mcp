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

@app.get("/chiffre_affaires")
def chiffre_affaires():

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

    total_ht = 0
    total_ttc = 0
    total_encaisse = 0
    total_restant = 0

    for facture in factures:

        total_ht += facture["total"]["vat_exclude"]
        total_ttc += facture["total"]["vat_include"]
        total_restant += facture["total"]["net_to_pay"]
        total_encaisse += facture["total"]["paid"]

    return {
        "nombre_factures": len(factures),
        "ca_ht": round(total_ht, 2),
        "ca_ttc": round(total_ttc, 2),
        "encaisse": round(total_encaisse, 2),
        "reste_a_encaisser": round(total_restant, 2)
    }

@app.get("/recherche_client/{nom}")
def recherche_client(nom: str):

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    page = 1
    resultat = []

    while True:

        url = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/clients?page={page}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        data = response.json()

        clients = data["data"]

        for client in clients:

            if nom.lower() in client["name"].lower():

                resultat.append({
                    "code": client["code"],
                    "nom": client["name"],
                    "ville": client["address"]["town"],
                    "telephone": client["phone"],
                    "mobile": client["mobile"]
                })

        if page >= data["meta"]["last_page"]:
            break

        page += 1

    return {
        "nombre_resultats": len(resultat),
        "clients": resultat
    }

@app.get("/tableau_de_bord")
def tableau_de_bord():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Factures
    url_factures = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/invoices"
    response_factures = requests.get(url_factures, headers=headers)

    if response_factures.status_code != 200:
        raise HTTPException(
            status_code=response_factures.status_code,
            detail=response_factures.text
        )

    factures = response_factures.json()["data"]

    # Clients
    url_clients = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/clients"
    response_clients = requests.get(url_clients, headers=headers)

    if response_clients.status_code != 200:
        raise HTTPException(
            status_code=response_clients.status_code,
            detail=response_clients.text
        )

    nb_clients = response_clients.json()["meta"]["total"]

    ca_ht = 0
    ca_ttc = 0
    encaisse = 0
    restant = 0
    impayes = 0

    for facture in factures:

        ca_ht += facture["total"]["vat_exclude"]
        ca_ttc += facture["total"]["vat_include"]
        encaisse += facture["total"]["paid"]

        if facture["status"] != "paid":
            impayes += 1
            restant += facture["total"]["net_to_pay"]

    return {
        "nombre_clients": nb_clients,
        "nombre_factures": len(factures),
        "nombre_factures_impayees": impayes,
        "ca_ht": round(ca_ht, 2),
        "ca_ttc": round(ca_ttc, 2),
        "encaisse": round(encaisse, 2),
        "reste_a_encaisser": round(restant, 2)
    }

@app.get("/client/{nom}")
def client(nom: str):

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    page = 1

    while True:

        url = f"https://www.evoliz.io/api/v1/companies/{COMPANY_ID}/clients?page={page}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        data = response.json()

        for client in data["data"]:

            if nom.lower() in client["name"].lower():

                return {
                    "clientid": client["clientid"],
                    "code": client["code"],
                    "nom": client["name"]
                }

        if page >= data["meta"]["last_page"]:
            break

        page += 1

    return {"erreur": "client introuvable"}

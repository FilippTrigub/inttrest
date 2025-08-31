# unified_server.py
import os
from dotenv import load_dotenv  # <-- AJOUT 1 : Importer la bibliothèque
from fastmcp import FastMCP, Client
from fastmcp.client.transports import StdioTransport

# --- NOUVELLE LIGNE ---
load_dotenv()  # <-- AJOUT 2 : Charger les variables du fichier .env

# --- 1. Configuration des clés d'API (maintenant lues depuis .env) ---
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
EXA_API_KEY = os.getenv("EXA_API_KEY")

if not APIFY_API_TOKEN or not EXA_API_KEY:
    raise ValueError(
        "N'a pas pu trouver APIFY_API_TOKEN ou EXA_API_KEY. "
        "Assurez-vous qu'elles sont définies dans votre fichier .env."
    )

# --- 2. Création du serveur principal unifié ---
main_mcp = FastMCP(name="Serveur d'Outils Unifié")

# --- 3. Configuration des clients pour chaque serveur externe ---
# Client pour le scraper Lusha d'Apify
apify_lusha_transport = StdioTransport(
    command="npx",
    args=[
        "mcp-remote",
        "https://mcp.apify.com/?actors=lexis-solutions/lu-ma-scraper",
        "--header",
        f"Authorization: Bearer {APIFY_API_TOKEN}",
    ],
)
apify_lusha_client = Client(apify_lusha_transport)

# Client pour le scraper Parsera d'Apify
apify_parsera_transport = StdioTransport(
    command="npx",
    args=[
        "mcp-remote",
        "https://mcp.apify.com/?actors=parsera-labs/parsera",
        "--header",
        f"Authorization: Bearer {APIFY_API_TOKEN}",
    ],
)
apify_parsera_client = Client(apify_parsera_transport)

# Client pour Exa
exa_transport = StdioTransport(
    command="npx",
    args=[
        "-y",
        "mcp-remote",
        f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}",
    ],
)
exa_client = Client(exa_transport)

# --- 4. Création des serveurs proxy pour chaque client ---
apify_lusha_proxy = FastMCP.as_proxy(apify_lusha_client)
apify_parsera_proxy = FastMCP.as_proxy(apify_parsera_client)
exa_proxy = FastMCP.as_proxy(exa_client)

# --- 5. Montage de chaque proxy sur le serveur principal avec un préfixe unique ---
main_mcp.mount(apify_lusha_proxy, prefix="apify_lusha")
main_mcp.mount(apify_parsera_proxy, prefix="apify_parsera")
main_mcp.mount(exa_proxy, prefix="exa")

# --- 6. Rendre le serveur principal exécutable en mode HTTP ---
if __name__ == "__main__":
    print("Démarrage du Serveur d'Outils Unifié en mode HTTP...")
    
    main_mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )
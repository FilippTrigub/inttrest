# unified_server.py
import asyncio
import os
from dotenv import load_dotenv
from fastmcp import FastMCP, Client
from fastmcp.client.transports import StreamableHttpTransport

load_dotenv()

# --- 1. Configuration des clés d'API ---
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
EXA_API_KEY = os.getenv("EXA_API_KEY")

if not APIFY_API_TOKEN or not EXA_API_KEY:
    raise ValueError(
        "N'a pas pu trouver APIFY_API_TOKEN ou EXA_API_KEY. "
        "Assurez-vous qu'elles sont définies dans votre fichier .env."
    )

# --- NOUVEAU : Configuration de l'URL du serveur MCP MongoDB local ---
# C'est l'URL par défaut sur laquelle le serveur mongodb-mcp-server écoute en mode HTTP.
MONGO_MCP_SERVER_URL = "http://127.0.0.1:3000"


async def main():
    # --- 2. Création du serveur principal unifié ---
    main_mcp = FastMCP(name="Serveur d'Outils Unifié")

    # --- 3. Configuration des clients avec une connexion HTTP DIRECTE ---
    # Client pour le scraper Lusha d'Apify
    apify_lusha_client = Client(
        transport=StreamableHttpTransport(
            url="https://mcp.apify.com/?actors=lexis-solutions/lu-ma-scraper",
            headers={"Authorization": f"Bearer {APIFY_API_TOKEN}"},
        )
    )

    # Client pour le scraper Parsera d'Apify
    apify_parsera_client = Client(
        transport=StreamableHttpTransport(
            url="https://mcp.apify.com/?actors=parsera-labs/parsera",
            headers={"Authorization": f"Bearer {APIFY_API_TOKEN}"},
        )
    )

    # Client pour Exa
    exa_client = Client(
        transport=StreamableHttpTransport(
            url=f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}"
        )
    )

    # --- NOUVEAU : Client pour le serveur MCP MongoDB ---
    # Ce client se connecte à votre serveur local lancé à l'étape 1.
    # Aucune authentification n'est nécessaire car il s'agit d'une connexion locale.
    mongodb_client = Client(
        transport=StreamableHttpTransport(
            url=MONGO_MCP_SERVER_URL
        )
    )


    # --- 4. Création des serveurs proxy pour chaque client ---
    apify_lusha_proxy = FastMCP.as_proxy(apify_lusha_client)
    apify_parsera_proxy = FastMCP.as_proxy(apify_parsera_client)
    exa_proxy = FastMCP.as_proxy(exa_client)
    # --- NOUVEAU : Proxy pour MongoDB ---
    mongodb_proxy = FastMCP.as_proxy(mongodb_client)


    # --- 5. IMPORTATION (await) de chaque proxy sur le serveur principal ---
    # On utilise import_server qui est asynchrone et fait une copie statique des outils.
    # C'est plus simple et plus fiable que mount pour ce cas d'usage.
    print("Importation des outils depuis les serveurs distants...")
    await main_mcp.import_server(apify_lusha_proxy, prefix="apify_lusha")
    await main_mcp.import_server(apify_parsera_proxy, prefix="apify_parsera")
    await main_mcp.import_server(exa_proxy, prefix="exa")
    # --- NOUVEAU : Importation des outils MongoDB ---
    # Le préfixe "mongo" permet d'éviter les conflits de noms (ex: mongo.find, mongo.list-collections)
    await main_mcp.import_server(mongodb_proxy, prefix="mongo")
    print("Tous les outils ont été importés avec succès !")

    # --- 6. Rendre le serveur principal exécutable en mode HTTP (de manière asynchrone) ---
    print("Démarrage du Serveur d'Outils Unifié en mode HTTP sur http://0.0.0.0:8000 ...")
    
    # On utilise run_async car nous sommes dans une fonction asynchrone
    await main_mcp.run_async(
        transport="http",
        host="0.0.0.0",
        port=8000
    )

if __name__ == "__main__":
    asyncio.run(main())
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BRIX_API_KEY", "")
API_URL = os.getenv("BRIX_API_URL", "https://api.brixhub.is/api/v1/search")
USER_AGENT = "BlackBerry-OSINT/2.0"

MAX_RESULTS = 10
TIMEOUT = 10
AUTO_SAVE = True
DATA_DIR = "data"

if not API_KEY:
    raise ValueError("❌ Clé API manquante. Copiez .env.example en .env et renseignez BRIX_API_KEY.")

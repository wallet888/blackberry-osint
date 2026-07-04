import cloudscraper
from config import API_KEY, API_URL, TIMEOUT, MAX_RESULTS

scraper = cloudscraper.create_scraper()

def search_person(nom_famille=None, prenom=None, pseudo=None, email=None):
    if not any([nom_famille, prenom, pseudo, email]):
        return []

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "BlackBerry-OSINT/2.0"
    }
    payload = {}
    if nom_famille: payload["nom_famille"] = nom_famille.strip()
    if prenom: payload["prenom"] = prenom.strip()
    if pseudo: payload["pseudo"] = pseudo.strip()
    if email: payload["email"] = email.strip().lower()

    try:
        response = scraper.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
        if response.status_code != 200:
            return []
        data = response.json()
        results = []
        if "data" in data:
            items = data["data"]
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and "results" in item:
                        if isinstance(item["results"], list):
                            results.extend(item["results"])
                        else:
                            results.append(item)
                    else:
                        results.append(item)
            elif isinstance(items, dict):
                if "results" in items and isinstance(items["results"], list):
                    results.extend(items["results"])
                else:
                    results.append(items)
        return results[:MAX_RESULTS]
    except Exception:
        return []

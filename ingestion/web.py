import requests

def fetch_web_data(url: str, limit: int = 2000):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text[:limit]

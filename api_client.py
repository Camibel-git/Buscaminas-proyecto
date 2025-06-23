import requests

BASE_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main"

def obtener_configuracion():
    """
    GET /config.json → (board_size, quantity_of_mines)
    Devuelve valores por defecto si no status 200.
    """
    url = f"{BASE_URL}/config.json"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json().get("global", {})
        return (
            data.get("board_size", [8, 8]),
            data.get("quantity_of_mines", {"easy":0.1, "medium":0.3, "hard":0.6})
        )
    return [8, 8], {"easy":0.1, "medium":0.3, "hard":0.6}

def obtener_leaderboard():
    """
    GET /leaderboard.json → lista de {first_name, last_name, time}
    Devuelve [] si no status 200.
    """
    url = f"{BASE_URL}/leaderboard.json"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return []

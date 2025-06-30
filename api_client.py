import requests
import json
import os

BASE_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main"
CONFIG_FILE = "config.txt"
LEADERBOARD_FILE = "leaderboard.txt"


def guardar_en_archivo(data, filename):
    """ guarda datos en un archivo TXT."""
    with open(filename, 'w') as f:
        json.dump(data, f)


def cargar_desde_archivo(filename):
    """ carga datos desde un archivo TXT. Si no existe, devuelve None."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


def obtener_configuracion():
    # verificar si el archivo local existe y es valido
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                if "board_size" in data and "quantity_of_mines" in data:
                    return data["board_size"], data["quantity_of_mines"]
        except:
            pass  # si hay error, se consulta la API

    # consultar API solo si no hay archivo local
    try:
        response = requests.get(f"{BASE_URL}/config.json")
        data = response.json().get("global", {})
        guardar_en_archivo(data, CONFIG_FILE)
        return data["board_size"], data["quantity_of_mines"]
    except:
        # Valores por defecto
        return (8, {"facil": 0.1, "medio": 0.2, "dificil": 0.3})


def obtener_leaderboard():
    """ obtiene leaderboard desde API o archivo local."""
    local_data = cargar_desde_archivo(LEADERBOARD_FILE)
    if local_data:
        return local_data

    url = f"{BASE_URL}/leaderboard.json"
    resp = requests.get(url)
    if resp.status_code == 200:
        guardar_en_archivo(resp.json(), LEADERBOARD_FILE)
        return resp.json()
    return []


def actualizar_record_local(nuevo_record):
    """Actualiza el leaderboard manteniendo los mejores records únicos"""
    try:
        # Validar campos requeridos
        required_fields = ["first_name", "last_name", "time", "board_size"]
        if not all(k in nuevo_record for k in required_fields):
            raise ValueError("Formato de record inválido")

        # Cargar records existentes
        records = cargar_desde_archivo(LEADERBOARD_FILE) or []

        # Verificar si el record ya existe (mismo nombre y apellido)
        existing_index = next((i for i, r in enumerate(records)
                               if r["first_name"] == nuevo_record["first_name"] and
                               r["last_name"] == nuevo_record["last_name"]), None)

        if existing_index is not None:
            # Si existe, actualizar solo si el nuevo tiempo es mejor
            if nuevo_record["time"] < records[existing_index]["time"]:
                records[existing_index] = nuevo_record
        else:
            # Si no existe, agregarlo
            records.append(nuevo_record)

        # Ordenar por tiempo y mantener solo los 3 mejores
        records.sort(key=lambda x: x["time"])
        records = records[:3]

        # Guardar en archivo
        guardar_en_archivo(records, LEADERBOARD_FILE)
        return True

    except Exception as e:
        print(f"Error al guardar record: {e}")
        return False

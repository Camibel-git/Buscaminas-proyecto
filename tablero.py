from libre import Libre
from mina import Mina

class Tablero:
    def __init__(self, num_minas):
        self.casillas = {}          # { "fila,col": Casilla }
        self.num_minas = num_minas
        self.estado_juego = 'INICIAL'

    def iniciar_tablero(self):
        # Crear casillas, colocar minas al azar, calcular adyacentes
        pass

    def revelar_casilla(self, ubicacion):
        # Revela y devuelve True/False
        pass

    def marcar_casilla(self, ubicacion):
        # Alterna bandera
        pass

    def mostrar(self):
        # Imprime el tablero fila por fila
        pass

    def _verificar_ganado(self):
        # Comprueba si todas las libres están reveladas
        pass
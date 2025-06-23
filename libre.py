from casilla import Casilla

class Libre(Casilla):
    def __init__(self, ubicacion, minas_adyacentes=0):
        super().__init__(ubicacion)
        self.minas_adyacentes = minas_adyacentes

    def ejecutar_accion(self):
        # No explota, sigue el juego
        pass
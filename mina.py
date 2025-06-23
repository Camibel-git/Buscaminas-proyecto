from casilla import Casilla

class Mina(Casilla):
    def __init__(self, ubicacion, mina_activa=True):
        super().__init__(ubicacion)
        self.mina_activa = mina_activa

    def ejecutar_accion(self):
        # Al revelar, desactiva la mina, marca como revelada y termina el juego
        self.mina_activa = False
        self.revelada = True
        return False

    def explotar(self):
        # Igual que ejecutar_accion
        self.mina_activa = False
        return False

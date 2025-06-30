from casilla import Casilla  # Importamos la clase base Casilla


class Mina(Casilla):
    """clase que representa una casilla que contiene una mina en el juego Buscaminas.
    Hereda de la clase abstracta Casilla.

    Atributos heredados:
        ubicacion: coordenadas de la casilla en formato 'fila,columna'
        revelada: indica si la casilla ha sido descubierta
        marca: puede ser None, "bandera" o "duda"""

    def _mostrar_revelada(self):
        """se implementa el metodo abstracto, devuelve la mina con emoji de bomba al seleccionarla"""
        return "[💣]"  # Emoji de bomba para minas descubiertas

    def ejecutar_accion(self):
        """Define qué ocurre cuando el jugador interactúa con la mina."""
        self.revelada = True  # Marca la casilla como revelada
        # Retorno False indica que la mina explotó (pérdida del juego)
        return False

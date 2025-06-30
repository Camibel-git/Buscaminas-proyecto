from casilla import Casilla  # Importa la clase base abstracta Casilla


class Libre(Casilla):
    """clase que representa una casilla segura (sin mina) en el tablero.
    hereda de la clase abstracta Casilla e implementa sus metodos abstractos."""

    def __init__(self, ubicacion, minas_adyacentes=0):
        """inicializa una casilla segura.

            ubicacion : coordenadas en formato 'fila,columna'
            minas_adyacentes: numero de minas vecinas. Default 0."""
        super().__init__(ubicacion)  # Llama al constructor de la clase base
        # Número de minas adyacentes (0-8)
        self.minas_adyacentes = minas_adyacentes

    def _mostrar_revelada(self):
        """
        implementacion concreta del metodo abstracto.
        devuelve la representacion visual cuando la casilla esta revelada.

        """
        if self.minas_adyacentes > 0:
            # muestra el numero de minas cercanas
            return f"[{self.minas_adyacentes}]"
        return "[ ]"  # casilla vacia

    def ejecutar_accion(self):
        """
        implementacion concreta del metodo abstracto.
        define el comportamiento al revelar esta casilla.
        """
        self.revelada = True  # marca la casilla como descubierta
        return True  # true indica que el juego debe continuar

from libre import Libre
from mina import Mina
import random


class Tablero:
    """clase principal que maneja la logica del tablero de Buscaminas"""

    def __init__(self, num_minas, size):
        """inicializa el tablero con:
        - num_minas: cantidad total de minas
        - size: tamaño del tablero (size x size)"""
        self.casillas = {}  # {coordenadas: objeto_casilla}
        self.size = size
        self.num_minas = num_minas
        self.estado_juego = 'INICIAL'  # Puede ser: INICIAL/JUGANDO/GANADO/PERDIDO

    def iniciar_tablero(self):
        """configura el tablero colocando minas aleatorias y casillas seguras"""
        # Coloca minas en posiciones aleatorias
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:
            fila = random.randint(0, self.size-1)
            col = random.randint(0, self.size-1)
            ubicacion = f"{fila},{col}"

            if ubicacion not in self.casillas:
                self.casillas[ubicacion] = Mina(ubicacion)
                minas_colocadas += 1

        # completa con casillas seguras
        for fila in range(self.size):
            for col in range(self.size):
                ubicacion = f"{fila},{col}"
                if ubicacion not in self.casillas:
                    # calcula minas adyacentes para cada casilla segura
                    adyacentes = self._calcular_minas_adyacentes(fila, col)
                    self.casillas[ubicacion] = Libre(ubicacion, adyacentes)

    def _calcular_minas_adyacentes(self, fila, col):
        """cuenta cuantas minas hay alrededor de una casilla"""
        contador = 0
        # revisa las 8 casillas circundantes
        for i in [fila-1, fila, fila+1]:
            for j in [col-1, col, col+1]:
                # verifica que este dentro del tablero
                if 0 <= i < self.size and 0 <= j < self.size:
                    ubicacion = f"{i},{j}"
                    if ubicacion in self.casillas and isinstance(self.casillas[ubicacion], Mina):
                        contador += 1
        return contador

    def revelar_casilla(self, ubicacion):
        """intenta revelar una casilla:
        - retorna True si es segura
        - retorna False si es mina (game over)"""
        if ubicacion not in self.casillas or self.casillas[ubicacion].revelada:
            return True  # asilla inválida o ya revelada

        casilla = self.casillas[ubicacion]
        casilla.revelada = True  # marca como revelada

        if isinstance(casilla, Mina):
            return False  # pierde el juego

        # si es casilla segura vacia (0 minas alrededor)
        if casilla.minas_adyacentes == 0:
            # revela automaticamente vecinas
            self._revelar_adyacentes(ubicacion)

        # verifica si gano
        if self._verificar_ganado():
            self.estado_juego = 'GANADO'

        return True  # continua el juego

    def _revelar_adyacentes(self, ubicacion):
        """revela recursivamente las casillas vecinas cuando se encuentra un area vacia"""
        fila, col = map(int, ubicacion.split(','))

        # revisa todas las casillas adyacentes
        for i in [fila-1, fila, fila+1]:
            for j in [col-1, col, col+1]:
                # verifica limites del tablero
                if 0 <= i < self.size and 0 <= j < self.size:
                    u = f"{i},{j}"
                    if u in self.casillas and not self.casillas[u].revelada:
                        self.casillas[u].revelada = True
                        # si es otra casilla vacia, sigue revelando
                        if isinstance(self.casillas[u], Libre) and self.casillas[u].minas_adyacentes == 0:
                            self._revelar_adyacentes(u)

    def mostrar(self):
        """muestra el tablero actual con formato"""
        # encabezado con numeros de columna
        print("   " + " ".join(f"{c:2}" for c in range(self.size)))

        # filas con numero de fila y estado de cada casilla
        for fila in range(self.size):
            print(f"{fila:2} ", end="")
            for col in range(self.size):
                ubicacion = f"{fila},{col}"
                print(self.casillas[ubicacion].mostrar(), end="")
            print()  # Salto de línea

    def _verificar_ganado(self):
        """verifica si el jugador gano (todas las casillas seguras reveladas)"""
        for casilla in self.casillas.values():
            if isinstance(casilla, Libre) and not casilla.revelada:
                return False
        return True

    def marcar_bandera(self, ubicacion):
        """marca una casilla con bandera (posible mina)"""
        if ubicacion in self.casillas:
            self.casillas[ubicacion].marcar_bandera()

    def marcar_duda(self, ubicacion):
        """marca una casilla con signo de duda"""
        if ubicacion in self.casillas:
            self.casillas[ubicacion].marcar_duda()

    def mostrar_minas(self):
        """revela todas las minas (cuando el jugador pierde)"""
        for casilla in self.casillas.values():
            if isinstance(casilla, Mina):
                casilla.revelada = True
        self.mostrar()

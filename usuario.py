class Usuario:
    """clase que representa un jugador del Buscaminas."""

    def __init__(self, nombre, apellido, record=0):
        """
        Inicializa un jugador con sus datos basicos.
        """
        self.nombre = nombre      # nombre del jugador
        self.apellido = apellido  # apellido del jugador
        self.record = record      # mejor tiempo (segundos)

    def mostrar_datos(self):
        """muestra en consola los datos del jugador."""
        print(
            f"Jugador: {self.nombre} {self.apellido} — Récord: {self.record}")

    def realizar_movimiento(self, tablero, ubicacion, accion):
        """
        ejecuta una accion del jugador sobre el tablero.

            tablero: Instancia del tablero de juego
            ubicacion: Coordenadas 'fila,columna'
            accion: 'revelar' o 'marcar'
        """
        if accion == 'revelar':
            # revela casilla (puede perder)
            return tablero.revelar_casilla(ubicacion)
        elif accion == 'marcar':
            tablero.marcar_casilla(ubicacion)  # coloca/remueve marca
            return True  # el juego siempre continúa
        else:
            print("Error: Acción debe ser 'revelar' o 'marcar'")
            return True  # juego continua ante accion invalida

    def actualizar_record(self, nuevo_tiempo):
        """Actualiza el récord personal si el nuevo tiempo es mejor"""
        if self.record == 0 or nuevo_tiempo < self.record:
            self.record = nuevo_tiempo
            return True  # Indica que hubo un nuevo récord
        return False

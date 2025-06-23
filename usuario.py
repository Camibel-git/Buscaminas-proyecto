class Usuario:
    def __init__(self, nombre, apellido, record=0):
        self.nombre = nombre
        self.apellido = apellido
        self.record = record

    def mostrar_datos(self):
        print(f"Jugador: {self.nombre} {self.apellido} — Récord: {self.record}")

    def realizar_movimiento(self, tablero, ubicacion, accion):
        if accion == 'revelar':
            return tablero.revelar_casilla(ubicacion)
        elif accion == 'marcar':
            tablero.marcar_casilla(ubicacion)
            return True
        else:
            print("Acción no válida. Usa 'revelar' o 'marcar'.")
            return True
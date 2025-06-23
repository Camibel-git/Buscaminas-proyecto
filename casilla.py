class Casilla:
    def __init__(self, ubicacion):
        self.ubicacion = ubicacion
        self.marcada = False
        self.revelada = False

    def mostrar(self):
        # Mostrar por consola: [   ], [ 🚩 ] o [ X ] / número
        pass

    def revelar_casilla(self):
        # Revela la casilla y ejecuta acción
        pass

    def marcar(self):
        # Alterna bandera
        pass

    def ejecutar_accion(self):
        # Debe implementarse en Libre y Mina
        pass

    def explotar(self):
        # Debe implementarse en Mina
        pass
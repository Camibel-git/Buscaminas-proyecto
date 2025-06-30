from abc import ABC, abstractmethod


class Casilla(ABC):  # hereda de ABC para ser abstracta
    def __init__(self, ubicacion, revelada=False):
        self.ubicacion = ubicacion
        self.revelada = revelada
        self.marca = None  # None, "bandera", "duda"

    def marcar_bandera(self):
        """marca/desmarca exclusivamente con bandera."""
        if not self.revelada:
            if self.marca == "bandera":
                self.marca = None  # desmarca si ya tenia bandera
            else:
                self.marca = "bandera"  # marca con bandera

    def marcar_duda(self):
        """marca/desmarca exclusivamente con duda."""
        if not self.revelada:
            if self.marca == "duda":
                self.marca = None  # desmarca si ya tenia duda
            else:
                self.marca = "duda"  # marca con duda

    def mostrar(self):
        """devuelve la representacion visual de la casilla."""
        if self.revelada:
            return self._mostrar_revelada()
        return self._mostrar_oculta()

    def _mostrar_oculta(self):
        """representacion cuando la casilla esta oculta."""
        if self.marca == "bandera":
            return "[🚩]"
        elif self.marca == "duda":
            return "[?] "
        return "[#] "

    @abstractmethod  # decorador para marcar el método como abstracto
    def _mostrar_revelada(self):
        """metodo abstracto que debe implementarse en subclases."""
        pass

    @abstractmethod  # otro metodo abstracto
    def ejecutar_accion(self):
        """ejemplo de otro metodo abstracto."""
        pass

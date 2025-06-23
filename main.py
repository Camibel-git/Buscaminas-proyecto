from api_client import obtener_configuracion, obtener_leaderboard
from tablero     import Tablero
from usuario     import Usuario

def imprimir_bienvenida():
    print("=== Bienvenido a Buscaminas ===")
    print("- Revela casillas sin explotar minas.")
    print("- Marca con bandera las casillas sospechosas.")

def menu_principal():
    print("\n--- Menú Principal ---")
    print("1) Iniciar nueva partida")
    print("2) Ver récord")
    print("3) Ver leaderboard")
    print("4) Salir")
    return input("Elige una opción: ").strip()

def configurar_partida():
    board_size, qty_mines = obtener_configuracion()
    side = board_size[0]
    print("\nNiveles disponibles:")
    for nivel, propor in qty_mines.items():
        print(f"- {nivel}: {int(side*side*propor)} minas")
    nivel = input("Elige nivel (easy/medium/hard): ").strip()
    num = int(side*side*qty_mines.get(nivel, 0.1))
    return side, num

def mostrar_leaderboard():
    tabla = obtener_leaderboard()
    print("\n-- Leaderboard --")
    for e in tabla:
        m = int(e["time"])
        s = int((e["time"]-m)*60)
        print(f"{e['first_name']} {e['last_name']} — {m}m {s}s")
    print("----------------\n")

def main():
    imprimir_bienvenida()
    jugador = Usuario(input("Nombre: "), input("Apellido: "))
    while True:
        op = menu_principal()
        if op == '1':
            size, minas = configurar_partida()
            tablero = Tablero(minas)
            tablero.iniciar_tablero()
            while tablero.estado_juego == 'JUGANDO':
                tablero.mostrar()
                accion = input("Acción ('revelar'/'marcar'): ")
                coord  = input("Coordenada (fila,col): ")
                sigue = jugador.realizar_movimiento(tablero, coord, accion)
                if not sigue:
                    print("¡Boom! Perdiste.")
                    tablero.estado_juego = 'PERDIDO'
                elif tablero._verificar_ganado():
                    print("¡Felicidades! Ganaste.")
                    jugador.record += 1
                    tablero.estado_juego = 'GANADO'
        elif op == '2':
            jugador.mostrar_datos()
        elif op == '3':
            mostrar_leaderboard()
        elif op == '4':
            print("Gracias por jugar. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    main()
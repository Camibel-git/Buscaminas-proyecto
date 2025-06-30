from api_client import obtener_configuracion, obtener_leaderboard, actualizar_record_local
from tablero import Tablero
from usuario import Usuario
import time  # Importamos time para el cronómetro


def imprimir_bienvenida():
    """muestra la bienvenida e instrucciones al juego"""
    print("======= BIENVENIDO A BUSCAMINAS ======")
    print(" Un juego de estrategia donde debes evitar las minas")
    print("\n=== INSTRUCCIONES DEL BUSCAMINAS ===")
    print("1. Objetivo: Revelar todas las casillas sin minas")
    print("2. Símbolos:")
    print("   - [#] : Casilla oculta")
    print("   - [ ] : Casilla vacía")
    print("   - [1-8] : Número de minas adyacentes")
    print("   - [🚩] : Bandera (marca una posible mina)")
    print("   - [?] : Duda (casilla sospechosa)")
    print("   - [💣] : Mina (se muestra al perder)")
    print("3. Acciones:")
    print("   - Revelar: Descubre lo que hay en la casilla")
    print("   - Bandera: Marca donde crees que hay una mina")
    print("   - Duda: Marca una casilla para revisar después")
    print("               ¡¡¡importante!!!                  ")
    print("¿ya tienes marcada una casilla con [🚩] : o [?]  y ahora quieres revelarla?")
    print("solo tienes que seleccionar nuevamente la opcion marcar (bandera o duda) y la coordenada de la casilla")
    print("así podrás desmarcar la casilla y ahora si revelarla")
    print("4. Cuando revelas una casilla vacía (0 minas),")
    print("   se revelan automáticamente sus vecinas")
    print("5. ¡Cuidado! Si revelas una mina, pierdes.")
    print("="*40 + "\n")


def menu_principal():
    """muestra el menú principal"""
    print("\n--- Menú Principal ---")
    print("1) Iniciar nueva partida")
    print("2) Ver récord")
    print("3) Ver leaderboard")
    print("4) Salir")
    return input("Elige una opción: ").strip()


def configurar_partida():
    """Configura la partida según la dificultad seleccionada:
    - Lee configuración desde API/archivo
    - Permite elegir nivel de dificultad
    - Retorna: (tamaño_tablero, cantidad_minas)"""

    board_size, qty_mines = obtener_configuracion()
    side = board_size[0]

    niveles = {
        '1': ('Fácil', 'easy'),
        '2': ('Medio', 'medium'),
        '3': ('Difícil', 'hard'),
        '4': ('Imposible', 'impossible')
    }

    print("\nNiveles disponibles:")
    for num, (nombre, key) in niveles.items():
        minas = int(side * side * qty_mines.get(key, 0.1))
        print(f"{num}) {nombre}: {minas} minas")

    while True:
        opcion = input("Elige un número de nivel (1-4): ").strip().lower()

        if opcion in niveles:
            nivel_key = niveles[opcion][1]
            break
        elif opcion in {'facil', 'easy'}:
            nivel_key = 'easy'
            break
        elif opcion in {'medio', 'medium'}:
            nivel_key = 'medium'
            break
        elif opcion in {'dificil', 'hard'}:
            nivel_key = 'hard'
            break
        elif opcion in {'imposible', 'impossible'}:
            nivel_key = 'impossible'
            break
        else:
            print("Opción no válida. Intenta nuevamente.")

    num_minas = int(side * side * qty_mines.get(nivel_key, 0.1))
    return side, num_minas


def mostrar_leaderboard():
    """Muestra el top 3 de mejores tiempos desde el archivo/API"""
    tabla = obtener_leaderboard()
    print("\n-- Leaderboard --")
    for e in tabla:
        m = int(e["time"])
        s = int((e["time"]-m)*60)
        print(f"{e['first_name']} {e['last_name']} — {m}m {s}s")
    print("----------------\n")


def main():
    """Función principal que maneja el flujo completo del juego"""

    # Configuración inicial
    imprimir_bienvenida()  # Muestra instrucciones
    jugador = Usuario(input("Nombre: "), input("Apellido: "))  # Crea usuario

    while True:  # Bucle principal del programa
        opcion = menu_principal()  # Muestra menú y obtiene selección

        if opcion == '1':  # Nueva partida
            size, minas = configurar_partida()  # Obtiene configuración
            tablero = Tablero(minas, size)  # Crea tablero
            tablero.iniciar_tablero()  # Coloca minas y casillas
            tablero.estado_juego = 'JUGANDO'
            inicio = time.time()  # Inicia cronómetro

            while tablero.estado_juego == 'JUGANDO':  # Bucle de partida
                # Mostrar estado actual
                print("\n" + "=" * 20)
                tablero.mostrar()

                # Obtener acción del jugador
                print("\nAcciones disponibles:")
                print("1) Revelar casilla")
                print("2) Marcar con bandera (🚩)")
                print("3) Marcar con duda (?)")
                accion = input("Elige una acción (1-3): ").strip()

                # Procesar coordenadas
                coord = input("Coordenada (fila,col): ").strip()
                try:
                    fila, col = map(int, coord.split(','))
                    if not (0 <= fila < size and 0 <= col < size):
                        print("Coordenadas fuera de rango.")
                        continue
                except ValueError:
                    print("Formato incorrecto. Usa fila,col (ej: 2,3).")
                    continue

                ubicacion = f"{fila},{col}"

                # Validar casilla no revelada y sin bandera
                casilla = tablero.casillas[ubicacion]
                if casilla.revelada:
                    print("¡Casilla ya revelada!")
                    continue
                if accion == '1' and casilla.marca == "bandera":
                    print("¡Primero quita la bandera!")
                    continue

                # Ejecutar acción seleccionada
                if accion == '1':  # Revelar
                    if not tablero.revelar_casilla(ubicacion):  # Si es mina
                        print("¡Boom! Perdiste.")
                        tablero.estado_juego = 'PERDIDO'
                        tablero.mostrar_minas()  # Mostrar todas las minas
                    elif tablero._verificar_ganado():  # Si ganó
                        tablero.estado_juego = 'GANADO'
                        tiempo = round(time.time() - inicio, 2)
                        print(f"\n¡FELICIDADES {jugador.nombre}! ¡HAS GANADO!")
                        print(f"Tiempo: {tiempo} segundos")

                        # Actualizar récord personal
                        if jugador.actualizar_record(tiempo):
                            print("¡Nuevo récord personal!")

                        # Guardar en leaderboard global
                        nuevo_record = {
                            "first_name": jugador.nombre.strip(),
                            "last_name": jugador.apellido.strip(),
                            "time": tiempo,
                            "board_size": size
                        }
                        if actualizar_record_local(nuevo_record):
                            print("¡Nuevo récord en el leaderboard!")

                elif accion == '2':  # Bandera
                    tablero.marcar_bandera(ubicacion)
                elif accion == '3':  # Duda
                    tablero.marcar_duda(ubicacion)
                else:
                    print("Acción no válida.")

        elif opcion == '2':  # Ver récord personal
            jugador.mostrar_datos()
            if jugador.record > 0:
                minutos = int(jugador.record // 60)
                segundos = int(jugador.record % 60)
                print(f"Mejor tiempo: {minutos}m {segundos}s")

        elif opcion == '3':  # Ver leaderboard
            mostrar_leaderboard()

        elif opcion == '4':  # Salir
            print("Gracias por jugar. ¡Hasta luego!")
            break

        else:  # Opción inválida
            print("Opción no válida.")


main()

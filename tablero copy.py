'''def mostrar_tablero_unicode(tablero):
    # Imprimir la primera línea del borde superior
    print("┌───┬───┬───┐")
    
    for i in range(3):
        # Imprimir cada fila con sus contenidos
        print(f"│ {tablero[i][0]} │ {tablero[i][1]} │ {tablero[i][2]} │")
        
        # Imprimir las líneas de separación entre filas
        if i < 2:
            print("├───┼───┼───┤")
    
    # Imprimir la última línea del borde inferior
    print("└───┴───┴───┘")

# Crear un tablero vacío de 3x3 con puntos (.) como marcadores
tablero = [['.' for _ in range(3)] for _ in range(3)]

# Llamar a la función para mostrar el tablero
mostrar_tablero_unicode(tablero)'''

from utils import limpiar_terminal

# Constantes de Unicode para personajes
ESBIRRO = u"\U0001F385"   # 🎅
REGALO = u"\U0001F381"    # 🎁
RUDOLPH = u"\U0001F98C"   # 🦌
INCONSCIENTE = u"\U0001F480" # 💀

# Clase Tablero
class Tablero:
    def __init__(self, turnos: int):
        self.turnos = turnos
        self.ronda_actual = 1
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]  # Cambié los puntos '.' por espacios
        self.esbirros = []  # Posiciones de los esbirros en el borde exterior (no en esquinas)
        self.reno = None    # Posición de Rudolph
        self.regalo = None  # Posición del regalo

    def mostrar(self, ocultar_renos: bool = False) -> None:
        """Muestra el tablero de 3x3 centrado, con esbirros fuera del tablero."""
        # Espacios para las posiciones de los esbirros fuera del tablero
        esbirros_posiciones = [[' ' for _ in range(5)] for _ in range(5)]
        
        # Colocar esbirros en las posiciones de borde
        posiciones_validas_bordes = [
            (0, 1), (0, 2), (0, 3),   # Fila superior
            (1, 0), (2, 0), (3, 0),   # Columna izquierda
            (1, 4), (2, 4), (3, 4),   # Columna derecha
            (4, 1), (4, 2), (4, 3)    # Fila inferior
        ]
        
        for (i, j) in self.esbirros:
            if (i, j) in posiciones_validas_bordes:
                esbirros_posiciones[i][j] = ESBIRRO  # Colocar esbirros en los bordes

        # Dibujar el tablero sin las líneas del borde del tablero expandido
        print(f"   {esbirros_posiciones[0][1]}   {esbirros_posiciones[0][2]}   {esbirros_posiciones[0][3]}")
        print("┌───┬───┬───┐")
        for i in range(3):
            row = f"{esbirros_posiciones[i + 1][0]} │ "
            for j in range(3):
                if (i, j) == self.reno and not ocultar_renos:
                    row += f"{RUDOLPH} │ "
                elif (i, j) == self.regalo:
                    row += f"{REGALO} │ "
                else:
                    row += "  │ "  # Espacios vacíos en lugar de puntos
            row += f"{esbirros_posiciones[i + 1][4]}"
            print(row)
            if i < 2:
                print("├───┼───┼───┤")
        print("└───┴───┴───┘")
        print(f"   {esbirros_posiciones[4][1]}   {esbirros_posiciones[4][2]}   {esbirros_posiciones[4][3]}")

    def posicionar_esbirros(self) -> None:
        """Posiciona los esbirros en las casillas alrededor del tablero a partir de la entrada del usuario."""
        posiciones_validas_bordes = [
            (0, 1), (0, 2), (0, 3),   # Fila superior
            (1, 0), (2, 0), (3, 0),   # Columna izquierda
            (1, 4), (2, 4), (3, 4),   # Columna derecha
            (4, 1), (4, 2), (4, 3)    # Fila inferior
        ]

        print(f"Las posiciones válidas para los esbirros son: {posiciones_validas_bordes}")
        
        for i in range(2):  # Se colocan dos esbirros
            while True:
                pos = input(f"Jugador Santa, introduce la posición del esbirro {i + 1} (fila, columna): ")
                try:
                    x, y = map(int, pos.split(","))
                    if (x, y) in posiciones_validas_bordes and (x, y) not in self.esbirros:
                        self.esbirros.append((x, y))
                        break
                    else:
                        print("Posición inválida o ya ocupada, intenta de nuevo.")
                except ValueError:
                    print("Formato inválido. Debes introducir fila y columna separadas por una coma.")

    def posicionar_reno(self) -> None:
        """Posiciona a Rudolph en una celda del tablero a partir de la entrada del usuario."""
        while True:
            pos = input("Jugador Reno, introduce la posición de Rudolph (fila, columna): ")
            try:
                x, y = map(int, pos.split(","))
                if (x, y) not in self.esbirros and (0 <= x < 3 and 0 <= y < 3):
                    self.reno = (x, y)
                    break
                else:
                    print("Posición inválida, intenta de nuevo.")
            except ValueError:
                print("Formato inválido. Debes introducir fila y columna separadas por una coma.")

    def posicionar_regalo(self) -> None:
        """Posiciona el regalo en una celda del tablero a partir de la entrada del usuario."""
        while True:
            pos = input("Jugador Reno, introduce la posición del regalo (fila, columna): ")
            try:
                x, y = map(int, pos.split(","))
                if (x, y) != self.reno and (0 <= x < 3 and 0 <= y < 3):
                    self.regalo = (x, y)
                    break
                else:
                    print("Posición inválida, intenta de nuevo.")
            except ValueError:
                print("Formato inválido. Debes introducir fila y columna separadas por una coma.")


    def mover_reno(self) -> None:
        """Mueve a Rudolph a una celda adyacente."""
        posibles_movimientos = self.obtener_celdas_adyacentes(self.reno)
        print(f"Posiciones disponibles para mover a Rudolph: {posibles_movimientos}")
        while True:
            nueva_pos = input("Introduce la nueva posición de Rudolph (fila, columna): ")
            try:
                x, y = map(int, nueva_pos.split(","))
                if (x, y) in posibles_movimientos:
                    self.reno = (x, y)
                    print(f"Rudolph se mueve a {self.reno}")
                    break
                else:
                    print("Movimiento inválido, intenta de nuevo.")
            except ValueError:
                print("Formato inválido. Debes introducir fila y columna separadas por una coma.")

    def mover_esbirro(self) -> None:
        """Mueve a uno de los esbirros alrededor del tablero."""
        print(f"Esbirros actuales: {self.esbirros}")
        while True:
            esbirro_idx = input("Selecciona el número del esbirro a mover (1 o 2): ")
            try:
                esbirro_idx = int(esbirro_idx) - 1
                if 0 <= esbirro_idx < len(self.esbirros):
                    esbirro_actual = self.esbirros[esbirro_idx]
                    posibles_movimientos = self.obtener_celdas_adyacentes(esbirro_actual, es_fueratablero=True)
                    print(f"Posiciones disponibles para mover al esbirro: {posibles_movimientos}")
                    nueva_pos = input("Introduce la nueva posición del esbirro (fila, columna): ")
                    x, y = map(int, nueva_pos.split(","))
                    if (x, y) in posibles_movimientos:
                        self.esbirros[esbirro_idx] = (x, y)
                        print(f"Esbirro {esbirro_idx + 1} se mueve a {self.esbirros[esbirro_idx]}")
                        break
                    else:
                        print("Movimiento inválido, intenta de nuevo.")
            except (ValueError, IndexError):
                print("Opción inválida. Intenta de nuevo.")

    def mover_regalo(self, modo_santa: bool) -> None:
        """Mueve el regalo a una nueva posición."""
        print(f"Posición actual del regalo: {self.regalo}")
        posibles_movimientos = [(i, j) for i in range(3) for j in range(3) if (i, j) != self.reno]
        print(f"Posiciones disponibles para mover el regalo: {posibles_movimientos}")
        while True:
            nueva_pos = input("Introduce la nueva posición del regalo (fila, columna): ")
            try:
                x, y = map(int, nueva_pos.split(","))
                if (x, y) in posibles_movimientos:
                    self.regalo = (x, y)
                    print(f"El regalo se mueve a {self.regalo}")
                    break
                else:
                    print("Movimiento inválido, intenta de nuevo.")
            except ValueError:
                print("Formato inválido. Debes introducir fila y columna separadas por una coma.")

    def obtener_celdas_adyacentes(self, pos, es_fueratablero=False):
        """Devuelve las celdas adyacentes a la posición actual."""
        x, y = pos
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        celdas_adyacentes = []
        for dx, dy in movimientos:
            nuevo_x, nuevo_y = x + dx, y + dy
            if es_fueratablero:
                # Permitimos movimiento en los bordes sin esquinas
                if (0 <= nuevo_x < 5) and ((nuevo_y in [0, 4]) or (nuevo_x in [0, 4] and 1 <= nuevo_y <= 3)):
                    celdas_adyacentes.append((nuevo_x, nuevo_y))
            else:
                if 0 <= nuevo_x < 3 and 0 <= nuevo_y < 3:
                    celdas_adyacentes.append((nuevo_x, nuevo_y))
        return celdas_adyacentes

    def hay_victoria(self) -> bool:
        """Verifica si hay un ganador."""
        # Lógica para determinar si hay una victoria
        return False  # A implementar

    def mostrar_estado(self) -> None:
        """Muestra el estado actual del juego."""
        self.mostrar(ocultar_renos=False)  # Mostrar a Rudolph

# Clase JugadorReno
class JugadorReno:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero

    def posicionar_equipo(self) -> None:
        self.tablero.posicionar_reno()
        self.tablero.posicionar_regalo()

    def turno(self) -> None:
        """Ejecuta el turno de Rudolph."""
        self.tablero.mostrar(ocultar_renos=False)
        self.tablero.mover_reno()
        # Aquí se pueden implementar más acciones, como mover el regalo o mover un esbirro.

# Clase JugadorSanta
class JugadorSanta:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero

    def posicionar_equipo(self) -> None:
        self.tablero.posicionar_esbirros()

    def turno(self) -> None:
        """Ejecuta el turno de Santa Claus."""
        self.tablero.mostrar(ocultar_renos=True)
        self.tablero.mover_esbirro()
        # Aquí se pueden implementar más acciones, como mover el regalo.

def main():
    num_rondas = 10
    tab = Tablero(num_rondas)
    jreno = JugadorReno(tab)
    jsanta = JugadorSanta(tab)

    # Fase de preparación
    jsanta.posicionar_equipo()
    jreno.posicionar_equipo()

    # Bucle del juego
    for _ in range(num_rondas):
        print(f"Ronda {tab.ronda_actual}")
        input('RUDOLPH, pulsa intro para comenzar tu turno')
        jreno.turno()
        input('RUDOLPH, pulsa intro para terminar tu turno')
        limpiar_terminal()

        input('SANTA, pulsa intro para comenzar tu turno')
        jsanta.turno()
        input('SANTA, pulsa intro para terminar tu turno')

        # Fase de comprobación (final de ronda)
        tab.mostrar_estado()
        if tab.hay_victoria():  # Hay un ganador
            input("La partida ha terminado. Pulsa intro para cerrar la aplicación")
            return
        else:  # Seguirían jugando
            input('Pulsa intro para continuar con la siguiente ronda')
        tab.ronda_actual += 1

if __name__ == "__main__":
    main()

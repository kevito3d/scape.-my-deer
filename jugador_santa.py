from tablero import Tablero
from utils import covert_position_esbirros, limpiar_terminal
class JugadorSanta:
    mover_regalo_cooldown = 0
    def __init__(self, tab:Tablero):
        self.tablero = tab

    def posicionar_equipo(self):
        print("Es momento de que el jugador que maneja santa posicione a su equipo")
        self.tablero.posicionar_esbirros()
        
    def menu(self):
        cooldown = self.mover_regalo_cooldown!=0
        print("Santa, es tu turno!. Acciones disponibles:")
        print("1. Mover un esbirro de santa")
        print(f"2. Mover el regalo{f" ( Cooldown restante {self.mover_regalo_cooldown})" if cooldown else ""}")
        opc = input("Selección: ")
        while True:
            if opc == "1":
                break
            elif opc == "2" and not cooldown:
                break
            else:
                print("Opción inválida, vuelve a elejir")
                opc = input("Selección: ")
        return opc

    def turno(self):
        self.tablero.mostrar(False)
        opc = self.menu()
        self.tablero.mostrar(False)
        if opc=="1":
            self.tablero.mover_esbirro()
        else:
            self.tablero.mover_regalo(True)
            self.mover_regalo_cooldown = 2
        cooldown = self.mover_regalo_cooldown
        if cooldown!=0:
            self.mover_regalo_cooldown = cooldown -1
        self.tablero.mostrar(False)
        
    
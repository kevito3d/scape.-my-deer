from tablero import Tablero
from utils import convert_position_tablero, limpiar_terminal
class JugadorReno:
    tablero:Tablero
    mover_esbirros_cooldown = 0
    def __init__(self, tab:Tablero):
      self.tablero = tab
    def getTablero(self):
      return self.tablero
    def posicionar_equipo(self):
      print("Es momento de que el jugador que maneja a Rudolf posicione a su equipo")
      self.tablero.posicionar_reno()
      self.tablero.posicionar_regalo()
      limpiar_terminal()

    def menu(self):
      cooldown = self.mover_esbirros_cooldown!=0
      print("Rudolf, es tu turno!. Acciones disponibles:")
      print("1. Moverme")
      print("2. Mover el regalo")
      print(f"3. Mover un esbirro de santa{f" ( Cooldown restante {self.mover_esbirros_cooldown})" if cooldown else ""}")
      opc = input("Selección: ")
      # while opc != "1" and opc != "2" and (not cooldown and opc!="3"):
      while True:
        if opc == "1" or opc == "2":
          break
        elif opc == "3" and not cooldown:
          break
        else:
          print("Opción inválida, vuelve a elejir")
          opc = input("Selección: ")
      return opc
      

    def turno(self):
      self.tablero.mostrar(False)
      if self.tablero.reno_inconciente:
        return
      opc = self.menu()
      if opc =="1":
        self.tablero.mover_reno()
      elif opc=="2":
        self.tablero.mover_regalo(False)
      else:
        self.tablero.mover_esbirro()
        self.mover_esbirros_cooldown = 3
      cooldown = self.mover_esbirros_cooldown
      if cooldown!=0:
        self.mover_esbirros_cooldown = cooldown -1
      self.tablero.mostrar(False)

    




    

    
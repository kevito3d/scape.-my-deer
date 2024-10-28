from tablero import Tablero
from utils import convert_position_tablero
class JugadorReno:
  # tablero:Tablero
  def __init__(self, tab:Tablero):
    self.tablero = tab

  def posicionar_equipo(self):
    print("Es momento de que el jugador que maneja a Rudolf posicione a su equipo")
    pos = input(f"Posiciona a tu Rudolf en el tablero: ")
    positions = convert_position_tablero(pos)
    print(positions)
    while positions[0]== -1:
      print("Posición no válida, vuelve a intentarlo")
      pos = input(f"Posiciona a tu Rudolf en el tablero: ")
      positions = convert_position_tablero(pos)
    
    self.tablero.setReno(positions[0],positions[1])

    pos =  input(f"Posiciona el regalo en el tablero: ")
    positions = convert_position_tablero(pos)
    while positions[0]== -1 or self.tablero.existeReno(positions[0],positions[1]):
      print("Posición no válida, vuelve a intentarlo")
      pos = input(f"Posiciona el regalo en el tablero: ")
      positions = convert_position_tablero(pos)
    self.tablero.setRegalo(positions[0],positions[1])

    
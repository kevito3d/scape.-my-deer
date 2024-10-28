from tablero import Tablero
from utils import covert_position_esbirros
class JugadorSanta:
    def __init__(self, tab:Tablero):
        self.tablero = tab
    
    def posicionar_equipo(self):
        print("Es momento de que el jugador que maneja santa posicione a su equipo")
        pos = input(f"Posiciona a tu esbirro (1) en el tablero: ")
        positions = covert_position_esbirros(pos)
        while positions[0]== -1:
            print("Posición no válida, vuelve a intentarlo")
            pos = input(f"Posiciona a tu esbirro (1) en el tablero: ")
            positions = covert_position_esbirros(pos)
        self.tablero.setEsbirros(0, positions[0],positions[1])
        
        pos =  input(f"Posiciona a tu esbirro (2) en el tablero: ")
        positions = covert_position_esbirros(pos)
        while positions[0]== -1 or self.tablero.existeReno(positions[0],positions[1]):
            print("Posición no válida, vuelve a intentarlo")
            pos = input(f"Posiciona a tu esbirro (2) en el tablero: ")
            positions = covert_position_esbirros(pos)
        self.tablero.setEsbirros(1, positions[0],positions[1])
            
    
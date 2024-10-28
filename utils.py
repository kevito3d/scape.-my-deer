# utils.py
def limpiar_terminal():
    """Limpia la consola para mejorar la experiencia de juego."""
    print(chr(27) + "[2J")
def covert_position_esbirros(pos:str):
    if pos == "0":
        return [1,0]
    elif pos == "1":
        return [2,0]
    elif pos == "2":
        return [3,0]
    elif pos == "3":
        return [4,1]
    elif pos == "4":
        return [4,2]
    elif pos == "5":
        return [4,3]
    elif pos == "6":
        return [3,4]
    elif pos == "7":
        return [2,4]
    elif pos == "8":
        return [1,4]
    elif pos == "9":
        return [0,3]
    elif pos == "10":
        return [0,2]
    elif pos == "11":
        return [0,1]
    else: return [-1,-1]

def convert_position_tablero(pos:str):
    if pos == "0":
        return [1,1]
    elif pos == "1":
        return [2,1]
    elif pos == "2":
        return [3,1]
    elif pos == "3":
        return [1,2]
    elif pos == "4":
        return [2,2]
    elif pos == "5":
        return [3,2]
    elif pos == "6":
        return [1,3]
    elif pos == "7":
        return [2,3]
    elif pos == "8":
        return [3,3]
    else:
        return [-1,-1]

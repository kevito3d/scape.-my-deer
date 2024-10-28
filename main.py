from tablero import Tablero
from jugador_reno import JugadorReno
from jugador_santa import JugadorSanta    
     
def main():
    tab = Tablero(rondas=10)
    reno = JugadorReno(tab)
    tab.mostrar(False)

    reno.posicionar_equipo()
    santa = JugadorSanta(tab)
    tab.mostrar(False)
    santa.posicionar_equipo()

    tab.mostrar(True)
    print(tab.verifica_si_esbirros_attrapan())

if __name__ == "__main__":
    main()
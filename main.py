from tablero import Tablero
from jugador_reno import JugadorReno
from jugador_santa import JugadorSanta    
from utils import limpiar_terminal
def main():
    rondas = 10
    tab = Tablero(rondas)
    reno = JugadorReno(tab)
    santa = JugadorSanta(tab)
    
    tab.mostrar(False)

    reno.posicionar_equipo()
    limpiar_terminal()
    santa.posicionar_equipo()
    while True:
        turno = tab.get_turno()

        if turno % 2 !=0:
            print(f"Ronda {turno}")
            input("Rudolf, pulsa intro para comenzar tu turno")
            reno.turno()
            input("Rudolf, pulsa intro para terminar tu turno")
            limpiar_terminal()
            print(f"Ronda {turno}")
            input("Santa, pulsa intro para comenzar tu turno")
            santa.turno()
            input("Santa, pulsa intro para terminar tu turno")
        else:
            print(f"Ronda {turno}")
            input("Santa, pulsa intro para comenzar tu turno")
            santa.turno()
            input("Santa, pulsa intro para terminar tu turno")
            limpiar_terminal()
            print(f"Ronda {turno}")
            input("Rudolf, pulsa intro para comenzar tu turno")
            reno.turno()
            input("Rudolf, pulsa intro para terminar tu turno")

        limpiar_terminal()
        victoria = tab.hay_victoria()
        if victoria:
            tab.mostrar(True)
        tab.mostrar_estado()
        if victoria:
            input("La partida ha terminado. Pulsa intro para terminar la aplicación")
            return
        else:
            input("Pulsa intro para continuar con la siguiente ronda")
        tab.aumentar_turno()


if __name__ == "__main__":
    main()
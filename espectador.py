# IMPORTANTE: ESTE CÓDIGO NO SE PUEDE MODIFICAR
import pickle
import sys
import socket
from utils import limpiar_terminal
from historico_partida import HistoricoPartida

def cliente(ip, puerto):
    try:
        # Conectamos con el servidor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, puerto))
        print('Bienvenidos al modo espectador de Escape, my Deer.')

        # Elegimos un nombre en el servidor
        usuariocorrecto = False
        while not usuariocorrecto:
            nombre = input("Introduce tu nombre de usuario: ")
            s.sendall(pickle.dumps(nombre))
            confirmacion = s.recv(1024)
            if not confirmacion:
                print("[ERROR] El servidor ha cancelado la conexión")
                s.close()
                return
            
            confirmacion = pickle.loads(confirmacion)
            if not confirmacion:
                print("[INFO] Nombre de usuario inválido")
                continue
            usuariocorrecto = True


        # Elegimos opción 3 => modo espectador
        s.sendall(pickle.dumps(3))
        confirmacion = s.recv(1024)
        if not confirmacion:
            print("[ERROR] El servidor ha cancelado la conexión")
            s.close()
            return

        # Bucle para dejar ver una partida y después otra
        
        # Nombre de la partida
        nombre_valido = False
        while not nombre_valido:
            nombre_partida = input("Introduce el nombre de la partida que quieres visualizar:\n")

            s.sendall(pickle.dumps(nombre_partida))
            resp = s.recv(1024)
            if not resp:
                print("[ERROR] El servidor ha cancelado la conexión")
                s.close()
                return
            resp = pickle.loads(resp) # True si es correcto
            if resp is False:
                print("[ERROR] La partida no existe!")
                continue
            
            nombre_valido = True
        s.sendall(pickle.dumps(True)) # Confirmamos OK a la partida

        resp = s.recv(4096) # Esperamos a recibir el historico de la partida
        if not resp:
            print("[ERROR] El servidor ha cancelado la conexión")
            s.close()
            return
        historico = pickle.loads(resp) 
        assert isinstance(historico, HistoricoPartida), "El mensaje recibido no es tipo HistoricoPartida"
        hora_fortmat = historico.hora_fin.strftime("%d/%m/%Y %H:%M")
        # print(fecha)
        # print(hora)
        print(f"Nombre de la partida: {historico.nombre}")
        print(f"Hora de finalización: {hora_fortmat}")
        print(f"Rudolph: {historico.nombre_reno}")
        print(f"Santa: {historico.nombre_santa}")
        print(f"Ganador: {historico.ganador}")
        
        # Bucle de visualización
        acciones = {"A": "Anterior", "S": "Siguiente", "X": "Salir"}
        actual = historico.primero() # Actual apunta al primer Nodo de la lista
        turno = 1
        ronda = 1
        while actual is not None:
            if ronda%2==0:
                jugador = "SANTA" if turno%2!=0 else "RUDOLPH"
            else:
                jugador = "RUDOLPH" if turno%2!=0 else "SANTA"

            # limpiar_terminal()
            print(f"Ronda {ronda}. Turno de {jugador}")
            actual.dato.mostrar(ocultar_renos=False)

            accion_correcta = False
            while not accion_correcta:
                if actual == historico.primero(): # Si es el primer turno, no se puede ir al anterior
                    acciones_disponibles = ["S", "X"]
                elif actual == historico.ultimo(): # Si es el último turno, no se puede ir al siguiente
                    acciones_disponibles = ["A", "X"]
                else: # Cualquier otro
                    acciones_disponibles = ["A", "S", "X"]
                
                msg = "Acción: "
                for ac in acciones_disponibles:
                    msg += f"{acciones[ac]} ({ac}) / "

                msg = msg[:-2] # Quitar última /
                accion = input(msg)
                accion = accion.upper()
                if accion not in acciones_disponibles:
                    continue
                else:
                    accion_correcta = True
                
            if accion == "S": # Acción Siguiente
                actual = actual.next
                turno += 1
                if turno%2==1:
                    ronda+=1
            elif accion == "A": # Acción Anterior
                actual = actual.prev
                turno -= 1
                if turno%2==0:
                    ronda-=1
            else: # Acción Salir
                print("Cerrando partida...\n\n")
                break

    except KeyboardInterrupt: # Si pulsa Ctrl+C para salir, salimos del bucle exterior
        print("Pulsado Ctrl+C. Cerrando modo expectador.")
    finally:
        s.close() # Cerramos socket cuando acaba la partida


if __name__ == '__main__':
    if len(sys.argv) !=3:
        print("[ERROR] Número de argumentos incorrecto. Para lanzar el cliente: python3 cliente.py <ip> <puerto>")
    else:
        cliente(sys.argv[1], int(sys.argv[2]))

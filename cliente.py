# IMPORTANTE: ESTE CÓDIGO NO SE PUEDE MODIFICAR
import pickle
import sys
import socket
from tablero import Tablero
from jugador_santa import JugadorSanta
from jugador_reno import JugadorReno

def cliente(ip, puerto):
    tablero = Tablero(10) # Tablero local del cliente. Se va sincronizando con lo que recibe del servidor.

    # Conectamos con el servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))
    print('Bienvenidos a Escape, my Deer. A jugar!')

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


    # Elegimos crear partida o unirnos a una
    opcion = -1
    while opcion not in [1, 2]:
        try:
            opcion = input("Menú:\n\t1. Partida nueva\n\t2. Unirse a una partida existente\n\n¿Qué quieres hacer?: ")
            opcion = int(opcion)
            if opcion not in [1, 2]:
                raise TypeError
        except:
            print("Opción inválida. Introduce un número de entre las opciones del menú")
    
    s.sendall(pickle.dumps(opcion))
    confirmacion = s.recv(1024)
    if not confirmacion:
        print("[ERROR] El servidor ha cancelado la conexión")
        s.close()
        return

    # Nombre de la partida
    if opcion == 1:
        msg = "Introduce el nombre de la nueva partida: "
    else:
        msg = "Introduce el nombre de la partida a la que te quieres unir: "
    
    nombre_valido = False
    while not nombre_valido:
        nombre_partida = input(msg)
        s.sendall(pickle.dumps(nombre_partida))
        resp = s.recv(1024)
        if not resp:
            print("[ERROR] El servidor ha cancelado la conexión")
            s.close()
            return
        resp = pickle.loads(resp) # True si es correcto
        if resp is False:
            if opcion == 1:
                error_msg = "[ERROR] El nombre de la partida no está disponible."
            else:
                error_msg = "[ERROR] La partida no existe!"
            print(error_msg)
            continue
        
        nombre_valido = True

    s.sendall(pickle.dumps(True)) # Confirmamos OK a la partida

    resp = s.recv(1024) # Esperamos al nombre del otro jugador
    if not resp:
        print("[ERROR] El servidor ha cancelado la conexión")
        s.close()
        return
    resp = pickle.loads(resp) 
    s.sendall(pickle.dumps(True)) # Confirmamos OK al nombre del oponente
    
    print(f"{nombre}, jugarás la partida {nombre_partida} contra {resp}")

    ## Comienza la partida
    # Recibir tipo de jugador
    tipojugador = s.recv(1024)
    if not tipojugador:
        print("[ERROR] El servidor ha cancelado la conexión")
        s.close()
        return
    tipojugador = pickle.loads(tipojugador)
    
    print(f"{nombre}, jugarás como {tipojugador}")

    # Declaramos una variable jugador, que representa una instancia de la clase correspondiente,
    # dependiendo de si el sorteo en el servidor nos asigna jugar como SANTA o como RUDOLPH 
    # Como ambas clases tienen definidas las funciones .posicionar_equipo() y .turno(), se pueden
    # invocar haciendo jugador.nombre_funcion() independientemente de si es un JugadorSanta o JugadorReno
    # Esto se llama POLIMORFISMO. Si quieres saber más, está explicado en detalle en el Tema 5 (material 
    # extra del Bloque II)
    jugador = None
    if tipojugador == 'SANTA':
        jugador = JugadorSanta(tablero)
    elif tipojugador == 'RUDOLPH':
        jugador = JugadorReno(tablero)
    else:
        print(f"[ERROR] Recibido tipo de jugador incorrecto {tipojugador}")
        return

    ## Posicionamiento
    if tipojugador == 'RUDOLPH':  # Actualizar tablero con esbirros posicionados por SANTA
        s.sendall(pickle.dumps(True)) # Para vaciar el buffer
        print("Espera mientras SANTA posiciona su equipo")
        resp = s.recv(1024)
        if not resp:
            print("[ERROR] El servidor ha cancelado la conexión")
            s.close()
            return
        tab = pickle.loads(resp)
        tablero.actualizar(tab)
        print("[INFO] SANTA ya ha posicionado su equipo")

    jugador.posicionar_equipo()

    # Enviar tablero
    s.sendall(pickle.dumps(tablero))

    # Recibir confirmacion
    if tipojugador == 'SANTA':
        print("Espera mientras RUDOLPH posiciona su equipo")
        resp = s.recv(1024)
        if not resp:
            print("[ERROR] El servidor ha cancelado la conexión")
            s.close()
            return
        tab = pickle.loads(resp)
        tablero.actualizar(tab)
        print("[INFO] RUDOLPH ya ha posicionado su equipo")
    
    ## Jugar partida
    if tipojugador == 'SANTA':
        resto_jugar = 0 # Empieza a jugar en las rondas pares
    else: # RUDOLPH
        resto_jugar = 1 # Empieza a jugar en las rondas impares

    for ronda_actual in range(1, 11):
        print(f"Ronda {ronda_actual}")
        if ronda_actual%2==resto_jugar:
            # Jugar
            input(f'{tipojugador}, pulsa intro para comenzar tu turno')
            jugador.turno()
            input(f'{tipojugador}, pulsa intro para terminar tu turno')
            
            # Enviar tablero
            s.sendall(pickle.dumps(tablero))
            
            # Juega el oponente
            print(f'El oponente está jugando su turno, espere...')
            
            # Recibir tablero
            tab = s.recv(1024)
            if not tab:
                print("[ERROR] El servidor ha cancelado la conexión")
                s.close()
                return
            tab = pickle.loads(tab)
            tablero.actualizar(tab)
            print(f'El turno del oponente ha terminado')
        else:
            # Juega el oponente
            print(f'El oponente está jugando su turno, espere...')

            # Recibir tablero
            tab = s.recv(1024)
            if not tab:
                print("[ERROR] El servidor ha cancelado la conexión")
                s.close()
                return
            tab = pickle.loads(tab)
            tablero.actualizar(tab)
            print(f'El turno del oponente ha terminado')
            
            # Jugar
            input(f'{tipojugador}, pulsa intro para comenzar tu turno')
            jugador.turno()
            input(f'{tipojugador}, pulsa intro para terminar tu turno')
            
            # Enviar tablero
            s.sendall(pickle.dumps(tablero))

        # Mostrar estado del tablero al final de la ronda
        tablero.mostrar_estado()

        # Enviar True si hay victoria y False si no, para que el servidor coordine el final de la ronda y de la partida
        if tablero.hay_victoria():
            tablero.mostrar(ocultar_renos=False)
            input("La partida ha terminado. Pulsa intro para cerrar la aplicación")
            s.sendall(pickle.dumps(True))
            s.close()
            return
        else: # Sin victoria. Se sigue jugando
            s.sendall(pickle.dumps(False)) 
    
    s.close() # Cerramos socket cuando acaba la partida
    return 0


if __name__ == '__main__':
    if len(sys.argv) !=3:
        print("[ERROR] Número de argumentos incorrecto. Para lanzar el cliente: python3 cliente.py <ip> <puerto>")
    else:
        cliente(sys.argv[1], int(sys.argv[2]))

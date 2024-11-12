import sys   
import socket
from usuario import Usuario
from partida import Partida
from tablero import Tablero
import threading
from typing import List, Tuple, Optional
partidas :List[Partida] = []

def verifica_si_partida_existe(nueva)-> Tuple[bool,Optional[Partida]]:
    global partidas
    for partida in partidas:
        nombre =partida.getNombre()
        if nueva == nombre:
            return [True, partida]
    return [False,None]



def bienvenida_usuario(clt_socket, clt_addr): # Emparejamiento de clientes y creación de partidas
    global partidas
    usuario = Usuario(clt_socket,clt_addr)
    nombre = usuario.recivirData()
    # validar nombre de usuario
    valido = True
    if len(nombre)<1:
        valido = False
    if valido:
        usuario.datatoSend(True)
    usuario.setNombre(nombre)
    # si me envian 1 es partida nueva si envian 2 es unirme
    eleccion_de_partida = usuario.recivirData(converToInt=True)
    usuario.datatoSend(True)

    not_valido = True
    nombre_partida = ""
    existe = False
    partida = Optional[Partida]
    while not_valido:
        nombre_partida = usuario.recivirData()
        # if eleccion_de_partida ==1:
        existe, partida =verifica_si_partida_existe(nombre_partida)
        usuario.datatoSend(not existe if eleccion_de_partida ==1 else  existe)
        not_valido =not( not existe if eleccion_de_partida ==1 else existe)
    
        # else:
        #     existe =verifica_si_partida_existe(nombre_partida)
        #     usuario.datatoSend(not existe)'
    usuario.recivirData()
    if eleccion_de_partida ==1:
        tablero = Tablero(10)
        partidaNew = Partida(nombre_partida,tablero,usuario)
        partidas.append(partidaNew)
        # en este punto el usuario que creo la partida se le muere este threard 
        # simplemente el se queda esperando que alguien se una a su partida
        # lo cual se hace en el else que es cuando alguien se une
    else:
        partida.setUsuario2(usuario)
        # mandar mensaje a unuario 1 que ya se le encontro partida
        usuario1 = partida.getUsuario1()
        usuario1.datatoSend(nombre)
        usuario.datatoSend(usuario1.getNombre())
        thread = threading.Thread(target=jugar_partida, args=(partida,))
        thread.start()

    




    


def jugar_partida(partida:Partida): # Gestión de la partida
    print("deberia comensar a jugar ya qui deberia tener a los dos jugadores")


def servidor(puerto): # Configuración y lanzamiento del servidor
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'

     # Vincula el socket a la dirección y al puerto
    server_address = (ip, puerto)
    print(f'starting up on {server_address}')
    sock.bind(server_address)

    sock.listen(1)
    while True:
        connection , client_address = sock.accept()
        print(connection)
        hilo = threading.Thread(target=bienvenida_usuario, args=(connection, client_address))
        hilo.start()


if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("[ERROR] Número de argumentos incorrecto. Para lanzar el servidor: python3 servidor.py <puerto>")
    else:
        servidor(int(sys.argv[1])) 
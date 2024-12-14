import sys   
import socket
import pickle
from datetime import datetime
from usuario import Usuario
from partida import Partida
from tablero import Tablero
import threading
from typing import List, Tuple, Optional
import random
import atexit
from historico_partida import HistoricoPartida

partidas :List[Partida] = []

partidasTerminadas = {}
filetxt = "historial_partidas.txt"



def verifica_si_existe_historial(nombre):
    global partidasTerminadas
    for clave, valor in partidasTerminadas.items():
        if nombre == clave:
            return valor
    return None

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
    historial = Optional[HistoricoPartida]
    while not_valido:
        try:
            nombre_partida = usuario.recivirData()
        except:
            break
        if eleccion_de_partida !=3:
            existe, partida =verifica_si_partida_existe(nombre_partida)
            usuario.datatoSend(not existe if eleccion_de_partida ==1 else  existe)
            not_valido =not( not existe if eleccion_de_partida ==1 else existe)
        else:
            historial =verifica_si_existe_historial(nombre_partida)
            usuario.datatoSend(True if historial !=None else  False)
            if historial:
                break
    
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
    elif eleccion_de_partida==2:
        partida.setUsuario2(usuario)
        # mandar mensaje a unuario 1 que ya se le encontro partida
        usuario1 = partida.getUsuario1()
        usuario1.datatoSend(nombre)
        usuario.datatoSend(usuario1.getNombre())
        thread = threading.Thread(target=jugar_partida, args=(partida,))
        thread.start()
    else: 
        # espectador, si envia la opción 3
        usuario.datatoSend(historial)
        
        
    if eleccion_de_partida!=3:    
        usuario.recivirData()

def jugar_partida(partida:Partida): # Gestión de la partida
    # tirar moneda
    int_ran = random.randint(1,2)
    # int_ran = 1
    if int_ran == 1:
        # usuario1 es rudolph
        # usuario2 es santa
        partida.getUsuario1().datatoSend("RUDOLPH")
        partida.getUsuario2().datatoSend("SANTA")

        partida.getUsuario1().recivirData() #para limpiear el bufer
        tablero = partida.getUsuario2().recivirData()
        partida.getUsuario1().datatoSend(tablero)
        
        tablero = partida.getUsuario1().recivirData()
        partida.getUsuario2().datatoSend(tablero)

        partida.tablero.actualizar(tablero)
        # partida.setTablero(tablero)
        # buferNew = partida.getUsuario1().recivirData()
        # print(buferNew)

        
    else:
        # usuario1 el santa
        # usuario2 es rudolph
        partida.getUsuario1().datatoSend("SANTA")
        partida.getUsuario2().datatoSend("RUDOLPH")

        partida.getUsuario2().recivirData() #para limpiear el bufer
        tablero = partida.getUsuario1().recivirData()
        partida.getUsuario2().datatoSend(tablero)

        tablero = partida.getUsuario2().recivirData()
        partida.getUsuario1().datatoSend(tablero)

        partida.tablero.actualizar(tablero)

        # buferNew = partida.getUsuario2().recivirData()
        # print(buferNew)
    historico = HistoricoPartida(partida.getNombre(), partida.getUsuario2().getNombre() if int_ran==1 else partida.getUsuario1().getNombre(), partida.getUsuario1().getNombre() if int_ran==1 else partida.getUsuario2().getNombre())
    historico.add_turno(partida.tablero)
    
    # print(partida.tablero)
    tablero = partida.tablero
    santa = partida.getUsuario2() if int_ran==1 else partida.getUsuario1()
    rudolph = partida.getUsuario1() if int_ran==1 else partida.getUsuario2()

    while True:
        turno = tablero.get_turno()
        if turno % 2 !=0:
            new_tab = rudolph.recivirData()
            historico.add_turno(new_tab)
            new_tab.turno = turno
            tablero.actualizar(new_tab)
            tablero.aumentar_turno()
            santa.datatoSend(tablero)
            new_tab = santa.recivirData()
            historico.add_turno(new_tab)
            tablero.actualizar(new_tab)
            # tablero.aumentar_turno()
            rudolph.datatoSend(tablero)
        else:
            new_tab = santa.recivirData()
            new_tab.turno = turno
            historico.add_turno(new_tab)
            tablero.actualizar(new_tab)
            tablero.aumentar_turno()
            rudolph.datatoSend(tablero)
            new_tab = rudolph.recivirData()
            historico.add_turno(new_tab)
            tablero.actualizar(new_tab)
            # tablero.aumentar_turno()
            santa.datatoSend(tablero)
        victoriaR=rudolph.recivirData()
        victoriaS=santa.recivirData()
        if victoriaR or victoriaS:
            # partidas.remove(partida)
            hora_fin =datetime.now()
            historico.set_hora_fin(hora_fin)
            tablero.hay_victoria()
            historico.set_ganador(tablero.ganador)
            save_partida(historico)
            break
        # print(tablero)
def save_partida(historial:HistoricoPartida):
    global partidasTerminadas
    partidasTerminadas[f"{historial.nombre}"]=historial

def read_historico():
    global filetxt
    global partidasTerminadas
    file = open (filetxt, "r")
    lines = file.readlines()
    for line in lines:
        line = line[:-1]
        [clave,valor]= line.split(":")
        bytesHitorico =bytes.fromhex(valor)
        objHistorico = pickle.loads(bytesHitorico)
        partidasTerminadas[clave]=objHistorico
    print(partidasTerminadas)
    file.close()
    
    
# def read_file_extension(file)->LDE:
#     file = open(file, "r")
#     lines = file.readlines()

#     lista = LDE()
#     for line in lines:
#         # quitar el ultimo caracter
#         line = line[:-1]
#         # Formato de cada línea: usuario:puntuacion:oponente:fechayhora (año-mes-dia-hora-minuto)
#         # valeria:1380:alex:2023-11-27-10-50
#         [name,score,oponente,fecha]= line.split(":")
#         lista.enlistar(PlayerScore(score= int(score),nombre= name,oponente=oponente,fecha=fecha))
# def leer_partidas():
#     file  =  open("historial_partidas.txt", "r")
#     lines = file.readlines()
#     for line in lines:

def write_in_file():
    global filetxt
    global partidasTerminadas
    file = open(filetxt, "w")
    for clave, valor in partidasTerminadas.items():
        bytesHistorico = pickle.dumps(valor)
        stringHistorico = bytesHistorico.hex()
        file.write(f"{clave}:{stringHistorico}\n")
    file.close()
        

    file.close()

def close_socket(sock):
    print("Cerrando socket...")
    write_in_file()
    sock.close()

def servidor(puerto): # Configuración y lanzamiento del servidor
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'

     # Vincula el socket a la dirección y al puerto
    server_address = (ip, puerto)
    print(f'starting up on {server_address}')
    sock.bind(server_address)

    sock.listen(1)
    sock.settimeout(1.0) 
    atexit.register(close_socket, sock)
    read_historico()
    try:
        while True:
            try:
                connection, client_address = sock.accept()
                hilo = threading.Thread(target=bienvenida_usuario, args=(connection, client_address))
                hilo.start()
            except socket.timeout:
                continue  # Continuar el bucle si se produce un tiempo de espera
    except KeyboardInterrupt:
        print("Interrupción del teclado recibida. Cerrando el servidor...")
    # finally:
    #     close_socket(sock)


if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("[ERROR] Número de argumentos incorrecto. Para lanzar el servidor: python3 servidor.py <puerto>")
    else:
        servidor(int(sys.argv[1])) 
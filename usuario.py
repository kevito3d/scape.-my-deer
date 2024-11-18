import socket
import pickle
# from utils import convertToBytes, convertToDict
# from phase_game import PhaseGame
class Usuario():
    nombre=""
    def __init__(self, connection: socket.socket, client_address) -> None:
        
        self.connection = connection
        self.client_address =client_address
    
    def setNombre(self, nombre):
        self.nombre = nombre
    
    def getNombre(self):
        return self.nombre

    def datatoSend(self,message):
        
         data = pickle.dumps(message)
         self.connection.sendto(data, self.client_address)

    def recivirData(self, converToInt = False):
        try:
            data = self.connection.recv(4096) 
            data_unpickle = pickle.loads(data)
            if converToInt:
                return int(data_unpickle)
            return data_unpickle
        except socket.error as e:
            print(e)
            return None
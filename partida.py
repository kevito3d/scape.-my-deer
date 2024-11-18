from typing import  Optional
from usuario import Usuario
from tablero import Tablero
class Partida:
    nombre = ""
    tablero=Optional[Tablero]
    usuario1 = None
    usuario2 = Optional[Usuario]
    def __init__(self, nombrePartida, tablero, usuario1):
        self.nombre = nombrePartida
        self.tablero = tablero
        self.usuario1 = usuario1
    def setTablero(self, tablero):
        self.tablero = tablero
    
    def setUsuario2(self, usuario2:Usuario):
        self.usuario2 = usuario2
    
    def getUsuario1(self) -> Usuario:
        return self.usuario1
    
    def getUsuario2(self)-> Usuario:
        return self.usuario2

    def getNombre(self):
        return self.nombre
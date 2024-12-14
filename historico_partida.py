from lista_doble_enlazada import ListaDobleEnlazada
from tablero import Tablero
from datetime import datetime
class HistoricoPartida:
    nombre:str
    nombre_santa:str
    nombre_reno:str
    ganador:str
    hora_fin:datetime
    turnos:ListaDobleEnlazada
    def __init__(self, nombre, nombre_santa,nombre_reno):
        self.nombre = nombre
        self.turnos = ListaDobleEnlazada()
        self.nombre_reno = nombre_reno
        self.nombre_santa = nombre_santa
        
    def set_hora_fin(self, hora_fin):
        self.hora_fin = hora_fin
    def set_ganador(self, ganador):
        self.ganador = ganador
    def add_turno(self,tablero:Tablero):
        self.turnos.agregar_al_final(dato=tablero)
    def primero(self):
        return self.turnos.obtener_cabeza()
    def ultimo(self):
        return self.turnos.obtener_cola()
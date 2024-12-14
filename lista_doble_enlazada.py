from tablero import Tablero
class Nodo:
    def __init__(self, dato:Tablero):
        self.dato = dato
        self.next = None
        self.prev = None

class ListaDobleEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar_al_inicio(self, dato:Tablero):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.next = self.cabeza
            self.cabeza.prev = nuevo_nodo
            self.cabeza = nuevo_nodo

    def agregar_al_final(self, dato:Tablero):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.next = nuevo_nodo
            nuevo_nodo.prev = self.cola
            self.cola = nuevo_nodo

    def obtener_cabeza(self):
        return self.cabeza
    
    def obtener_cola(self):
        return self.cola
    
    def imprimir_lista(self):
        temp = self.cabeza
        while temp:
            print(temp.dato, end=' ')
            temp = temp.next
        print()

# Ejemplo de uso
# lista = ListaDobleEnlazada()
# lista.agregar_al_inicio(3)
# lista.agregar_al_inicio(2)
# lista.agregar_al_inicio(1)
# lista.agregar_al_final(4)
# lista.agregar_al_final(5)

# lista.imprimir_lista()  # Salida: 1 2 3 4 5

# cabeza, cola = lista.obtener_cabeza_y_cola()
# print(f'Cabeza: {cabeza.dato}, Cola: {cola.dato}')  # Salida: Cabeza: 1, Cola: 5

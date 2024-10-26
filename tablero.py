from posicion import Posicion
class Tablero:
    turnos = 0
    esbirros = [Posicion(0,1),Posicion(4,1)]
    reno = Posicion(1,1)
    regalo = Posicion(1,1)
    rondas=0
    fil = 5
    col =5
    
    def __init__(self, rondas ):
        self.rondas=rondas
    
    def existeEsbirro(self,x,y):
        if self.esbirros[0].getX()==x and self.esbirros[0].getY()==y:
            return True
        if self.esbirros[1].getX()==x and self.esbirros[1].getY()==y:
            return True
        return False
    
    def existeReno(self, x,y):
        if self.reno.getX()==x and self.reno.getY()==y:
            return True
        return False
    
    def existeRegalo(self, x,y):
        if self.regalo.getX()==x and self.regalo.getY()==y:
            return True
        return False

    def mostrar (self, renos:bool):
            # for y in range(5):
            #     for x in range(5):
            #         if self.existeEsbirro(x,y):
            #             print(u"\U0001F385",end="")
            #         if self.existeRegalo(x,y):
            #             print(u"\U0001F381",end="")
            #         if self.existeReno(x,y):
            #             print(u"\U0001F98C",end="")
            #         print(" ",end="")
            #     print("")
            print("┌" + "─" * 3, end="")  # Esquina superior izquierda
            for c in range(self.col - 1):
                print("┬" + "─" * 3, end="")  # Esquinas intermedias superiores
            print("┐")  # Esquina superior derecha

            # Imprimir las filas intermedias con contorno lateral y intersecciones
            for f in range(self.fil - 1):
                print("│" + u"\U0001F98C" +" ", end="")  # Lateral izquierdo
                for c in range(self.col - 1):
                    print("│" + u"\U0001F98C" +" ", end="")  # Lados internos
                print("│")  # Lateral derecho

                # Imprimir las intersecciones y líneas entre filas
                print("├" + "─" * 3, end="")  # Esquina izquierda de intersección
                for c in range(self.col - 1):
                    print("┼" + "─" * 3, end="")  # Intersecciones internas
                print("┤")  # Esquina derecha de intersección

            # Imprimir la última fila de contenido
            print("│" + " " * 3, end="")  # Lateral izquierdo
            for c in range(self.col - 1):
                print("│" + " " * 3, end="")  # Lados internos
            print("│")  # Lateral derecho

            # Imprimir la última fila (inferior)
            print("└" + "─" * 3, end="")  # Esquina inferior izquierda
            for c in range(self.col - 1):
                print("┴" + "─" * 3, end="")  # Esquinas intermedias inferiores
            print("┘")  # Esquina inferior derecha
          

                        
                    

                
        

tab = Tablero(rondas=10)
tab.mostrar(renos=True)
                
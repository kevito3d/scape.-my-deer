from posicion import Posicion

ESBIRRO = u"\U0001F385"   # 🎅
REGALO = u"\U0001F381"    # 🎁
RUDOLPH = u"\U0001F98C"   # 🦌
INCONSCIENTE = u"\U0001F480" # 💀
class Tablero:
    turnos = 0
    esbirros = [Posicion(-1,-1),Posicion(-1,-1)]
    reno = Posicion(-1,-1)
    regalo = Posicion(-1,-1)
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
    def setReno(self, x,y):
        self.reno = Posicion(x,y)
    
    def setRegalo(self, x,y):
        self.regalo = Posicion(x,y)
    
    def setEsbirros(self,numero, x,y):
        # if numero!=0 or numero != 1:
        #     return False
        self.esbirros[numero] = Posicion(x,y)
        return True
    
    

    def mostrar (self, reno:bool):
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
            print(" " + " " * 3, end="")  # Esquina superior izquierda
            for x in range(self.col - 1):
                print("" + " " * 3, end="")  # Esquinas intermedias superiores
            print(" ")  # Esquina superior derecha

            # Imprimir las filas intermedias con contorno lateral y intersecciones
            for y in range(self.fil - 1):
                # print(y)
                if reno and self.existeEsbirro(x=0,y=y):
                    print(" " + ESBIRRO+" ", end="")  # Lados internos
                else:
                    print(" "  + " "*3, end="")  # Lateral izquierdo
                pared = " " if y==0 else "│" 
                for x in range(self.col - 1):
                    if reno and self.existeReno(x=x+1,y=y):
                    
                        print(pared + RUDOLPH+" ", end="")  # Lados internos
                    elif self.existeRegalo(x=x+1,y=y):
                        print(pared + REGALO+" ", end="")  # Lados internos

                    elif self.existeEsbirro(x=x+1,y=y):
                        print(pared + ESBIRRO+" ", end="")  # Lados internos

                    else: 
                        print(pared +" "*3, end="")  # Lateral izquierdo
                print(" ")  # Lateral derecho

                # Imprimir las intersecciones y líneas entre filas
                print(" "+ " " * 3, end="")  # Esquina izquierda de intersección
                for x in range(self.col - 1):
                    # print(x)
                    print("┼" +( (" "*3) if x+1==(self.col-1) else ("─" * 3)), end="")  # Intersecciones internas
                print(" ")  # Esquina derecha de intersección

            # Imprimir la última fila de contenido
            print(" " + " " * 3, end="")  # Lateral izquierdo
            for x in range(self.col - 1):
                if self.existeEsbirro(x=x+1,y=y+1):
                    print(" " + ESBIRRO+" ", end="")  # Lados internos
                else:
                    print(" " + " " * 3, end="")  # Lados internos
            print(" ")  # Lateral derecho

            # Imprimir la última fila (inferior)
            print( " "  + " " * 3, end="")  # Esquina inferior izquierda
            for x in range(self.col - 1):
                    print(" " + " "*3, end="")  # Esquinas intermedias inferiores
            print(" ")  # Esquina inferior derecha
          
    def verifica_si_esbirros_attrapan(self):
        positions1 = self.esbirros[0].getPosicion()
        positions2 = self.esbirros[1].getPosicion()
        print(positions1)
        x1 = positions1[0]
        y1 = positions1[1]
        encontrado = False

        if x1 == 0 or x1 ==4:
            for i in range(1 if x1==0 else self.col-2 ,self.col-1 if x1==0 else 0, +1 if x1==0 else -1):
                if self.existeRegalo(i,y1):
                    break
                if self.existeReno(i,y1):
                    encontrado = True
                    break
        else: #quiere decir que esta en mirando en vertical y no en horizontal
            for i in range(1 if y1==0 else self.fil-2 ,self.fil-1 if y1==0 else 0, +1 if y1==0 else -1):
                if self.existeRegalo(x1,i):
                    break
                if self.existeReno(x1,i):
                    encontrado = True
                    break

        
        x2 = positions2[0]
        y2 = positions2[1]

        if x2 == 0 or x2 ==4:
            for i in range(1 if x2==0 else self.col-2 ,self.col-1 if x2==0 else 0, +1 if x2==0 else -1):
                if self.existeRegalo(i,y2):
                    break
                if self.existeReno(i,y2):
                    encontrado = True
                    break
        else: #quiere decir que esta en mirando en vertical y no en horizontal
            for i in range(1 if y2==0 else self.fil-2 ,self.fil-1 if y2==0 else 0, +1 if y2==0 else -1):
                if self.existeRegalo(x2,i):
                    break
                if self.existeReno(x2,i):
                    encontrado = True
                    break
        return encontrado
                        

                
     


                
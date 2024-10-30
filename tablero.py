from posicion import Posicion
from utils import covert_position_esbirros
from utils import convert_position_tablero

ESBIRRO = u"\U0001F385"   # 🎅
REGALO = u"\U0001F381"    # 🎁
RUDOLPH = u"\U0001F98C"   # 🦌
INCONSCIENTE = u"\U0001F480" # 💀
class Tablero:
    turno = 1
    esbirros = [Posicion(-1,-1),Posicion(-1,-1)]
    reno = Posicion(-1,-1)
    regalo = Posicion(-1,-1)
    rondas=0
    fil = 5
    col =5
    reno_inconciente = False
    
    def __init__(self, rondas ):
        self.rondas=rondas

    def aumentar_turno(self):
        self.turno = self.turno +1

    def get_turno(self):
        return self.turno
    
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
                if self.existeEsbirro(x=0,y=y):
                    print(" " + ESBIRRO+" ", end="")  # Lados internos
                else:
                    print(" "  + " "*3, end="")  # Lateral izquierdo
                pared = " " if y==0 else "│" 
                for x in range(self.col - 1):
                    if reno and self.existeReno(x=x+1,y=y) and self.reno_inconciente:
                        print(pared + INCONSCIENTE+" ", end="")  # Lados internos

                    elif reno and self.existeReno(x=x+1,y=y):
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
          
    def is_esbirros_atrapan_reno(self):
        positions1 = self.esbirros[0].getPosicion()
        positions2 = self.esbirros[1].getPosicion()
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

    def posicionar_esbirros(self):
        pos = input(f"Posiciona a tu esbirro (1) en el tablero: ")
        positions = covert_position_esbirros(pos)
        while positions[0]== -1:
            print("Posición no válida, vuelve a intentarlo")
            pos = input(f"Posiciona a tu esbirro (1) en el tablero: ")
            positions = covert_position_esbirros(pos)
        self.setEsbirros(0, positions[0],positions[1])
        pos =  input(f"Posiciona a tu esbirro (2) en el tablero: ")
        positions = covert_position_esbirros(pos)
        while positions[0]== -1 or self.existeReno(positions[0],positions[1]):
            print("Posición no válida, vuelve a intentarlo")
            pos = input(f"Posiciona a tu esbirro (2) en el tablero: ")
            positions = covert_position_esbirros(pos)
        self.setEsbirros(1, positions[0],positions[1])
    
    def posicionar_reno(self):
        pos = input(f"Posiciona a tu Rudolf en el tablero: ")
        positions = convert_position_tablero(pos)
        while positions[0]== -1:
            print("Posición no válida, vuelve a intentarlo")
            pos = input(f"Posiciona a tu Rudolf en el tablero: ")
            positions = convert_position_tablero(pos)
        
        self.setReno(positions[0],positions[1])
    
    def posicionar_regalo(self):
        pos =  input(f"Posiciona el regalo en el tablero: ")
        positions = convert_position_tablero(pos)
        while positions[0]== -1 or self.existeReno(positions[0],positions[1]):
            print("Posición no válida, vuelve a intentarlo")
            pos = input(f"Posiciona el regalo en el tablero: ")
            positions = convert_position_tablero(pos)
        self.setRegalo(positions[0],positions[1])
        
    def mover_reno(self):
        reno = self.reno
        xreno = reno.getX()
        yreno = reno.getY()
        izq = Posicion(xreno-1,yreno)
        arr = Posicion(xreno,yreno-1)
        der = Posicion(xreno+1,yreno)
        aba = Posicion(xreno,yreno+1)
        posibles_posiciones = [izq,arr,der,aba]
        posiciones_disponibles = []

        for i in range (len(posibles_posiciones)):
            item = posibles_posiciones[i]
            if item.getAliasReno()==-1:
                continue
            if not self.existeRegalo(item.getX(),item.getY()):
                posiciones_disponibles.append(str(item.getAliasReno()))
        
        print(f"Te moveras,tu posicion actual es la {self.reno.getAliasReno()}")
        pos = input(f"escrige nueeva posicion para el reno {posiciones_disponibles}: ")
        while  pos not in posiciones_disponibles:
            print("Posición inválida, vuelve a introducir posición")
            pos = input(f"escrige nueeva posicion para el reno {posiciones_disponibles}: ")
        nueva_pos = convert_position_tablero(pos)
        self.reno.setX(nueva_pos[0])
        self.reno.setY(nueva_pos[1])

    def hay_victoria(self):
        if self.is_esbirros_atrapan_reno():
            return True
        if self.reno_inconciente:
            return True
        if self.turno > self.rondas:
            return True
        return False

            

    def mover_regalo(self, modo_santa:bool):
        
        posiciones_disponibles = []
        for y in range(1,self.fil-1):
            for x in range(1,self.col-1):
                if not modo_santa and self.existeReno(x,y):
                    continue
                posiciones_disponibles.append(str(Posicion(x,y).getAliasReno()))

        print(f"Moveras el regalo, posicion actual es la {self.regalo.getAliasReno()}")
        pos = input(f"escribe una nueva posicion para el regalo {posiciones_disponibles}: ")
        while  pos not in posiciones_disponibles:
            print("Posición inválida, vuelve a introducir posición")
            pos = input(f"escribe una nueva posicion para el regalo {posiciones_disponibles}: ")
        nueva_pos = convert_position_tablero(pos)
        self.regalo.setX(nueva_pos[0])
        self.regalo.setY(nueva_pos[1])
        if modo_santa :
            if self.reno.getPosicion() == self.regalo.getPosicion():
                self.reno_inconciente=True
    
    def mover_esbirro(self):
        esbirro1 = self.esbirros[0]
        esbirro2 = self.esbirros[1]
        posicion_esbirro1 = esbirro1.getAliasEsbirro()
        posicion_esbirro2 = esbirro2.getAliasEsbirro()
        print("Elige que esbirro mover")
        print(f"Esbirro 1 (Posición {str(posicion_esbirro1)})")
        print(f"Esbirro 2 (Posición {str(posicion_esbirro2)})")
        xesbirro = input("Selección: ")
        while xesbirro !="1" and xesbirro!="2":
            print("Elije un esbirro bien: 1 o 2")
            xesbirro = input("Selección: ")
        print(f"Moveras el esbirro {xesbirro}")
        izq = -1
        der = -1
        not_izq = False
        not_der = False
        if xesbirro == "1":
            izq = posicion_esbirro1 -1
            der = posicion_esbirro1 +1
        else:
            izq = posicion_esbirro2 -1
            der = posicion_esbirro2 +1
        if izq == -1:
            izq = 11
        if der == 12:
            der = 0
        
        if xesbirro =="1":
            if izq == posicion_esbirro2:
                not_izq = True
            if der == posicion_esbirro2:
                not_der = True
        else:    
            if izq == posicion_esbirro1:
                not_izq = True
            if der == posicion_esbirro1:
                not_der = True

        izq = str(izq)
        der = str(der)


        positions_diponibles = []
        if not not_izq:
            positions_diponibles.append(izq)
        if not not_der:
            positions_diponibles.append(der)
        print(f"Elige la nueva posicion para este esbirro {positions_diponibles}")
        pos = input("Selección: ")
        while pos not in positions_diponibles:
            print("Posición inválida, vuelve a ingresar posición")
            pos = input("Selección: ")
        
        posicion =covert_position_esbirros(pos)
        if xesbirro == "1":
            esbirro1.setX(posicion[0])        
            esbirro1.setY(posicion[1])
        else:
            esbirro2.setX(posicion[0])        
            esbirro2.setY(posicion[1])


        # filtrar no disponibles y ocupada

    def mostrar_estado(self):
        if self.is_esbirros_atrapan_reno():
            print("la huida de Rudolf ha fracasado y seguirá esclavizado cada navidad. Felicidades, Santa Claus!")
        elif self.reno_inconciente:
            print("Rudolf... Santa Claus te ha golpeado y has quedado inconciente. Tu huida ha fracasado")
        elif self.turno > self.rondas:
            print("Se han agotado los turnos y Rudolf ha escapado, arruinando así la navidad! Disfruta de tu libertad!")
        else:
            print(f"Todavía no hay ganador. Rondas restantes: {self.rondas -self.turno}")
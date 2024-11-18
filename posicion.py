class Posicion:
    x:0
    y:0
    alias =0
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def setX(self, x):
        self.x = x
        
    def setY(self, y):
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getPosicion(self):
        return [self.x,self.y]
    def __repr__(self): return f"Posicion(x={self.x}, y={self.y})"
    def getAliasEsbirro(self):
        if self.y == 0:
            if self.x ==1:
                return 0
            elif self.x ==2:
                return 1
            elif self.x ==3:
                return 2
        else:
            if self.x ==1:
                return 8
            elif self.x ==2:
                return 7
            elif self.x ==3:
                return 6
        if self.x ==0:
            if self.y ==1:
                return 11
            if self.y ==2:
                return 10
            if self.y ==3:
                return 9
        else:
            if self.y ==1:
                return 3
            if self.y ==2:
                return 4
            if self.y ==3:
                return 5
    def getAliasReno(self):
        if self.x<1 or self.x>3 or self.y<1 or self.y>3:
            return -1
        if self.y ==1:
            if self.x ==1:
                return 0
            if self.x ==2:
                return 1
            if self.x ==3:
                return 2
        elif self.y==2:
            if self.x ==1:
                return 3
            if self.x ==2:
                return 4
            if self.x ==3:
                return 5
        else:
            if self.x ==1:
                return 6
            if self.x ==2:
                return 7
            if self.x ==3:
                return 8
            
            
            
            
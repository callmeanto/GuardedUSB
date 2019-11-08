txt=" "
cont=0

def incrementarContador():
    global cont
    cont +=1
    return "%d" %cont


class TerminalNode:
    def __init__(self,name,tk):
        self.name = name
        self.tk = tk

    def imprimir(self,ident):
        print (ident+self.tk+": "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

# Clase Node, nada simbolo de la gramatica es considerado un nodo
class NoTerminalNode:

    # Constructor de la clase
    def __init__(self, sons=None, name=None):
        self.name = name
        self.sons = sons

    # Metodo para imprimir la gramatica
    def imprimir(self, ident):
        print(ident+"Node: "+self.name)
        
        for i in range(len(self.sons)):
            if(self.sons[i] == None):
                continue
            self.sons[i].imprimir(" "+ident)

    # Metodo para traducir simbolo no terminal o terminal en el arbol    
    def traducir(self):
        global txt
        id = incrementarContador()

        
        txt += id + "[label= "+self.name+"]"+"\n\t"

        for i in range(len(self.sons)):
            txt += id+"->"+self.sons[i].traducir()+"\n\t"

        return id

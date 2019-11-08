class Node:
    def __init__(self, sons=None, name=None):
        self.name = name
        self.sons = sons

    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        
        for index, son in enumerate(self.sons):
            if(son.sons == None):
                break
            son.imprimir(" "+ident)
    """
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"

        txt += id+"->"+son1+"\n\t"
        txt += id+"->"+son2+"\n\t"
        txt += id+"->"+son3+"\n\t"

        return id
    """
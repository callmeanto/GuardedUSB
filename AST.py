# GuardedUSB Interpreter
# Segunda etapa: Analizador Sintactico
# Lenguaje de implementacion del Interprete: Python 3
# Autores: Carlos Gonzalez y Antonella Requena
# Carnets: 15-10611 15-11196
# Fecha ultimo update: 10/11/2019
# Descripcion: Este archivo contiene las clases que sirven para construir el arbol abstracto


# Inicializamos contadores
txt=" "
cont=0

# Funcion para aumentar la identacion en el arbol
def incrementarContador():
    global cont
    cont +=1
    return "%d" %cont

# Clase para nodo lambda
class Null():
    def __init__(self):
        self.type = 'void'

    def imprimir(self,ident):
        pass

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id+"[label= "+"nodo_nulo"+"]"+"\n\t"

        return id

# Nodo root
class program():
    def __init__(self,son1,nombre):
        self.nombre = nombre
        self.son1  = son1

    def imprimir(self,ident):

        self.son1.imprimir(" "+ident)

    def traducir(self):
        global txt
        id=incrementarContador()
        son1=self.son1.traducir()
        txt+= id + "[label= "+self.nombre+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"

        return "digraph G {\n\t"+txt+"}"


# Clase Node, cada simbolo de la gramatica es considerado un nodo
# Cada nodo posee un metodo para ser impreso
# y un metodo para ser traducido al formato vz
class Node():

    # Constructor de la clase
    def __init__(self, sons=None, name=None):
        self.name = name
        self.sons = sons

    # Metodo para imprimir la gramatica
    def imprimir(self, ident):
        if(self.name != None):
            print(ident+self.name)

        if(self.sons != None):
            for i in range(len(self.sons)):
                if(self.sons[i] == None):
                    continue
                self.sons[i].imprimir(" "+ident)

    # Metodo para traducir simbolo no terminal o terminal en el arbol
    def traducir(self):
        global txt
        id = incrementarContador()

        if(self.name != None):
            txt += id + "[label= "+self.name+"]"+"\n\t"

        if (self.sons != None):
            for i in range(len(self.sons)):
                txt += id+"->"+self.sons[i].traducir()+"\n\t"

        return id

# Clase especial unicamente para simbolos terminales que
# se imprimen, como los Id, Literales y strings 
class Token():
    def __init__(self, token=None, label=None):
        self.token = token
        self.label = label

    def imprimir(self, ident):
        if self.token != None:
            print(ident+self.label+": "+self.token)
        else: 
            print(ident+self.label)

    def traducir(self):
        global txt
        id = incrementarContador()
        if(self.token != None):
            txt += id + "[label= \""+self.token+"\"]"+"\n\t"

        return id
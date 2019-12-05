import sys


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
    def __init__(self, sons=None, name=None,type=None):
        self.name = name
        self.sons = sons
        self.type = type 

    # Metodo para imprimir la gramatica
    def imprimir(self, ident):

        if (self.name == "Declare"):
            self.sons[-1].printTable()

        else:
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
    def __init__(self, token=None, name=None,type=None):
        self.token = token
        self.name = name
        self.type = type

    def imprimir(self, ident):
        if self.token != None:
            print(ident+self.name+": "+self.token)
        else: 
            print(ident+self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        if(self.token != None):
            txt += id + "[label= \""+self.token+"\"]"+"\n\t"

        return id



# Metodo para recorrer el arbol hasta llegar a una hoja
def get_children2(t):
    children = []
    # Si es una hoja
    if isinstance(t,Token):
        children.append(t.token)
    else:
        while(len(t.sons)>1):
            children.append(t.sons[0].token)
            t = t.sons[1]

        children.append(t.sons[0].token)    
        return children

children = []
def get_children(t,first):
    global children
    array = []
    if first and children != []: children = []
    
    if isinstance(t.sons[0],Token) and t.sons[0].token != 'array':
        children.append(t.sons[0].token)

    elif not isinstance(t.sons[0],Token) and (len(t.sons)>1):
        for i in range(len(t.sons)):
            # Si el nodo es de tipo array
            # hay que agregar a la lista los limites superiores
            # e inferiores
            if(t.sons[i].type == 'array'):
                array.append(t.sons[i].sons[0].token)
                array.append(t.sons[i].sons[1].sons[0].token)
                array.append(t.sons[i].sons[2].sons[0].token)
                children.append(array)
            get_children(t.sons[i],False)

    # Ultimo nodo
    elif len(t.sons)==1:
        if t.sons[0].sons[0].token == 'array':
            array.append(t.sons[0].sons[0].token)
            array.append(t.sons[0].sons[1].sons[0].token)
            array.append(t.sons[0].sons[2].sons[0].token)
            children.append(array)
        else:    
            children.append(t.sons[0].sons[0].token)
    return children


# Metodo para contar cantidad de hojas en el sub arbol sintactico
# Metodo auxiliar para saber cuantos nodos terminales
# hay en una derivacion
count = 0
def leaf_count(t,first):
    global count
    if first and count != 0: count = 0
    for son in t.sons:
        if isinstance(son,Token) and ((son.name == "Literal" and son.type != 'int') or (son.name == "Ident") or (son.name == "String")):
            print("Error: los arreglos deben ser de tipo entero")
            sys.exit()
        if isinstance(son,Token):
            # llegamos a una hoja
            count += 1            
        else:
            # hay que seguir recorriendo
            leaf_count(son,False)
    return count

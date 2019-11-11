txt=" "
cont=0

def incrementarContador():
	global cont
	cont +=1
	return "%d" %cont

class Nodo():
	pass

class Null(Nodo):
	def __init__(self):
		self.type = 'void'

	def imprimir(self,ident):
		print (ident + "nodo nulo")

	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id+"[label= "+"nodo_nulo"+"]"+"\n\t"

		return id

class program(Nodo):
	def __init__(self,son1,nombre):
		self.nombre = nombre
		self.son1  = son1

	def imprimir(self,ident):

		print (ident+"Nodo: "+self.nombre)
		self.son1.imprimir(" "+ident)

	def traducir(self):
		global txt
		id=incrementarContador()
		son1=self.son1.traducir()
		txt+= id + "[label= "+self.nombre+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"

		return "digraph G {\n\t"+txt+"}"


# Clase Node, nada simbolo de la gramatica es considerado un nodo
class Node(Nodo):

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


class Token(Nodo):
    def __init__(self, name, tk):
        self.name = name
        self.tk = tk

    def imprimir(self, ident):
        print(ident+self.tk+": "+self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id



###############################################################
###############################################################

class Comma(Nodo):

	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "Comma: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class Semicolon(Nodo):

	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "Semicolon: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class TwoPoints(Nodo):

	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "TwoPoints: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id
class Assignment(Nodo):

	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "Asig: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class array(Nodo):
	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "Array: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id


class Id(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"ID: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= "+self.name+"]"+"\n\t"

		return id

class Number(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Number: "+str(self.name))
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= "+str(self.name)+"]"+"\n\t"

		return id


class Plus(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Plus: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class Mult(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Times: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class Minus(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Minus: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class Div(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Divide: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class TkOBlock(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Oblock: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class TkCBlock(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Cblock: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CArrow(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Arrow: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CIf(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"If: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id


class CFi(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Fi: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CFor(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"For: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id
class CRof(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Rof: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CTo(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"If: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CGuard(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Guard: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CLess(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Less: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id
class CGreater(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Greater: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CLeq(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Leq: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CGeq(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Geq: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CEqual(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Equal: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CNEqual(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"NEqual: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class CAnd(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"And: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class COr(Nodo):
	def __init__(self,name):
		self.name = name

	def imprimir(self,ident):
		print (ident+"Or: "+self.name)
			
	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class COBracket(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"OBracket: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CCBracket(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"CBracket: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CSoForth(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"CSoForth: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CIn(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"In: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CMax(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Max: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CMin(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Min: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CAtoi(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Atoi: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CDo(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Do: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class COd(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Od: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CConcat(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"Concat: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CTrue(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"True: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CFalse(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"False: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class CString(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        print (ident+"String: "+self.name)
            
    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id
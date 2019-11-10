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



class bloque(Nodo):
	def __init__(self, son1, son2, son3, name):
		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3

	def imprimir(self, ident):
		print (ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)

		
	def traducir(self):
		global txt
		id = incrementarContador()

		son1=self.son1.traducir()
		son2=self.son2.traducir()
		son3=self.son3.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		txt+= id+"->"+son2+"\n\t"
		txt+= id+"->"+son3+"\n\t"

		return id

class t(Nodo):
	def __init__(self, son1, name):
		self.name = name
		self.son1=son1
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

	def traducir(self):
		global txt
		id=incrementarContador()
		son1=self.son1.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		return id

class t2(Nodo):
    def __init__(self, son1, son2,name):
        self.name = name
        self.son1=son1
        self.son2=son2
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)

    def traducir(self):
        global txt
        id=incrementarContador()
        son1=self.son1.traducir()
        son2=self.son2.traducir()

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        return id

class casoInstrucciones1(Nodo):
    def __init__(self,  son1, name):
        self.name = name
        self.son1=son1
        
        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
       

    def traducir(self):
        global txt
        id=incrementarContador()
        son1=self.son1.traducir()
    

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
      
        return id

class casoInstrucciones2(Nodo):
    def __init__(self,  son1,son2,son3,name):
        self.name = name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        
        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
       

    def traducir(self):
        global txt
        id=incrementarContador()
        son1=self.son1.traducir()
        son2=self.son2.traducir()
        son3=self.son3.traducir()
    

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
      
        return id

class declaracionVariables(Nodo):
	def __init__(self,  son1, son2, name):
		self.name = name
		self.son1=son1
		self.son2=son2
		
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		if type(self.son2)==type(tuple()):
			self.son2[0].imprimir(" "+ident)
		else:
			self.son2.imprimir(" "+ident)

	def traducir(self):
		global txt
		id=incrementarContador()
		son1=self.son1.traducir()
		if type(self.son2)==type(tuple()):
			son2=self.son2[0].traducir()
		else:
			
			son2=self.son2.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		txt+= id+"->"+son2+"\n\t"
		return id

class declaracion1(Nodo):
	def __init__(self, son1,son2,son3,son4,son5, name):
		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		self.son4=son4
		self.son5=son5
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		if(type(self.son1) == type(tuple())):
			self.son1[0].imprimir(" "+ident)
		else:
			self.son1.imprimir(" "+ident)
		if(type(self.son2) == type(tuple())):
			self.son2[0].imprimir(" "+ident)
		else:
			self.son2.imprimir(" "+ident)

		self.son3.imprimir(" "+ident)
		self.son4.imprimir(" "+ident)
		self.son5.imprimir(" "+ident)
	def traducir(self):
		global txt
		id = incrementarContador()

		if type(self.son1) == type(tuple()):
			son1 = self.son1[0].traducir()
		else:
			son1 = self.son1.traducir()

		if type(self.son2) == type(tuple()):
			son2 = self.son2[0].traducir()
		else:
			son2 = self.son2.traducir()

		son3=self.son3.traducir()
		son4=self.son4.traducir()
		son5=self.son5.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		txt+= id+"->"+son2+"\n\t"
		txt+= id+"->"+son3+"\n\t"
		txt+= id+"->"+son4+"\n\t"
		txt+= id+"->"+son5+"\n\t"
		return id

class declaracion2(Nodo):
	def __init__(self, son1,son2,son3, name):
		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		
		
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		if(type(self.son1) == type(tuple())):
			self.son1[0].imprimir(" "+ident)
		else:
			self.son1.imprimir(" "+ident)
		if(type(self.son2) == type(tuple())):
			self.son2[0].imprimir(" "+ident)
		else:
			self.son2.imprimir(" "+ident)

		self.son3.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id = incrementarContador()

		if type(self.son1) == type(tuple()):
			son1 = self.son1[0].traducir()
		else:
			son1 = self.son1.traducir()

		if type(self.son2) == type(tuple()):
			son2 = self.son2[0].traducir()
		else:
			son2 = self.son2.traducir()

		son3=self.son3.traducir()
	
		
		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		txt+= id+"->"+son2+"\n\t"
		txt+= id+"->"+son3+"\n\t"
		
	
		return id

class declaracion3(Nodo):
    def __init__(self, son1,son2,son3, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        
        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)
        if(type(self.son2) == type(tuple())):
            self.son2[0].imprimir(" "+ident)
        else:
            self.son2.imprimir(" "+ident)

        self.son3.imprimir(" "+ident)
        
        
    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        if type(self.son2) == type(tuple()):
            son2 = self.son2[0].traducir()
        else:
            son2 = self.son2.traducir()

        son3=self.son3.traducir()
    
        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
        
    
        return id

class listaInstrucciones1(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
	def traducir(self):
		global txt
		id=incrementarContador()

		
		son1=self.son1.traducir()
		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
	

		return id

class declaracionSemicolon1(Nodo):
    def __init__(self, son1,son2,son3, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        son1=self.son2.traducir()
        son1=self.son3.traducir()
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
        txt += id +"->"+son2+"\n\t"
        txt += id +"->"+son3+"\n\t"
    

        return id
class declaracionSemicolon2(Nodo):
    def __init__(self, son1, name):
        self.name=name
        self.son1=son1
        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
       
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
       
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
       

        return id

class listaInstruccionesAsig(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
	def traducir(self):
		global txt
		id=incrementarContador()

		
		son1=self.son1.traducir()
		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
	

		return id

class listaInstruccionesFor(Nodo):
    def __init__(self, son1, name):
        self.name=name
        self.son1=son1
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
    

        return id

class instruccionFor(Nodo):
    def __init__(self, son1,son2,son3,son4,son5,son6,son7,son8,son9, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4
        self.son5=son5
        self.son6=son6
        self.son7=son7
        self.son8=son8
        self.son9=son9
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        self.son4.imprimir(" "+ident)
        self.son5.imprimir(" "+ident)
        self.son6.imprimir(" "+ident)
        self.son7.imprimir(" "+ident)
        self.son8.imprimir(" "+ident)
        self.son9.imprimir(" "+ident)
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        son2=self.son2.traducir()
        son3=self.son3.traducir()
        son4=self.son4.traducir()
        son5=self.son5.traducir()
        son6=self.son6.traducir()
        son7=self.son7.traducir()
        son8=self.son8.traducir()
        son9=self.son9.traducir()
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        
        txt += id +"->"+son1+"\n\t"
        txt += id +"->"+son2+"\n\t"
        txt += id +"->"+son3+"\n\t"
        txt += id +"->"+son4+"\n\t"
        txt += id +"->"+son5+"\n\t"
        txt += id +"->"+son6+"\n\t"
        txt += id +"->"+son7+"\n\t"
        txt += id +"->"+son8+"\n\t"
        txt += id +"->"+son9+"\n\t"
    

        return id

class instruccionDo(Nodo):
    def __init__(self, son1,son2,son3,son4,son5, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4
        self.son5=son5
        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        self.son4.imprimir(" "+ident)
        self.son5.imprimir(" "+ident)
        
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        son2=self.son2.traducir()
        son3=self.son3.traducir()
        son4=self.son4.traducir()
        son5=self.son5.traducir()
        
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        
        txt += id +"->"+son1+"\n\t"
        txt += id +"->"+son2+"\n\t"
        txt += id +"->"+son3+"\n\t"
        txt += id +"->"+son4+"\n\t"
        txt += id +"->"+son5+"\n\t"
       
        return id

class listaInstruccionesRead(Nodo):
    def __init__(self, son1, name):
        self.name=name
        self.son1=son1
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
    

        return id

class listaInstruccionesPrint(Nodo):
    def __init__(self, son1, name):
        self.name=name
        self.son1=son1
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
    

        return id

class listaInstruccionesPrintln(Nodo):
    def __init__(self, son1, name):
        self.name=name
        self.son1=son1
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
    def traducir(self):
        global txt
        id=incrementarContador()

        
        son1=self.son1.traducir()
        
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
    

        return id

class asignacionVariables(Nodo):
    def __init__(self,  son1, name):
        self.name = name
        self.son1=son1
        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)

        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

    def traducir(self):
        global txt
        id=incrementarContador()
        
        if type(self.son1)==type(tuple()):
            son1=self.son1[0].traducir()
        else:
            son1=self.son1.traducir()

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        return id

class asignacion1(Nodo):
    def __init__(self, son1,son2,son3,son4,son5, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4
        self.son5=son5

        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        self.son4.imprimir(" "+ident)


        if(type(self.son5) == type(tuple())):
            self.son5[0].imprimir(" "+ident)
        else:
            self.son5.imprimir(" "+ident)

    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        son2=self.son2.traducir()
        son3=self.son3.traducir()
        son4=self.son4.traducir()


        if type(self.son5) == type(tuple()):
            son5 = self.son5[0].traducir()
        else:
            son5 = self.son5.traducir()

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        
        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
        txt+= id+"->"+son4+"\n\t"
        txt+= id+"->"+son5+"\n\t"
        return id

class asignacion2(Nodo):
    def __init__(self, son1,son2,son3, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)
        
        self.son2.imprimir(" "+ident)

        if(type(self.son3) == type(tuple())):
            self.son3[0].imprimir(" "+ident)
        else:
            self.son3.imprimir(" "+ident)

        
    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        son2=self.son2.traducir()

        if type(self.son3) == type(tuple()):
            son3 = self.son3[0].traducir()
        else:
            son3 = self.son3.traducir()

        
        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
        
        return id

class readVariables(Nodo):
    def __init__(self,  son1, name):
        self.name = name
        self.son1=son1
        
    def imprimir(self, ident):
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

    def traducir(self):
        global txt
        id=incrementarContador()
        son1=self.son1.traducir()
        if type(self.son1)==type(tuple()):
            son1=self.son1[0].traducir()
        else:
            son1=self.son1.traducir()

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        return id

class read1(Nodo):
    def __init__(self, son1,son2,son3,son4, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4

        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        self.son4.imprimir(" "+ident)
        
    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        son2=self.son2.traducir()
        son3=self.son3.traducir()
        son4=self.son4.traducir()
        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        
        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
        txt+= id+"->"+son4+"\n\t"

    
        return id

class read2(Nodo):
    def __init__(self, son1,son2, name):
        self.name=name
        self.son1=son1
        self.son2=son2
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        
        son1=self.son1.traducir()
        son2=self.son2.traducir()

        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"

        
        return id

class printExpression(Nodo):
    def __init__(self,  son1, name):
        self.name = name
        self.son1=son1
        
    def imprimir(self, ident):
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

    def traducir(self):
        global txt
        id=incrementarContador()
        if type(self.son1)==type(tuple()):
            son1=self.son1[0].traducir()
        else:
            son1=self.son1.traducir()

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        return id

class print1(Nodo):
    def __init__(self, son1,son2,son3,son4, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4

        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        
        if(type(self.son4) == type(tuple())):
            self.son4[0].imprimir(" "+ident)
        else:
            self.son4.imprimir(" "+ident)

    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        son2=self.son2.traducir()
        son3=self.son3.traducir()
        
        if type(self.son4) == type(tuple()):
            son4 = self.son4[0].traducir()
        else:
            son4 = self.son4.traducir()

        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        
        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
        txt+= id+"->"+son4+"\n\t"

    
        return id

class print2(Nodo):
    def __init__(self, son1,son2, name):
        self.name=name
        self.son1=son1
        self.son2=son2
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        
        self.son1.imprimir(" "+ident)
        if(type(self.son2) == type(tuple())):
            self.son2[0].imprimir(" "+ident)
        else:
            self.son2.imprimir(" "+ident)

    def traducir(self):
        global txt
        id = incrementarContador()
        
        son1=self.son1.traducir()
        
        if type(self.son2) == type(tuple()):
            son2 = self.son2[0].traducir()
        else:
            son2 = self.son2.traducir()

        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"

        
        return id

class concatPrint(Nodo):
    def __init__(self, son1,son2,son3, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        
        self.son1.imprimir(" "+ident)
        if(type(self.son2) == type(tuple())):
            self.son2[0].imprimir(" "+ident)
        else:
            self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)

    def traducir(self):
        global txt
        id = incrementarContador()
        
        son1=self.son1.traducir()
        
        if type(self.son2) == type(tuple()):
            son2 = self.son2[0].traducir()
        else:
            son2 = self.son2.traducir()
        son3=self.son3.traducir()

        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"

        
        return id

class concatPrint2(Nodo):
    def __init__(self, son1, name):
        self.name=name
        self.son1=son1
       
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        
        self.son1.imprimir(" "+ident)
        

    def traducir(self):
        global txt
        id = incrementarContador()
        
        son1=self.son1.traducir()
        
       
        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
      

        
        return id

class printlnExpression(Nodo):
    def __init__(self,  son1, name):
        self.name = name
        self.son1=son1
        
    def imprimir(self, ident):
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

    def traducir(self):
        global txt
        id=incrementarContador()
        son1=self.son1.traducir()
        if type(self.son1)==type(tuple()):
            son1=self.son1[0].traducir()
        else:
            son1=self.son1.traducir()

        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        return id

class println1(Nodo):
    def __init__(self, son1,son2,son3,son4, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4

        
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        if(type(self.son1) == type(tuple())):
            self.son1[0].imprimir(" "+ident)
        else:
            self.son1.imprimir(" "+ident)

        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        
        if(type(self.son4) == type(tuple())):
            self.son4[0].imprimir(" "+ident)
        else:
            self.son4.imprimir(" "+ident)

    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        son2=self.son2.traducir()
        son3=self.son3.traducir()
        
        if type(self.son4) == type(tuple()):
            son4 = self.son4[0].traducir()
        else:
            son4 = self.son4.traducir()

        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        
        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"
        txt+= id+"->"+son3+"\n\t"
        txt+= id+"->"+son4+"\n\t"

    
        return id

class println2(Nodo):
    def __init__(self, son1,son2, name):
        self.name=name
        self.son1=son1
        self.son2=son2
    def imprimir(self, ident):
        print(ident+"Nodo: "+self.name)
        
        self.son1.imprimir(" "+ident)
        if(type(self.son2) == type(tuple())):
            self.son2[0].imprimir(" "+ident)
        else:
            self.son2.imprimir(" "+ident)

    def traducir(self):
        global txt
        id = incrementarContador()
        
        son1=self.son1.traducir()
        
        if type(self.son2) == type(tuple()):
            son2 = self.son2[0].traducir()
        else:
            son2 = self.son2.traducir()

        
        txt+= id + "[label= "+self.name+"]"+"\n\t"

        txt+= id+"->"+son1+"\n\t"
        txt+= id+"->"+son2+"\n\t"

        
        return id

class listaInstruccionesIf(Nodo):
	def __init__(self, son1, name):

		self.name=name
		self.son1=son1

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"		

		return id

class instruccionIf1(Nodo):
	def __init__(self, son1,son2,son3,son4,son5,son6,name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		self.son4=son4
		self.son5=son5
		self.son6=son6
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		self.son4.imprimir(" "+ident)
		self.son5.imprimir(" "+ident)
		self.son6.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	
		son2=self.son2.traducir()
		son3=self.son3.traducir()
		son4=self.son4.traducir()
		son5=self.son5.traducir()
		son6=self.son6.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"		
		txt += id +"->"+son2+"\n\t"	
		txt += id +"->"+son3+"\n\t"	
		txt += id +"->"+son4+"\n\t"	
		txt += id +"->"+son5+"\n\t"	
		txt += id +"->"+son6+"\n\t"	
			

		return id 
class instruccionIf2(Nodo):
	def __init__(self, son1,son2,son3,son4,son5,son6,name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		self.son4=son4
		self.son5=son5
		self.son6=son6
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		self.son4.imprimir(" "+ident)
		self.son5.imprimir(" "+ident)
		self.son6.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	
		son2=self.son2.traducir()
		son3=self.son3.traducir()
		son4=self.son4.traducir()
		son5=self.son5.traducir()
		son6=self.son6.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"		
		txt += id +"->"+son2+"\n\t"	
		txt += id +"->"+son3+"\n\t"	
		txt += id +"->"+son4+"\n\t"	
		txt += id +"->"+son5+"\n\t"	
		txt += id +"->"+son6+"\n\t"	
		

		return id

class variasGuardias1(Nodo):
	def __init__(self, son1,son2,son3,son4,son5,name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		self.son4=son4
		self.son5=son5
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		self.son4.imprimir(" "+ident)
		self.son5.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	
		son2=self.son2.traducir()
		son3=self.son3.traducir()
		son4=self.son4.traducir()
		son5=self.son5.traducir()
	

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"		
		txt += id +"->"+son2+"\n\t"	
		txt += id +"->"+son3+"\n\t"	
		txt += id +"->"+son4+"\n\t"	
		txt += id +"->"+son5+"\n\t"	
		

		return id

class variasGuardias2(Nodo):
	def __init__(self, son1,son2,son3,son4,son5,name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		self.son4=son4
		self.son5=son5
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		self.son4.imprimir(" "+ident)
		self.son5.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	
		son2=self.son2.traducir()
		son3=self.son3.traducir()
		son4=self.son4.traducir()
		son5=self.son5.traducir()
	

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"		
		txt += id +"->"+son2+"\n\t"	
		txt += id +"->"+son3+"\n\t"	
		txt += id +"->"+son4+"\n\t"	
		txt += id +"->"+son5+"\n\t"	
		

		return id
class condicion1(Nodo):
	def __init__(self, son1,name):

		self.name=name
		self.son1=son1
		
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	
		
	

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"		
	

		return id
class condicion2(Nodo):
	def __init__(self, son1,son2,son3,name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	

		son2=self.son2.traducir()	
		son3=self.son3.traducir()	
		
	

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"	
		txt += id +"->"+son2+"\n\t"		
		txt += id +"->"+son3+"\n\t"		
	

		return id

class condicion3(Nodo):
	def __init__(self, son1,son2,son3,name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	

		son2=self.son2.traducir()
		son3=self.son3.traducir()		
		
	

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"	
		txt += id +"->"+son2+"\n\t"		
		txt += id +"->"+son3+"\n\t"	
	

		return id

class condicion4(Nodo):
	def __init__(self, son1,son2,son3,son4,son5, name):

		self.name=name
		self.son1=son1
		self.son2=son2
		self.son3=son3
		self.son4=son4
		self.son5=son5
		
		

	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		self.son4.imprimir(" "+ident)
		self.son5.imprimir(" "+ident)
		
		

	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()	

		son2=self.son2.traducir()
		son3=self.son3.traducir()	
		son4=self.son4.traducir()
		son5=self.son5.traducir()	
		
	

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"	
		txt += id +"->"+son2+"\n\t"		
		txt += id +"->"+son3+"\n\t"	
		txt += id +"->"+son4+"\n\t"	
		txt += id +"->"+son5+"\n\t"	
	

		return id

class operadorBool1(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class operadorBool2(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class tipoExpression(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class relation1(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class relation2(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class relation3(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class relation4(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class relation5(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class relation6(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):

		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class declare(Nodo):
	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident+"Nodo: "+self.name)
		print(ident + "Declare: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

class Read(Nodo):
    def __init__(self, name):
        self.name=name
    def imprimir(self,ident):
        print(ident + "Read: "+self.name)
    def traducir(self):
        global txt
        id = incrementarContador()
        
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id


class Print(Nodo):
    def __init__(self, name):
        self.name=name
    def imprimir(self,ident):
        print(ident + "Print: "+self.name)
    def traducir(self):
        global txt
        id = incrementarContador()
        
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id


class Println(Nodo):
    def __init__(self, name):
        self.name=name
    def imprimir(self,ident):
        print(ident + "Println: "+self.name)
    def traducir(self):
        global txt
        id = incrementarContador()
        
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id



class tipo1(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)

		
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
		
		return id

class tipo2(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1=son1
		
	def imprimir(self, ident):
		
		self.son1.imprimir(" "+ident)
		
		
	def traducir(self):
		global txt
		id=incrementarContador()

		son1=self.son1.traducir()
		

		
		txt += id +"[label= "+self.name+"]"+"\n\t"
		txt += id +"->"+son1+"\n\t"
	

		return id

class tipo3(Nodo):
    def __init__(self, son1, son2, son3, son4, son5, son6, name):
        self.name=name
        self.son1=son1
        self.son2=son2
        self.son3=son3
        self.son4=son4
        self.son5=son5
        self.son6=son6
        

        
    def imprimir(self, ident):
        
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        self.son4.imprimir(" "+ident)
        self.son5.imprimir(" "+ident)
        self.son6.imprimir(" "+ident)
        
        
    def traducir(self):
        global txt
        id=incrementarContador()

        son1=self.son1.traducir()
        son2=self.son2.traducir()
        son3=self.son3.traducir()
        son4=self.son4.traducir()
        son5=self.son5.traducir()
        son6=self.son6.traducir()
                
        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
        txt += id +"->"+son2+"\n\t"
        txt += id +"->"+son3+"\n\t"
        txt += id +"->"+son4+"\n\t"
        txt += id +"->"+son5+"\n\t"
        txt += id +"->"+son6+"\n\t"
        

        return id

class tipoInt(Nodo):
	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "Int: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id
class booleano(Nodo):
	def __init__(self, name):
		self.name=name
	def imprimir(self,ident):
		print(ident + "Bool: "+self.name)
	def traducir(self):
		global txt
		id = incrementarContador()
		
		txt += id + "[label= \""+self.name+"\"]"+"\n\t"

		return id

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

class expression1(Nodo):
	def __init__(self, son1, name):
		self.name=name
		self.son1= son1
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()
		son1=self.son1.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		return id

class expression2(Nodo):
	def __init__(self, son1, son2, name):
		self.name=name
		self.son1= son1
		self.son2= son2
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()
		son1=self.son1.traducir()
		son2=self.son2.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		txt+= id+"->"+son2+"\n\t"


		return id


class expression3(Nodo):
	def __init__(self, son1, son2, son3, name):
		self.name=name
		self.son1= son1
		self.son2= son2
		self.son3= son3
	def imprimir(self, ident):
		print(ident+"Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)
		

	def traducir(self):
		global txt
		id=incrementarContador()
		son1=self.son1.traducir()
		son2=self.son2.traducir()
		son3=self.son3.traducir()

		txt+= id + "[label= "+self.name+"]"+"\n\t"

		txt+= id+"->"+son1+"\n\t"
		txt+= id+"->"+son2+"\n\t"
		txt+= id+"->"+son3+"\n\t"


		return id

class addingOperator1(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):

		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class addingOperator2(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):
		print (ident + "Nodo: "+self.name)
			
		self.son1.imprimir(" "+ident)

		
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class term1(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):
		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

		
			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class term2(Nodo):
	def __init__(self,son1,son2,son3,name):
		self.name = name
		self.son1 = son1
		self.son2 = son2
		self.son3 = son3

	def imprimir(self,ident):

		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)
		self.son3.imprimir(" "+ident)


	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()
		son2 = self.son2.traducir()
		son3 = self.son3.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"
		txt += id + " -> " + son2 + "\n\t"
		txt += id + " -> " + son3 + "\n\t"

		return id

class multiplyingOperator1(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):
		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

		
			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class multiplyingOperator2(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):
		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

		
			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class Id1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class Id2(Nodo):
    def __init__(self,son1,son2,name):
        self.name = name
        self.son1 = son1
        self.son2=son2

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"


        return id


class factor1(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):

		print (ident + "Nodo: "+self.name)
			
		self.son1.imprimir(" "+ident)

		
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class factor2(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):

		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class factor3(Nodo):
	def __init__(self,son1,name):
		self.name = name
		self.son1 = son1

	def imprimir(self,ident):
		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)

	
			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"

		return id

class factor4(Nodo):
	def __init__(self,son1,son2,name):
		self.name = name
		self.son1 = son1
		self.son2 = son2

	def imprimir(self,ident):

		print (ident + "Nodo: "+self.name)
		self.son1.imprimir(" "+ident)
		self.son2.imprimir(" "+ident)

		
			
	def traducir(self):
		global txt
		id = incrementarContador()

		son1 = self.son1.traducir()
		son2= self.son2.traducir()

		txt += id + "[label= "+self.name+"]"+"\n\t"
		txt += id + " -> " + son1 + "\n\t"
		txt += id + " -> " + son2 + "\n\t"


		return id

class factor5(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor6(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor7(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor8(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor9(Nodo):
    def __init__(self,son1,son2,son3,son4,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
        self.son4 = son4

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)
        self.son3.imprimir(" "+ident)
        self.son4.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()
        son4 = self.son4.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"
        txt += id + " -> " + son4 + "\n\t"


        return id


class embed1(Nodo):
    def __init__(self,son1, son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"


        return id

class embed2(Nodo):
    def __init__(self,son1, son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"


        return id

class embed3(Nodo):
    def __init__(self,son1, son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self,ident):

        print (ident + "Nodo: "+self.name)
        self.son1.imprimir(" "+ident)
        self.son2.imprimir(" "+ident)

            
    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"


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
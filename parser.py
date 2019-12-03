import ply.yacc as yacc
import os
import codecs
import re

from lexer import tokens
import sys
import os.path
from AST import *
from sym_table import *

# GuardedUSB Interpreter
# Segunda etapa: Analizador Sintactico
# Lenguaje de implementacion del Interprete: Python 3
# Autores: Carlos Gonzalez y Antonella Requena
# Carnets: 15-10611 15-11196
# Fecha ultimo update: 10/11/2019
# Descripcion: se implemento un lexer utilizando la libreria .ply de python, el siguiente programa recibe un archivo y retorna la lista de "tokens"
# o elementos atomicos del lenguaje si pertenecen, o da un mensaje de error si
# encuentra un caracter que no pertenece al lenguaje. Asi mismo, indica la posicion en donde se encuentra.


# Inicializamos las estructuras a utilizar 
# para chequeo de semantica



# Utilizamos una pila para las tablas de simbolos
stack_table = TableStack()

# Utilizamos una pila para los iteradores
stack_iterator = TableStack()


#######################################
###### CONSTRUCCION DE LA GRAMATICA ###
#######################################


# Funcion que describe la regla gramatical para la instruccion programa
# esta instruccion es la principal y deriva a bloque
def p_program(p):
    ''' program : bloque '''
    p[0] = program(p[1],"program")

# Funcion que describe la regla gramatical para la instruccion bloque
# Un bloque es todo aquello que este definido entre los brackets
# Esta produccion deriva a t que es el contenido del programa / subprograma
def p_bloque(p):
    '''bloque : TkOBlock t TkCBlock'''
    p[0] = Node([p[2]],None)

    stack_table.pop()
    
# Funcion que describe la regla gramatical que genera el contenido del programa
# deriva en declaracion de variables + conjunto de secuenciacion de instrucciones
# o solo conjunto de instrucciones
def p_t(p):
    '''
    t : casoInstrucciones
      | TkDeclare declaracionVariables casoInstrucciones
    '''
    # Caso en que hay declaraciones y luego secuenciacion de instrucciones
    if len(p) == 4: 
        p[0] = Node([p[2],p[3]],None)
    # Caso en que solo hay secuenciacion de instrucciones
    else: 
        p[0] = Node([p[1]],None)
    

# Gramatica para declaracion de variables #
def p_declaracionVariables(p):
    '''declaracionVariables : listaDeclaraciones TkTwoPoints tipos TkSemicolon declaracionVariables
                            | listaDeclaraciones TkTwoPoints tipos
    '''
    aux_table = SymbolTable()

    # No Recursivo
    if len(p) == 4:
        p[0] = Node([p[1],p[3],aux_table],"Declare",None)

    # Recursivo
    else:
        p[0] = Node([p[1],p[3],p[5],aux_table],"Declare",None)
        p[0] = p[5]


    # Verificamos que no se esten asignando menos tipos a las variables
    children = get_children(p[3],True)
          
    if len(children) != len(get_children2(p[1])) and len(children) != 1 :
        print("Error de sintaxis: esta asignando menos tipos de los que ha declarado")
        sys.exit()

 

    for i in get_children2(p[1]):

        # Si la asignacion es de un solo tipo para todas las variables
        # duplicamos el tipo en el arreglo de tipos k veces
        # con k el numero de variables por comodidad de implementacion
        if len(children)==1:
            children = [children[0] for k in range(len( get_children2(p[1])))]
       
            
        type = children.pop(0)
        
        # Si el elemento al que deriva tipo es TkArray
        if type != 'int' and type != 'bool' :
            # Verificamos que las cotas esten correctas
            if type[1] > type[2] :
                print('Error: El limite inferior del arreglo ' + i +' debe ser menor que el superior')
                sys.exit()

            arr = []
            # Inicializamos el arreglo, calculamos la longitud del mismo
            arrlen = abs(type[2] - type[1]) + 1
            
            arr = [None for k in range(arrlen)]
        
            # Insertamos en la tabla el tipo con las cotas del arreglo y la longitud del arreglo
            # y los valores iniciales
            # este metodo ya verifica si la variable ha sido declarada
            aux_table.push_symbol(i, [type, arrlen],arr)

        else:
            aux_table.push_symbol(i, type)
    
    # Insertamos la tabla
    stack_table.push(aux_table)



# Gramatica para caso en que se tiene una lista de tipos separada por comas    
def p_tipos(p):
    """
    tipos : tipo TkComma tipos
          | tipo
    """
    if len(p) == 4:
        p[0] = Node([p[1], p[3]],"tipos",None)
    else:
        p[0] = Node([p[1]],None,None)

# Declaracion multiple de varios tipos en una misma linea de instruccion	
def p_listaDeclaraciones(p):
    '''listaDeclaraciones : TkId TkComma listaDeclaraciones
                          | TkId
    '''
    if len(p) == 2:
        p[0] = Node([Token(p[1],"Ident")])
    else:
        p[0] = Node([Token(p[1],"Ident"),p[3]])    
   

# Gramatica para asignacion de variables
def p_asignacion(p):
    '''asignacion : TkId TkAsig expresion
                  | TkId TkAsig listaExpresion
                  | TkId TkAsig asignacionArreglos
    '''
    p[0]= Node([Token(p[1],"Ident"), p[3]], "Asig")

    # p[0] = [p[1],p[3],"Asig"]

    
    value = stack_table.is_in_table(p[0].sons[0].token)
    # Verificamos que la variable a asignar ya fue declarada
    if value is False:
        print("La variable " + p[0].sons[0].token + " esta intentando ser asignada pero no fue declarada")
        sys.exit()

    # Verificamos el tipo de las variables
    # Es porque es de tipo arreglo con asignacion por lista
    try:
        if value[0][0][0] == 'array' and p[3].sons[0].name == 'listaExpresion':

            # Contemos la cantidad de elementos en listaExpresion
            count1 = leaf_count(p[3],True)
        
            # Si el length del arreglo es menor al length de la lista de expresiones
            if int(value[0][1]) < count1:
                print("Error: indice del arreglo '"+ p[0].sons[0].token +"' fuera del rango")
                sys.exit()

        else:
            # Es porque es de tipo bool o int
            # Primero verificamos que no se le esten asignando mas de una expresion a los tipos basicos
            if p[3].name == 'listaExpresion':
                print("Error: no puede asignarle a la variable '" + p[0].sons[0].token +"' mas de una expresion porque tiene un tipo de dato basico")
                sys.exit()
            
            if not(value[0] == p[3].sons[0].sons[0].type):
                print("Error: la variable '"+p[0].sons[0].token +"' es de tipo '"+ value[0] +"', no se le puede asignar algo de tipo '" + p[3].sons[0].sons[0].type +"'" )
                sys.exit()
    except: pass

# Gramatica para lista de expresiones a asignar en arreglos y variables
def p_listaExpresion(p):
    '''listaExpresion : listaExpresion TkComma expresion
                      | expresion
    '''
    if len(p) == 2:
        p[0] = Node([p[1]],None)
        
    else:
        p[0]= Node([p[1], p[3]], "listaExpresion")
        
# Gramatica para asignacion de arreglos
def p_asignacionArreglos(p):
    '''asignacionArreglos : TkId listaIndices posicionArreglo'''
    p[0] = Node([Token(p[1],"Ident"),p[2],p[3]],"ArrayAsig")
    
    # Verificamos que TkId sea de tipo array y este en alguna tabla de su scope
    value = stack_table.is_in_table(p[0].sons[0].token)
    if value == False:
        print("Error: Esta intentando asignar el arreglo '"+ p[0].sons[0].token +"' que no fue declarado")
        sys.exit()
    # Esta en la tabla pero no es de tipo array
    elif value[0] == 'int' or value[0] == 'bool':
        print("Error: la variable '"+p[0].sons[0].token+"' no es de tipo 'array'")
        sys.exit()

    # Esta en la tabla, es de tipo array pero no tiene nada asignado en el rango pedido o el rango es incorrecto
    # consultamos en la tabla de simbolos
    elif not (value[0][0][1]<= p[2].sons[0].sons.token <= value[0][0][2] ):
        print("Error: Esta intentando indexar una posicion no valida del arreglo '"+ p[0].sons[0].token+"'")
        sys.exit()
    

def p_listaIndices(p):
    '''listaIndices : listaIndices TkOpenPar number TkTwoPoints number TkClosePar
                    | TkOpenPar number TkTwoPoints number TkClosePar
    '''
    if len(p) == 7:
        p[0] = Node([p[1],p[3], p[5]],"ArrayAsig")
    else:
        p[0] = Node([p[2],p[4]],"ArrayAsig")
        

def p_posicionArreglo(p):
    '''posicionArreglo : TkOBracket TkNum TkCBracket
                       | empty
    '''
    if len(p) == 2:
        p[0] = Null()
    else:
        p[0] = Node([Token(str(p[2]),"Literal")],"EvalArray")


# Funcion que describe la regla gramatical que genera una instruccion
# una instruccion puede ser una secuencia de instrucciones o una sola instruccion
# deriva en los tipos de instrucciones definidos para el lenguaje
def p_casoInstrucciones(p):
    '''casoInstrucciones : Instruccion
                         | casoInstrucciones TkSemicolon Instruccion
    '''
    # Caso en que solo hay una instruccion
    if len(p)==2:
        p[0]=Node([p[1]], None)
    # Caso recursivo
    else: 
        p[0]=Node([p[1], p[3]], None)


###########################################
##### PRODUCCIONES PARA INSTRUCCIONES #####
###########################################

# Funcion que describe la regla gramatical que deriva los diferentes tipos de instrucciones
def p_Instruccion(p):
    '''
    Instruccion : If
                | For
                | Do
                | singleInstruccion
    
    '''

    p[0]=Node([p[1]],"Sequencing")

# Instrucciones de una sola linea
def p_singleInstruccion(p):
    '''
    singleInstruccion : asignacion
                      | read
                      | print
    '''
    p[0]=Node([p[1]],"Sequencing")


# Regla gramatical que describe la derivacion de la instruccion If
# considerando los diferentes casos
def p_If(p):
    '''
    
    If : TkIf condicion TkArrow bloque variasGuardias TkFi
       | TkIf condicion TkArrow singleInstruccion variasGuardias TkFi
       | TkIf condicion TkArrow expresion variasGuardias TkFi
       | TkIf TkOpenPar condicion TkClosePar TkArrow bloque variasGuardias TkFi
       | TkIf TkOpenPar condicion TkClosePar TkArrow singleInstruccion variasGuardias TkFi
       | TkIf TkOpenPar condicion TkClosePar TkArrow expresion variasGuardias TkFi
    
    '''
    if len(p) == 7:
        p[0]=Node([p[2], p[4], p[5]],"If")
    else:
        p[0] = Node([p[3],p[6],p[7]],"If")
 
# Regla gramatical que deriva de la instruccion If cuando hay mas de una guardia
def p_variasGuardias(p):
    '''
    variasGuardias : TkGuard condicion TkArrow bloque variasGuardias
                   | TkGuard condicion TkArrow print variasGuardias
                   | empty
    
    '''
    # Caso en que hay varias guardias
    if len(p) == 6:
        p[0]=Node([p[2], p[4], p[5]], "Guard")
    # Caso en que variasGuardias evalua lambda
    else: p[0]=Null()

# Regla gramatical que deriva de la instruccion For
def p_For(p):
    '''
    For : TkFor TkId TkIn expresion TkTo expresion TkArrow bloque TkRof
    '''
    p[0]=Node([Token(p[2],"Ident"),Token(None,"In"),p[4],p[6],p[8]], "For") 
    
    aux_table = SymbolTable()

    # Verificamos si la variable de control ya fue declarada, sino
    # la agregamos a una tabla de simbolos auxiliar
    aux_table.push_symbol(p[2],'int')
    stack_table.push(aux_table)
    

    # Verificamos que la variable de control del for no este siendo modificada
    try:
        if (p[0].sons[4].sons[0].sons[0].sons[0].sons[0].sons[0].sons[0].sons[0][0] == p[2]) and (p[0].sons[4].sons[0].sons[0].sons[0].sons[0].sons[0].sons[0].sons[0][2]=='Asig'):
            print("Error: Esta cambiando la variable "+p[2]+", que es una variable de control de una instruccion ’for’")
            sys.exit()
    except:
        pass

    # aux_table.printTable()

# Regla gramatical que deriva de la instruccion Do
def p_Do(p):
    '''
    Do : TkDo condicion TkArrow bloque variasGuardias TkOd
       | TkDo condicion TkArrow singleInstruccion variasGuardias TkOd
       | TkDo condicion TkArrow expresion variasGuardias TkOd
       | TkDo TkOpenPar condicion TkClosePar TkArrow bloque variasGuardias TkOd
       | TkDo TkOpenPar condicion TkClosePar TkArrow singleInstruccion variasGuardias TkOd
       | TkDo TkOpenPar condicion TkClosePar TkArrow expresion variasGuardias TkOd

    '''
    if len(p)== 7:
        p[0]=Node([p[2], p[4], p[5]],"Do")
    else:
        p[0] = Node([p[3],p[6],p[7]],"Do")

# Regla gramatical para determinar condiciones
# Una condicion puede ser de tipo expresion, 
# expresion relacion expresion
# expresion operador booleano expresion
def p_condicion(p):
    '''
    condicion : expresion
              | condicion operadorBool expresion
    '''
    # Caso en que solo hay una expresion
    if len(p)==2:
        p[0]=Node([p[1]], None)
    # Caso en que hay condicion operador y expresion/ expresion relacion expresion
    elif len(p)== 4:
        p[0]=Node([p[1],p[2],p[3]], None)
   

# Regla gramatical para definir operadores booleanos
def p_operadorBool(p):
    '''operadorBool : TkAnd
                    | TkOr
                    | TkNot
    
    '''
    if p[1] == "\/":
        p[0]=Node(None,"Or")
    if p[1] == '!':
        p[0] = Node(None,"Not")
    else:
        p[0]=Node(None,"And")

# Regla gramatical que define los simbolos de una relacion, 
# deriva en los tokens definidos para el lenguaje
def p_relacion(p):
    '''
    relacion : TkLess
             | TkGreater
             | TkLeq
             | TkGeq
             | TkEqual
             | TkNEqual
    '''
    if p[1] == "<":
        p[0]=Node(None, "Less")
    elif p[1] == ">":
        p[0] = Node(None,"Greater")
    elif p[1] == "<=":
        p[0] = Node(None,"Leq")
    elif p[1] == ">=":
        p[0] = Node(None,"Geq")
    elif p[1] == "==":
        p[0] = Node(None,"Equal")
    elif p[1] == "!=":
        p[0] = Node(None,"NEqual")




###########################################
####### GRAMATICA PARA CADA INSTRUCCION ###
###########################################


############ INSTRUCCION READ ##############

# Regla gramatical para leer una variable
def p_read(p):
    ''' read : TkRead TkId '''
    p[0]=Node([Token(p[2],"Ident")],"Read")

    # Revisamos si la variable que se va a leer fue declarada
    if not stack_table.is_in_table(p[2]):
        print("Error: la variable "+p[2]+" esta intentando ser leida pero no ha sido declarada")
        sys.exit()


############ INSTRUCCION PRINT ##############
# Gramatica para imprimir expresiones
# Deriva a print o print ln
def p_print(p):
    ''' print : TkPrint concatPrint 
              | TkPrintln concatPrint
    '''
    if p[1] == 'print':
        p[0]=Node([p[2]],"Print")
    else:
        p[0]=Node([p[2]],"Println")


# Regla gramatical para concatenar expresiones
def p_concatPrint(p):
    '''concatPrint : concatPrint TkConcat expresion
                   | expresion

    '''
    if len(p) == 4:
        p[0]=Node([p[1], p[3]], "Concat")
    else:
        p[0] = Node([p[1]])

###############################################
######### GRAMATICA PARA TIPOS DE VARIABLES ###
###############################################

def p_tipo(p):
    '''tipo : TkBool
            | TkInt
            | TkArray TkOBracket number TkSoForth number TkCBracket
    '''
    if len(p) == 2:
        p[0]=Node([Token(p[1],"type")],None,type='type')
    else:
        p[0]=Node([Token(p[1],'array'),p[3],p[5]],None,type='array')

# Gramatica para literal numero (entero positivo o negativo)
def p_number(p):
    '''
        number : TkNum
               | TkMinus TkNum
    '''
    if len(p) == 2:
        p[0] = Node(Token(p[1]),type='int')
    else:
        p[0] = Node(Token(int(p[1] + str(p[2]))),type='int')

# Gramatica de lambda (token vacio)
def p_empty(p):
    '''empty :'''
    pass


##############################################
######### GRAMATICA PARA EXPRESIONES #########
##############################################

# Gramatica para una expresion
# deriva en termino, operador suma con termino, o expresion, operador
# de suma y termino
def p_expresion(p):
    '''expresion : term
                 | addingOperator term
                 | operadorBool expresion
                 | expresion addingOperator term
                 | expresion relacion expresion
                 | embed
    '''
    # Caso en que es un solo termino
    if len(p) == 2:
        p[0]=Node([p[1]], "Exp")
    # Caso en que es un termino y un operador numerico / un bool y una expresion
    elif len(p) == 3:
        p[0] = Node([p[1],p[2]],"Exp")
    elif len(p) == 4:
        p[0] = Node([p[1],p[2],p[3]],"Exp")
    else:
        p[0] = Node([p[1],p[2],p[3]],"Exp") 

# Regla gramatical para operadores aritmeticos
def p_addingOperator(p):
    '''addingOperator : TkPlus
                      | TkMinus
    '''
    if p[1] == '+':
        p[0]=Node(None, "Plus")
    else:
        p[0]=Node(None,"Minus")

# Regla gramatical para simbolo de terminos
def p_term(p):
    '''term : factor
            | term multiplyingOperator factor
    '''
    if len(p) == 2:
        p[0] = Node([p[1]], None)
    else:
        p[0] = Node([p[1],p[2],p[3]], None)
    
# Regla gramatical para operadores multiplicativos
def p_multiplyingOperator(p):
    '''multiplyingOperator : TkMult
                           | TkDiv
                           | TkMod
    '''
    if p[1] == '*':
        p[0]=Node(None, "Mult")
    elif p[1] == '/':
        p[0]=Node(None,"Div")
    else:
        p[0] = Node(None,"Mod")
    
# Regla gramatical para expresiones de tipo factor:
# variables, numericas, strings, funciones, booleanos
# y combinacion de operadores aritmeticos unarios con variables
def p_factor(p):
    '''factor : TkId
              | TkNum
              | TkString
              | TkTrue
              | TkFalse
              | TkMinus TkNum
              | TkOpenPar expresion TkClosePar
              | TkId TkOBracket expresion TkCBracket
    '''
    # Caso en que es un numero, o true o false
    if len(p) == 2 and isinstance(p[1], int):
        p[0] = Node([Token(str(p[1]),"Literal")],"Literal",type='int')

    elif len(p) == 2 and p[1] == 'true' or p[1] == 'false':
        p[0] = Node([Token(str(p[1]),"Literal")],"Literal",type='bool')
    
    # Caso en que es un string
    elif len(p) == 2 and re.match('"([^"\\\n]|\\"|\\\\|\\n)*"',p[1]):
        p[0] = Node([Token(p[1],"String")],None)

    # Caso en que es un Id
    elif len(p) == 2:
        p[0] = Node([Token(p[1],"Ident")],None)
    
    # Caso en que es numero con simbolo menos delante
    elif isinstance(p[2], int):
        p[0] = Node([Token(str(p[1]),"Literal")],None)

    # Caso en que es una expresion entre parentesis    
    elif len(p) == 4:
        p[0] = Node([p[2]],None)

    # Caso en que es una expresion id[exp]
    elif len(p) == 5:
        p[0]=Node([Token(p[1],"Ident"),p[3]],None)

# Regla gramatical para funciones embebidas
def p_embed(p):
    '''embed : TkMax TkOpenPar TkId TkClosePar
             | TkMin TkOpenPar TkId TkClosePar
             | TkAtoi TkOpenPar TkId TkClosePar
             | TkSize TkOpenPar TkId TkClosePar
    '''
    if p[1] == 'max':
        p[0]=Node([Token(p[3],"Ident")], "Max")
    if p[1] == 'min':
        p[0]=Node([Token(p[3],"Ident")], "Min")
    if p[1] == 'atoi':
        p[0]=Node([Token(p[3],"Ident")], "Atoi")
    if p[1] == 'size':
        p[0]=Node([Token(p[3],"Ident")], "Size")


# Regla gramatical para el manejo de errores de sintaxis
# Por defecto del parser
def p_error(p):
    print ("Error de sintaxis ", p)
    sys.exit(0)

# Casos borde de IO: No ingresa ruta de archivo de entrada
if(len(sys.argv)<=1):
    print("Error, debe ingresar el nombre del archivo a ser leido")
    sys.exit(0)

else:
    # Asignamos al string nombre el nombre del archivo
    nombre=sys.argv[1]

    # Verificacion de la extension del archivo
    if(os.path.splitext((nombre))[1]!=".gusb"):
        print("Formato incorrecto de archivo, recuerde que debe tener extension .gusb")
        sys.exit(0)
    else:
        # Verificacion de la existencia del archivo
        if(os.path.isfile(nombre)):
            # Abrimos el archivo en modo lectura
            archivo=open(nombre,"r")
            # Asignamos al string entrada el contenido de todo el archivo
            entrada=archivo.read()
        else:
            print("El archivo indicado no existe")
            sys.exit(0)

# creamos archivo de formato .vz para generar el arbol abstracto
def traducir(result):
    graphFile = open('AST.vz', 'w')
    graphFile.write(result.traducir())
    graphFile.close()


# Que se haga la magia
parser=yacc.yacc()
result = parser.parse(entrada)

#traducir(result)

result.imprimir(" ")

# PILA
# for i in range(len(stack_table.stack)):
#    print("ELEMENTO "+str(i) + " de la pila",stack_table.stack[i].printTable())

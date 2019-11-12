import ply.yacc as yacc
import os
import codecs
import re

from lexer import tokens
import sys
import os.path
from AST import *

# GuardedUSB Interpreter
# Segunda etapa: Analizador Sintactico
# Lenguaje de implementacion del Interprete: Python 3
# Autores: Carlos Gonzalez y Antonella Requena
# Carnets: 15-10611 15-11196
# Fecha ultimo update: 10/11/2019
# Descripcion: se implemento un lexer utilizando la libreria .ply de python, el siguiente programa recibe un archivo y retorna la lista de "tokens"
# o elementos atomicos del lenguaje si pertenecen, o da un mensaje de error si
# encuentra un caracter que no pertenece al lenguaje. Asi mismo, indica la posicion en donde se encuentra.


# Funcion que describe la regla gramatical para la instruccion programa
# esta instruccion es la principal y deriva a bloque
def p_program(p):
    '''program :  bloque'''
    p[0] = Node([p[1]], "program")


# Funcion que describe la regla gramatical para la instruccion bloque
# Un bloque es todo aquello que este definido entre los brackets
# Esta produccion deriva a t que es el contenido del programa / subprograma
def p_bloque(p):
    '''bloque : TkOBlock t TkCBlock'''
    p[0] = Node([TkOBlock(p[1]), p[2], TkCBlock(p[3])], "bloque")

# Funcion que describe la regla gramatical que genera el contenido del programa
# deriva en declaracion de variables + conjunto de secuenciacion de instrucciones
# o solo conjunto de instrucciones
def p_t(p):
    '''
    t : casoInstrucciones
      | declaracionVariables casoInstrucciones
    '''
    # Caso en que hay declaraciones y luego secuenciacion de instrucciones
    if len(p) == 3: p[0] = Node([p[1], p[2]], "t")
    # Caso en que solo hay secuenciacion de instrucciones
    else: p[0] = Node([p[1]], "t")

# Funcion que describe la regla gramatical que genera una instruccion
# una instruccion puede ser una secuencia de instrucciones o una sola instruccion
# deriva en los tipos de instrucciones definidos para el lenguaje
def p_casoInstrucciones(p):
    '''casoInstrucciones : Instruccion
                         | casoInstrucciones TkSemicolon Instruccion
    '''
    # Caso en que solo hay una instruccion
    if len(p)==2:
        p[0]=Node([p[1]], "Instruccion")
    # Caso recursivo
    else: 
        p[0]=Node([p[1], Semicolon(p[2]), p[3]], "Instruccion recursivo")


###########################################
##### PRODUCCIONES PARA INSTRUCCIONES #####
###########################################

# Funcion que describe la regla gramatical que deriva los diferentes tipos de instrucciones
def p_Instruccion(p):
    '''
    Instruccion : If
                | For
                | Do
                | asignacion
                | read
                | print
    
    '''

    p[0]=Node([p[1]],"Instruccion")


# Regla gramatical que describe la derivacion de la instruccion If
# considerando los diferentes casos
def p_If(p):
    '''
    
    If : TkIf condicion TkArrow bloque variasGuardias TkFi
       | TkIf condicion TkArrow print variasGuardias TkFi
    
    '''
    p[0]=Node([CIf(p[1]), p[2], CArrow(p[3]), p[4], p[5], CFi(p[6])],"If")
 
# Regla gramatical que deriva de la instruccion If cuando hay mas de una guardia
def p_variasGuardias(p):
    '''
    variasGuardias : TkGuard condicion TkArrow bloque variasGuardias
                   | TkGuard condicion TkArrow print variasGuardias
                   | empty
    
    '''
    # Caso en que hay varias guardias
    if len(p) == 6:
        p[0]=Node([CGuard(p[1]), p[2], CArrow(p[3]), p[4], p[5]], "VariasGuardias")
    # Caso en que variasGuardias evalua lambda
    else: p[0]=Null()

# Regla gramatical que deriva de la instruccion For
def p_For(p):
    '''
    For : TkFor TkId TkIn expresion TkTo expresion TkArrow bloque TkRof
    '''
    p[0]=Node([CFor(p[1]),Id(p[2]),CIn(p[3]),p[4],CTo(p[5]),p[6], CArrow(p[7]), p[8], CRof(p[9])], "For") 

# Regla gramatical que deriva de la instruccion Do
def p_Do(p):
    '''
    Do : TkDo condicion TkArrow bloque TkOd
    '''
    p[0]=Node([CDo(p[1]), p[2], CArrow(p[3]),p[4],COd(p[5])],"Do")

# Regla gramatical para determinar condiciones
# Una condicion puede ser de tipo expresion, 
# expresion relacion expresion
# expresion operador booleano expresion
def p_condicion(p):
    '''
    condicion : expresion
              | expresion relacion expresion
              | condicion operadorBool expresion
              | condicion operadorBool expresion relacion expresion
    '''
    # Caso en que solo hay una expresion
    if len(p)==2:
        p[0]=Node([p[1]], "condicion")
    # Caso en que hay condicion operador y expresion/ expresion relacion expresion
    elif len(p)== 4:
        p[0]=Node([p[1],p[2],p[3]], "condicion")
    # Caso en que hay una combinacion de lo anterior
    else:
        p[0]=Node([p[1],p[2],p[3], p[4], p[5]], "condicion")

# Regla gramatical para definir operadores booleanos
def p_operadorBool(p):
    '''operadorBool : TkAnd
                    | TkOr
    
    '''
    p[0]=Node([COr(p[1])], "Bool")

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
    p[0]=Node([CLess(p[1])], "Relacion")

###########################################
####### GRAMATICA PARA CADA INSTRUCCION ###
###########################################


# Gramatica para declaracion de variables #
def p_declaracionVariables(p):
    '''declaracionVariables : TkDeclare declaracionSemicolon'''
    p[0]=Node([Id(p[1]), p[2]],"declaracionVariables")

# Regla gramatical para cuando la declaracion es predecida por una declaracion
# separada por punto y coma
def p_declaracionSemicolon(p):
    '''declaracionSemicolon : declaracionSemicolon TkSemicolon declaracion
                            | declaracion
    
    '''
    if len(p) == 2:
        p[0]=Node([p[1]], "declaracionSemicolon")   
    else:
        p[0]=Node([p[1], Semicolon(p[2]), p[3]], "declaracionSemicolon")

# Declaracion multiple de varios tipos en una misma linea de instruccion	
def p_declaracion(p):
    '''declaracion : TkId TkComma declaracion TkComma tipo
                   | TkId TkTwoPoints tipo
                   | TkId TkComma declaracion
    '''
    if len(p) == 6:
        p[0]=Node([Id(p[1]), Comma(p[2]), p[3], Comma(p[4]), p[5]],"declaracion")
    else:
        p[0]=Node([Id(p[1]), TwoPoints(p[2]), p[3]],"declaracion")
    

# Gramatica para asignacion de variables
def p_asignacion(p):
    '''asignacion : TkId TkAsig listaExpresion
                  | TkId TkAsig asignacionArreglos
    '''

    p[0]= Node([Id(p[1]),Assignment(p[2]), p[3]], "asignacion")

def p_listaExpresion(p):
    '''listaExpresion : listaExpresion TkComma expresion
                      | expresion
    '''
    if len(p) == 2:
        p[0] = Node([p[1]],"expresion")
    else:
        p[0]= Node([p[1],Comma(p[2]), p[3]], "expresion")


def p_asignacionArreglos(p):
    '''asignacionArreglos : TkId listaIndices posicionArreglo'''
    p[0] = Node([Id(p[1]),p[2],p[3]],"asignacionArreglos")

def p_listaIndices(p):
    '''listaIndices : listaIndices TkOpenPar expresion TkTwoPoints expresion TkClosePar
                    | TkOpenPar expresion TkTwoPoints expresion TkClosePar
    '''
    if len(p) == 7:
        p[0] = Node([p[1],Id(p[2]),p[3], Id(p[4]), p[5], Id(p[6])],"listaIndices")
    else:
        p[0] = Node([Id(p[1]),p[2], Id(p[3]), p[4], Id(p[5])],"listaIndices")
        

def p_posicionArreglo(p):
    '''posicionArreglo : TkOBracket TkNum TkCBracket
                       | empty
    '''
    if len(p) == 2:
        p[0] = Null()
    else:
        p[0] = Node([TkOBlock(p[1]),Id(p[2]),Id(p[3])],"array index")


############ INSTRUCCION READ ##############

# Regla gramatical para leer una variable
def p_read(p):
    ''' read : TkRead TkId '''
    p[0]=Node([Id(p[1]),Id(p[2])],"read")


############ INSTRUCCION PRINT ##############
# Gramatica para imprimir expresiones
# Deriva a print o print ln
def p_print(p):
    ''' print : TkPrint concatPrint 
              | TkPrintln concatPrint
    '''
    p[0]=Node([Id(p[1]),p[2]],"print")

# Regla gramatical para concatenar expresiones
def p_concatPrint(p):
    '''concatPrint : concatPrint TkConcat expresion
                   | expresion

    '''
    if len(p) == 4:
        p[0]=Node([p[1], CConcat(p[2]), p[3]], "concat")
    else:
        p[0] = Node([p[1]],"expresion")

###############################################
######### GRAMATICA PARA TIPOS DE VARIABLES ###
###############################################

def p_tipo(p):
    '''tipo : TkBool
            | TkInt
            | TkArray TkOBracket expresion TkSoForth expresion TkCBracket
    '''
    if len(p) == 2:
        p[0]=Node([Id(p[1])], "tipo")
    else:
        p[0]=Node([array(p[1]),COBracket(p[2]),p[3], CSoForth(p[4]),p[5],CCBracket(p[6])],"tipo")


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
                 | expresion addingOperator term
    '''
    if len(p) == 2:
        p[0]=Node([p[1]], "expresion")
    elif len(p) == 3:
        p[0] = Node([p[1],p[2]],"expresion")
    else:
        p[0] = Node([p[1],p[2],p[3]],"expresion") 

# Regla gramatical para operadores aritmeticos
def p_addingOperator(p):
    '''addingOperator : TkPlus
                      | TkMinus
    '''
    p[0]= Node([Plus(p[1])], "AddingOperator")

# Regla gramatical para simbolo de terminos
def p_term(p):
    '''term : factor
            | term multiplyingOperator factor
    '''
    if len(p) == 2:
        p[0] = Node([p[1]],"term")
    else:
        p[0] = Node([p[1],p[2],p[3]],"term")
    
# Regla gramatical para operadores multiplicativos
def p_multiplyingOperator(p):
    '''multiplyingOperator : TkMult
                           | TkDiv
                           | TkMod
    '''
    p[0] = Node([Mult(p[1])],"multiplyingOperator")
    
# Regla gramatical para expresiones de tipo factor:
# variables, numericas, strings, funciones, booleanos
# y combinacion de operadores aritmeticos unarios con variables
def p_factor(p):
    '''factor : TkId
              | TkNum
              | TkString
              | embed
              | TkTrue
              | TkFalse
              | TkNot TkId
              | TkMinus TkNum
              | TkOpenPar expresion TkClosePar
              | TkId TkOBracket expresion TkCBracket
              | TkNot TkId TkOBracket expresion TkCBracket
    '''
    if len(p) == 2 and p[1]!="embed":
        p[0] = Node([Id(p[1])],"factor")
    elif len(p) == 2 and p[1] == "embed":
        p[0] = Node([p[1]],"factor")
    elif len(p) == 3:
        p[0]=Node([Id(p[1]), Id(p[2])], "factor")
    elif len(p) == 4:
        p[0]=Node([Id(p[1]), p[2],Id(p[3])], "factor")        
    elif len(p) == 5:
        p[0]=Node([Id(p[1]), Id(p[2]),p[3],Id(p[4])], "factor")
    elif len(p) == 6:
        p[0]=Node([Id(p[1]),Id(p[2]), Id(p[3]),p[4],Id(p[5])], "factor")


# Regla gramatical para funciones embebidas
def p_embed(p):
    '''embed : TkMax TkOpenPar TkId TkClosePar
             | TkMin TkOpenPar TkId TkClosePar
             | TkAtoi TkOpenPar TkId TkClosePar
             | TkSize TkOpenPar TkId TkClosePar
    '''
    p[0]=Node([CMax(p[1]),CMax(p[2]),CMax(p[3]), Id(p[4])], "embed")

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

traducir(result)

result.imprimir(" ")

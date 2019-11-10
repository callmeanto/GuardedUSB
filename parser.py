# GuardedUSB Interpreter
# Segunda etapa: Analizador Sintactico
# Lenguaje de implementacion del Interprete: Python 3
# Autores: Carlos Gonzalez y Antonella Requena
# Carnets: 15-10611 15-11196
# Fecha ultimo update: 02/11/2019
# Descripcion: se implemento un lexer utilizando la libreria .ply de python, el siguiente programa recibe un archivo y retorna la lista de "tokens"
# o elementos atomicos del lenguaje si pertenecen, o da un mensaje de error si
# encuentra un caracter que no pertenece al lenguaje. Asi mismo, indica la posicion en donde se encuentra.

import ply.yacc as yacc
import os
import codecs
import re

from lexer import tokens
import sys
import os.path
from AST import *


def p_program(p):
    '''program :  bloque'''
    p[0] = program(p[1], "program")


def p_bloque(p):
    '''bloque : TkOBlock t TkCBlock'''
    p[0] = Node([Token(p[1], "OBlock"), p[2], TkCBlock(p[3])], "bloque")


def p_t(p):
    '''
    t : casoInstrucciones
      | declaracionVariables casoInstrucciones
    '''
    if len(p) == 3: p[0] = Node([p[1], p[2]], "t")
    else: p[0] = Node([p[1]], "t")


def p_casoInstrucciones(p):
    '''casoInstrucciones : Instruccion
                         | casoInstrucciones TkSemicolon Instruccion

    '''
    if len(p)==2:
        p[0]=Node([p[1]], "Instruccion")
    else: 
        p[0]=Node([p[1], Semicolon(p[2]), p[3]], "Instruccion recursivo")



###########################################
####### PRODUCCION PARA INSTRUCCIONES #####
###########################################

def p_Instruccion(p):
    '''
    Instruccion : If
                | For
                | Do
                | asignacionVariables
                | readVariables
                | printExpression
    
    '''
    p[0]=Node([p[1]],"Instruccion")

def p_If(p):
    '''
    
    If : TkIf condicion TkArrow bloque variasGuardias TkFi
       | TkIf condicion TkArrow printExpression variasGuardias TkFi
    
    '''
    p[0]=Node([CIf(p[1]), p[2], CArrow(p[3]), p[4], p[5], CFi(p[6])],"If")
 


def p_variasGuardias(p):
    '''
    variasGuardias : TkGuard condicion TkArrow bloque variasGuardias
                   | TkGuard condicion TkArrow printExpression variasGuardias
                   | empty
    
    '''
    if len(p) == 7:
        p[0]=Node([CGuard(p[1]), p[2], CArrow(p[3]), p[4], p[5]], "VariasGuardias1")
    elif len(p) == 6:
        p[0]=Node([CGuard(p[1]), p[2], CArrow(p[3]), p[4], p[5]], "VariasGuardias2")
    else: p[0]=Null()

def p_For(p):
    '''
    
    For : TkFor TkId TkIn expression TkTo expression TkArrow bloque TkRof
    
    '''
    p[0]=Node([CFor(p[1]),Id(p[2]),CIn(p[3]),p[4],CTo(p[5]),p[6], CArrow(p[7]), p[8], CRof(p[9])], "For") 

def p_Do(p):
    '''
    Do : TkDo condicion TkArrow bloque TkOd
    '''
    p[0]=Node([CDo(p[1]), p[2], CArrow(p[3]),p[4],COd(p[5])],"Do")


def p_condicion(p):
    '''
    condicion : tipoExpresion
              | tipoExpresion relation tipoExpresion
              | condicion operadorBool tipoExpresion
              | condicion operadorBool tipoExpresion relation tipoExpresion
    '''
    if len(p)==2:
        p[0]=Node([p[1]], "condicion")
    elif len(p)== 4:
        p[0]=Node([p[1],p[2],p[3]], "condicion")
    else:
        p[0]=Node([p[1],p[2],p[3], p[4], p[5]], "condicion")

def p_operadorBool(p):
    '''operadorBool : TkAnd
                    | TkOr
    
    '''
    p[0]=Node([p[1]], "Bool")



def p_tipoExpresion(p):
    '''tipoExpresion : expression'''
    p[0]=tipoExpression(p[1], "tipoExpression")

def p_relation1(p):
    '''relation : TkLess'''
    p[0]=relation1(CLess(p[1]), "Menor")

def p_relation2(p):
    '''relation : TkGreater'''
    p[0]=relation2(CGreater(p[1]), "Mayor")
def p_relation3(p):
    '''relation : TkLeq'''
    p[0]=relation3(CLeq(p[1]), "Menor igual")
def p_relation4(p):
    '''relation : TkGeq'''
    p[0]=relation4(CGeq(p[1]), "Mayor igual")
def p_relation5(p):
    '''relation : TkEqual'''
    p[0]=relation5(CEqual(p[1]), "Igual")

def p_relation6(p):
    '''relation : TkNEqual'''
    p[0]=relation6(CNEqual(p[1]), "Diferente")




###########################################
####### GRAMATICA PARA CADA INSTRUCCION ###
###########################################


# Gramatica para declaracion de variables
def p_declaracionVariables2(p):
    '''declaracionVariables : TkDeclare declaracionSemiColon'''
    p[0]=declaracionVariables(declare(p[1]), p[2],"declaracionVariables")


def p_declaracionSemicolon1(p):
    '''declaracionSemiColon : declaracionSemiColon TkSemicolon declaracion'''
    p[0]=declaracionSemiColon1(p[1], Semicolon(p[2]), p[3], "declaracionSemicolon1")

def p_declaracionSemicolon2(p):
    '''declaracionSemiColon : declaracion'''
    p[0]=declaracionSemicolon2(p[1], "declaracionSemicolon2")

def p_declaracion1(p):
    '''declaracion : TkId TkComma declaracion TkComma tipo'''
    p[0]=declaracion1(Id(p[1]), Comma(p[2]), p[3], Comma(p[4]), p[5],"declaracion1")

def p_declaracion2(p):
    '''declaracion : TkId TkTwoPoints tipo'''
    p[0]=declaracion2(Id(p[1]), TwoPoints(p[2]), p[3],"declaracion2")

def p_declaracion3(p):
    '''declaracion : TkId TkComma declaracion'''
    p[0]=declaracion3(Id(p[1]), Comma(p[2]), p[3],"declaracion2")




# Gramatica para asignacion de variables
def p_asignacionVariables(p):
    '''asignacionVariables : asignacion'''
    p[0]=asignacionVariables(p[1], "asignacionVariables")

# Caso recursivo
"""def p_asignacion1(p):
    '''asignacion : asignacion TkSemicolon TkId TkAsig expression'''
#	p[0]= asignacion1(p[1],Semicolon(p[2]), Id(p[3]),Assignment(p[4]), p[5], "asignacion1")
"""
# Caso base
def p_asignacion2(p):
    '''asignacion : TkId TkAsig expression'''
    p[0]= asignacion2(Id(p[1]),Assignment(p[2]), p[3], "asignacion2")
#
# Gramatica para leer una variable
def p_readVariables(p):
    ''' readVariables :  read '''
    p[0]=readVariables(p[1],"readVariable")
"""
# Caso recursivo
def p_read1(p):
    ''' read : read TkSemicolon TkRead TkId '''
    p[0]=read1(p[1],Semicolon(p[2]),Read(p[3]),Id(p[4]),"read1")
"""
# Caso base
def p_read2(p):
    ''' read : TkRead TkId '''
    p[0]=read2(Read(p[1]),Id(p[2]),"read2")

# Gramatica para imprimir expresiones
def p_printExpression(p):
    ''' printExpression : print '''
    p[0]=printExpression(p[1],"printExpression")


# Caso base
def p_print2(p):
    ''' print : TkPrint concatPrint'''
    p[0]=print2(Print(p[1]),p[2],"print2")

def p_concatPrint(p):
    '''concatPrint : concatPrint TkConcat expression'''
    p[0]=concatPrint(p[1], CConcat(p[2]), p[3], "concatPrint")

def p_concatPrint2(p):
    '''concatPrint : expression'''
    p[0]=concatPrint2(p[1], "concatPrint2")

#
# Gramatica para imprimir expresiones con salto de linea
def p_printlnExpression(p):
    ''' printlnExpression : println '''
    p[0]=printlnExpression(p[1],"printlnExpression")

# Caso recursivo
"""
def p_println1(p):
    ''' println : println TkSemicolon TkPrintln expression '''
#	p[0]=println1(p[1],Semicolon(p[2]),Println(p[3]),p[4],"print1")
"""
# Caso base
def p_println2(p):
    ''' println : TkPrintln expression '''
    p[0]=println2(Println(p[1]),p[2],"println2")

###############################################
######### GRAMATICA PARA TIPOS DE VARIABLES ###
###############################################

def p_tipo1(p):
    '''tipo : TkBool'''
    p[0]=tipo1(booleano(p[1]), "tipo1 bool")

def p_tipo2(p):
    '''tipo : TkInt'''
    p[0]=tipo2(tipoInt(p[1]), "tipo2 int")

def p_tipo3(p):
    '''tipo : TkArray TkOBracket expression TkSoForth expression TkCBracket'''
    p[0]=tipo3(array(p[1]),COBracket(p[2]),p[3], CSoForth(p[4]),p[5],CCBracket(p[6]),"tipo3 array")

def p_empty(p):
    '''empty :'''
    pass


##############################################
######### GRAMATICA PARA EXPRESIONES #########
##############################################

# Expresion de solo un termino
def p_expression1(p):
    '''expression : term '''
    p[0]=expression1(p[1], "expression1")

def p_expression2(p):
    '''expression : addingOperator term'''

    p[0]=expression2(p[1],p[2], "expression2")

def p_expression3(p):
    '''expression : expression addingOperator term'''
    p[0]=expression3(p[1],p[2],p[3], "expression3")

def p_addingOperator1(p):
    '''addingOperator : TkPlus'''
    p[0]= addingOperator1(Plus(p[1]), "AddingOperator")

def p_addingOperator2(p):
    '''addingOperator : TkMinus'''
    p[0]= addingOperator2(Minus(p[1]), "SubsOperator")

def p_term1(p):
    '''term : factor'''
    p[0] = term1(p[1],"term1")

def p_term2(p):
    '''term : term multiplyingOperator factor'''
    p[0] = term2(p[1],p[2],p[3],"term2")

def p_multiplyingOperator1(p):
    '''multiplyingOperator : TkMult'''
    p[0] = multiplyingOperator1(Mult(p[1]),"multiplyingOperator")

def p_multiplyingOperator2(p):
    '''multiplyingOperator : TkDiv'''
    p[0] = multiplyingOperator2(Div(p[1]),"divisiongOperator")

def p_factor1(p):
    '''factor : Id'''
    p[0] = factor1(p[1],"factor1")

def p_Id1(p):
    '''Id : TkId'''
    p[0]=Id1(Id(p[1]), "Id1")
def p_Id2(p):
    '''Id : TkNot TkId'''
    p[0]=Id2(CNot(p[1]), Id(p[2]), "id2")

def p_factor2(p):
    '''factor : TkNum'''
    p[0] = factor2(Number(p[1]),"factor2")


def p_factor3(p):
    '''factor : TkOpenPar expression TkClosePar'''

    p[0] = factor3(p[2],"factor3")

def p_factor4(p):
    '''factor : TkMinus TkNum'''
    p[0] = factor4(Minus(p[1]),Number(p[2]), "factor4")

def p_factor5(p):
    '''factor : TkString'''
    p[0]= factor5(CString(p[1]),"factor5")

def p_factor6(p):
    '''factor : embed'''
    p[0]=factor6(p[1], "factor6")

def p_factor7(p):
    '''factor : TkTrue'''
    p[0]=factor7(CTrue(p[1]), "True")

def p_factor8(p):
    '''factor : TkFalse'''
    p[0]=factor8(CFalse(p[1]), "True")


def p_embed1(p):
    '''embed : TkMax TkOpenPar TkId TkClosePar'''
    p[0]=embed1(CMax(p[1]), Id(p[3]), "embed1")

def p_embed2(p):
    '''embed : TkMin TkOpenPar TkId TkClosePar'''
    p[0]=embed2(CMin(p[1]), Id(p[3]), "embed2")

def p_embed3(p):
    '''embed : TkAtoi TkOpenPar TkId TkClosePar'''
    p[0]=embed3(CAtoi(p[1]), Id(p[3]), "embed3")


def p_error(p):
    print ("Error de sintaxis ", p)

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


def traducir(result):
    graphFile = open('AST.vz', 'w')
    graphFile.write(result.traducir())
    graphFile.close()


parser=yacc.yacc()
result = parser.parse(entrada)

traducir(result)

result.imprimir(" ")

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
    print("program")
    p[0] = program(p[1], "program")

def p_bloque(p):
    '''bloque : TkOBlock t TkCBlock'''
    print("bloque")
    p[0] = bloque(TkOBlock(p[1]),p[2],TkCBlock(p[3]), "bloque")
    print(p)
"""
def p_lista1(p):
    '''lista : lista TkSemicolon t'''
   # p[0]= lista1(p[1], Semicolon(p[2]), p[3], "lista1")

def p_lista2(p):
    '''lista : t'''
   # p[0]=lista2(p[1], "lista2")
"""

def p_t1(p):
    '''t : casoInstrucciones'''

    p[0]=t(p[1], "t")
def p_t2(p):
 	'''t : declaracionVariables casoInstrucciones'''
 	p[0]=t2(p[1], p[2], "t2")
def p_casoInstrucciones1(p):
	'''casoInstrucciones : listaInstrucciones'''
	p[0]=casoInstrucciones1(p[1], "casoInstrucciones1")
def p_casoInstrucciones2(p):
	'''casoInstrucciones : casoInstrucciones TkSemicolon listaInstrucciones'''
	p[0]=casoInstrucciones2(p[1], Semicolon(p[2]), p[3], "casoInstrucciones2")


def p_listaInstruccionesIf(p):
    '''listaInstrucciones : instruccionIf'''
    p[0]=listaInstruccionesIf(p[1],"listaInstruccionesIf")

def p_instruccionIf1(p):
    '''instruccionIf : TkIf condicion TkArrow bloque variasGuardias TkFi'''
    p[0]=instruccionIf1(CIf(p[1]), p[2], CArrow(p[3]), p[4], p[5], CFi(p[6]),"InstruccionIf1")

#Caso declaracion de variables
def p_instruccionIf2(p):
    '''instruccionIf : TkIf condicion TkArrow printExpression variasGuardias TkFi'''
    p[0]=instruccionIf2(CIf(p[1]), p[2], CArrow(p[3]), p[4], p[5], CFi(p[6]),"InstruccionIf2")


def p_variasGuardias1(p):
    '''variasGuardias : TkGuard condicion TkArrow bloque variasGuardias'''
    p[0]=variasGuardias1(CGuard(p[1]), p[2], CArrow(p[3]), p[4], p[5], "VariasGuardias1")

def p_variasGuardias2(p):
    '''variasGuardias : TkGuard condicion TkArrow printExpression variasGuardias'''
    p[0]=variasGuardias2(CGuard(p[1]), p[2], CArrow(p[3]), p[4], p[5], "VariasGuardias2")

def p_variasGuardiasEmpty(p):
    '''variasGuardias : empty'''
    p[0]=Null()


def p_condicion1(p):
    '''condicion : tipoExpresion'''
    p[0]=condicion1(p[1], "condicion1")

def p_condicion2(p):
    '''condicion : tipoExpresion relation tipoExpresion'''
    p[0]=condicion2(p[1],p[2],p[3], "condicion2")

def p_condicion3(p):
    '''condicion : condicion operadorBool tipoExpresion'''
    p[0]=condicion3(p[1], p[2], p[3],  "condicion3")

def p_condicion4(p):
    '''condicion : condicion operadorBool tipoExpresion relation tipoExpresion'''
    p[0]=condicion4(p[1],p[2],p[3], p[4], p[5], "condicion4")

def p_operadorBool1(p):
    '''operadorBool : TkAnd'''
    p[0]=operadorBool1(CAnd(p[1]), "operadorAnd")

def p_operadorBool2(p):
    '''operadorBool : TkOr'''
    p[0]=operadorBool2(COr(p[1]), "operadorOr")

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
####### PRODUCCION PARA INSTRUCCIONES #####
###########################################

def p_listaInstruccionesAsig(p):
	''' listaInstrucciones : asignacionVariables'''
	p[0]=listaInstruccionesAsig(p[1],"listaInstruccionesAsig")
#
def p_listaInstruccionesRead(p):
	''' listaInstrucciones : readVariables '''
	p[0]=listaInstruccionesRead(p[1],"listaInstruccionesRead") 

def p_listaInstruccionesPrint(p):
	''' listaInstrucciones : printExpression '''
	p[0]=listaInstruccionesPrint(p[1],"listaInstruccionesPrint")

def p_listaInstruccionesPrintln(p):
	''' listaInstrucciones : printlnExpression '''
	p[0]=listaInstruccionesPrintln(p[1],"listaInstruccionesPrintln")

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

# Caso recursivo
"""
def p_print1(p):
	''' print : print TkSemicolon TkPrint expression '''
	#p[0]=print1(p[1],Semicolon(p[2]),Print(p[3]),p[4],"print1")
"""
# Caso base
def p_print2(p):
	''' print : TkPrint expression '''
	p[0]=print2(Print(p[1]),p[2],"print2")
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
    print("expression1")

def p_expression2(p):
    '''expression : addingOperator term'''

    p[0]=expression2(p[1],p[2], "expression2")
    print("expression2")

def p_expression3(p):
    '''expression : expression addingOperator term'''
    print("expresion3")
    p[0]=expression3(p[1],p[2],p[3], "expression3")

def p_addingOperator1(p):
    '''addingOperator : TkPlus'''
    p[0]= addingOperator1(Plus(p[1]), "AddingOperator")
    print("addingOperator1")

def p_addingOperator2(p):
    '''addingOperator : TkMinus'''
    p[0]= addingOperator2(Minus(p[1]), "SubsOperator")
    print("addingOperator2")

def p_term1(p):
    '''term : factor'''
    p[0] = term1(p[1],"term1")
    print("term1")

def p_term2(p):
    '''term : term multiplyingOperator factor'''
    print("term2")
    p[0] = term2(p[1],p[2],p[3],"term2")

def p_multiplyingOperator1(p):
    '''multiplyingOperator : TkMult'''
    p[0] = multiplyingOperator1(Mult(p[1]),"multiplyingOperator")
    print("multiplyingOperator1")

def p_multiplyingOperator2(p):
    '''multiplyingOperator : TkDiv'''
    p[0] = multiplyingOperator2(Div(p[1]),"divisiongOperator")
    print("multiplyingOperator2")

def p_factor1(p):
    '''factor : TkId'''
    p[0] = factor1(Id(p[1]),"factor1")
    print("factor1")

def p_factor2(p):
    '''factor : TkNum'''
    p[0] = factor2(Number(p[1]),"factor2")
    print("factor2")


def p_factor3(p):
    '''factor : TkOpenPar expression TkClosePar'''

    p[0] = factor3(p[2],"factor3")

def p_factor4(p):
    '''factor : TkMinus TkNum'''
    p[0] = factor4(Minus(p[1]),Number(p[2]), "factor4")

def p_factor5(p):
	'''factor : TkString'''
	#p[0]= factor5(Id(p[1]),"factor5")

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
    print("Guardado")


parser=yacc.yacc()
result = parser.parse(entrada)

traducir(result)

#print(result)

result.imprimir(" ")
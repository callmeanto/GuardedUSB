# GuardedUSB Interpreter
# Primera etapa: Lexer
# Lenguaje de implementacion del Interprete: Python 3
# Autores: Carlos Gonzalez y Antonella Requena
# Carnets: 15-10611 15-11196
# Fecha ultimo update: 08/10/2019
# Descripcion: se implemento un lexer utilizando la libreria .ply de python, el siguiente programa recibe un archivo y retorna la lista de "tokens"
# o elementos atomicos del lenguaje si pertenecen, o da un mensaje de error si 
# encuentra un caracter que no pertenece al lenguaje. Asi mismo, indica la posicion en donde se encuentra.


# Importamos modulos necesarios
import ply.lex as lex
import sys
import os.path

# Lista de tipos de tokens

# Reserved words: diccionario de palabras reservadas del lenguaje, esto es, 
# corresponde, a palabras que tienen un uso especifico y no se 
# expresan mediante una regla de expresion regular

reserved = {
    # Boolean values
    'true': 'TkTrue',
    'false': 'TkFalse',

    # Types admitted
    'int': 'TkInt',
    'bool': 'TkBool',
    'array': 'TkArray',

    # Miscelaneous
    'declare': 'TkDeclare',
    'print': 'TkPrint',
    'println': 'TkPrintln',
    'read': 'TkRead',

    # Conditionals
    'if': 'TkIf',
    'fi': 'TkFi',

    # Loops
    'for': 'TkFor',
    'in': 'TkIn',
    'to': 'TkTo',
    'rof': 'TkRof',
    'do': 'TkDo',
    'od': 'TkOd',

    # Type conversion and embed functions
    'atoi': 'TkAtoi',
    'size': 'TkSize',
    'max': 'TkMax',
    'min': 'TkMin',
}

# Es necesario indicar al modulo ply la lista de tokens que se implementaran, 
# lo cual se realiza a continuacion.
tokens = [

    'TkId',
    'TkNum',
    'TkString',

    # Separators
    'TkOBlock',
    'TkCBlock',
    'TkSoForth',
    'TkComma', 
    'TkOpenPar',
    'TkClosePar',
    'TkAsig',
    'TkSemicolon',
    'TkArrow',
    'TkGuard',
   

    # Operators
    'TkPlus',
    'TkMinus',
    'TkMult',
    'TkDiv',
    'TkMod',
    'TkOr',
    'TkAnd',
    'TkNot',
    'TkLess',
    'TkLeq',
    'TkGeq',
    'TkGreater',
    'TkEqual',
    'TkNEqual',
    'TkOBracket',
    'TkCBracket',
    'TkTwoPoints',
    'TkConcat',

    # Comments
    'TkComment',

] + list(reserved.values())  # Agregamos la lista de palabras reservadas


###################### REGULAR EXPRESSION RULES FOR TOKENS ################
###########################################################################

# Regular expression rules for separators
t_TkOBlock = r'\|\['
t_TkCBlock = r'\]\|'
t_TkSoForth = r'\.\.'
t_TkComma = r'\,'
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkAsig = r'\:\='
t_TkSemicolon = r'\;'
t_TkArrow = r'\-\-\>'
t_TkGuard = r'\[\]'

# Regular expression rules for operators
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkMult = r'\*'
t_TkDiv = r'\/'
t_TkMod = r'\%'
t_TkOr = r'\\\/'
t_TkAnd = r'\/\\'
t_TkNot = r'\!'
t_TkLess = r'\<'
t_TkLeq = r'\<\='
t_TkGeq = r'\>\='
t_TkGreater = r'\>'
t_TkEqual = r'\=\='
t_TkNEqual = r'\!\='
t_TkOBracket = r'\['
t_TkCBracket = r'\]'
t_TkTwoPoints = r'\:'
t_TkConcat = r'\|\|'

# Regular expression rule to identify variables
def t_TkId(id):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    id.type = reserved.get(id.value, 'TkId')    # Check for reserved words
    return id

# Regular expression rule to identify integer numbers
def t_TkNum(num):
    r'\d+'
    num.value = int(num.value)
    return num

# Regular expression rule to identify strings
def t_TkString(string):
    r'"([^"\\\n]|\\"|\\\\|\\n)*"'
    return string


# Rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string to ignore spaces and tabs
t_ignore = ' \t'


# Rule to ignore comments
def t_TkComment(t):
    r'//.*'
    pass

# Error handling rule
def t_error(t):
    print("Error: Unexpected character " +
          str(t.value[0]) + " in row " + str(t.lineno) + ", column " + str(t.lexpos+1))
    t.lexer.skip(1)


# Entrada de nombre de archivo para el input y lectura del mismo
# Se verifica si el usuario introdujo en la llamada a programa el archivo 
# correspondiente a ser leido, en caso contrario, el programa no es ejecutado.
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

# Funcion utilizada exclusivamente para imprimir en el formato indicado 
# los atributos del token que se piden(tipo y posicion)
def print_format(t):
    if(t.type == 'TkId' or t.type == 'TkNum' or t.type == 'TkString'):
        print(str(t.type)+"("+"\""+str(t.value)+"\""+")" +
              " "+str(t.lineno)+" "+str(t.lexpos+1))
    else:
        print(str(t.type)+" "+str(t.lineno)+" "+str(t.lexpos+1))


# Build the lexer
lexer = lex.lex()

# Give the lexer input
lexer.input(entrada)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print_format(tok)

# Cerramos el archivo
archivo.close()
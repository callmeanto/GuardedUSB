import sys

# Mensajes de error


def p_error(id):
    # codigo de error para pila vacia
    if id == 0:
        return "Empty Stack: Couldn't add any entry because there is no table"

    # codigo de error para cuando hay underflow
    if id == 1:
        return "Stack Underflow: Couldn't delete scope"


class SymbolTable:

    # Constructor de la table de simbolos
    # El argumento table superior contendra un objeto del tipo table de simbolo
    # y este sera justamente la table del scope inmediatamente superior
    def __init__(self, table_superior=None):
        self.table = {}
        self.table_anterior = table_superior

    # Agrega simbolos a la table anadir_table
    def push_symbol(self, id,  tipo, valor=None):
        if not self.exists_table(id):
            self.table[id] = [tipo, valor]
        else:
            print("Error, la variable " + id + " ya ha sido declarada")
            sys.exit()

    # Funcion que se encargara de verificar si el simbolo ya existe en la table
    def exists_table(self, id):
        if self.table.get(id) == None:
            return False
        else:
            return self.table[id]

    # Metodo para imprimir bonito la tabla de simbolos
    def printTable(self):
        print('\n'+ "Symbols Table")
        if self.table != {}:
            aux = ''
            for i in self.table.keys():
                if self.table[i][0] != 'int' and self.table[i][0] != 'bool' :
                    type = str(self.table[i][0][0][0]) + '['+str(self.table[i][0][0][1]) + '..' + str(self.table[i][0][0][2]) + ']'
                else: 
                    type = str(self.table[i][0])
                aux = "variable: " + str(i) + " | " + "type: " + type
                print(aux)
            return aux
        return ''



# Implementacion de la clase Pila (de tables de simbolos)
# con sus respectivas operaciones
class TableStack:

    # Constructor de la clase
    def __init__(self):
        self.stack = []
        self.head = 0

    # Insertar en la pila una nueva table

    def push(self, table):
        self.stack.append(table)
        self.head = len(self.stack) - 1

    # ELiminar table de la pila
    def pop(self):
        if not self.empty():
            return self.stack.pop()
        else:
            p_error(1)

    # Consultar el tope de la pila
    def top(self):
        return self.stack[len(self.stack) - 1]

    # Consultar si un elemento esta en alguna de las tables de la pila
    def is_in_table(self, id):

        if not self.empty():
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i].exists_table(id) != False:
                    return self.stack[i].exists_table(id)
            return False

        # Pila vacia
        return p_error(1)

    # Modificar algun valor de la pila
    def modify_symbol(self, id, valor, indexacion=None):
        x = self.is_in_table(id)
        if not x:
            print("Error: variable " + id + " no declarada")
            sys.exit()
        if indexacion == None:
            x[1] = valor
        else:
            x[1][indexacion] = valor

    def empty(self):
        return self.stack == []

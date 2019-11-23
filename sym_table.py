from stack import *

# Mensajes de error
def p_error(id):
    # codigo de error para pila vacia
    if id == 0:
        return "Empty Stack: Couldn't add any entry because there is no table"

    # codigo de error para cuando hay underflow
    if id == 1:
        return "Stack Underflow: Couldn't delete scope"
    


# Clase para tabla de simbolos, con sus respectivos metodos
class SymbolTable:

    # Constructor de la clase cuyo
    # unico atributo es table
    def __init__(self):
        self.table = Stack()

    # Insertar scope: insertar una nueva tabla en la pila
    # en la pila, utilizando push
    def insert_scope(self):
        self.table.push({})

    # Eliminar scope: eliminar tabla de la pila
    def delete_scope(self):
        # Verificamos si no esta vacia la pila
        if not self.table.isEmpty():
            self.table.pop()
        # Si esta vacia, arrojamos una excepcion
        else:
            raise Exception(p_error(1))

    # Insertar una entrada (en tabla): si la pila no esta vacia, 
    # agrega el parametro value en la posicion 'key' tabla que esta en el tope de la pila 
    def insert(self, key, value):

        # Si no esta vacia la pila, se puede hacer el insert
        if not self.table.isEmpty():

            # Obtenemos la tabla tope de la lista
            current_table = self.table.top()

            # Si no existe tal entrada en la tabla, se agrega
            # en la posicion 'key' de la tabla
            if not key in current_table:
                current_table[key] = value
                return True

            # Si ya existia, se retorna False    
            return False

        # Si la pila esta vacia, se arroja una excepcion
        raise Exception(p_error(0))

    # Query: consulta a la pila 
    # Hacemos una consulta en la pila completa desde el fondo
    # asi revisamos desde el scope mas amplio
    def query(self, key):

        # Verificamos que la pila no este vacia
        if not self.table.isEmpty():

            # Iteramos sobre todas las tablas en la pila
            for i in range(self.table.size() - 1, -1, -1):
                aux = self.table.get_level(i)
                result = self._isInTable(aux, key)
                if result != None:
                     return result

        raise Exception(p_error(0))

    def _isInTable(self, hash_, key):
        try:
            return hash_[key]
        except:
            return None


    # Metodo para asignacion de un nuevo valor a una variable
    def modificar(self, key, valor):
        if not self.table.isEmpty():
            for i in range(self.table.size() - 1, -1, -1):
                aux = self.table.get_level(i)
                result = self._isInTable(aux, key)
                if result is not None:
                    aux[key] = valor

    # Metodo para imprimir bonitico el nivel actual de estado de las variables
    def __str__(self):
        if not self.table.isEmpty():
            aux1 = ''
            for i in range(self.table.size() - 1, -1, -1):
                aux = self.table.get_level(i)
                aux1 += str(i) + ') ' + str(aux) + '\n'
            return aux1
        return ''

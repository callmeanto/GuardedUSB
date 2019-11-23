# Clase Pila

# Implementacion de una pila utilizando operaciones de lista de python
class Stack(object):

    def __init__(self):
        super(Stack, self).__init__()
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.isEmpty():
            return self.items.pop()

    def top(self):
        if not self.isEmpty():
            return self.items[-1]

    def size(self):
        return len(self.items)

    def get_level(self, level):
        if not self.isEmpty() and level < self.size() and level >= 0:
            return self.items[level]

    def __str__(self):
        lista = ''
        for i in range(len(self.items)-1, -1, -1):
            lista += '[' + str(self.items[i]) + '],' + '\n'
        return lista

from collections import deque

class Postfix:
    def __init__(self, infix):
        self.infix = infix
        self.precedence = {'|': 1, '.': 2, '*': 3}  # Define la precedencia de los operadores en un diccionario

    def infix_to_postfix(self):
        postfix = ""  # Resultado en notación postfix
        stack = deque()  # Usamos una pila para almacenar los operadores

        for char in self.infix:
            # Si el caracter no es un operador, añádelo al postfix
            if char not in self.precedence and char not in ['(', ')']:
                postfix += char
            # Si es un paréntesis abierto, añádelo a la pila
            elif char == '(':
                stack.append(char)
            # Si es un paréntesis cerrado, desapila hasta que encuentres el paréntesis abierto correspondiente
            elif char == ')':
                while stack and stack[-1] != '(':
                    postfix += stack.pop()
                if stack and stack[-1] == '(':
                    stack.pop()
                else:
                    raise ValueError("Invalid infix expression: mismatched parentheses")
            # Si es un operador, desapila todos los operadores de mayor o igual precedencia, luego apila este operador
            else:
                while stack and self.precedence.get(char, -1) <= self.precedence.get(stack[-1], -1):
                    postfix += stack.pop()
                stack.append(char)

        # Al final, desapila cualquier operador restante y añádelo al postfix
        while stack:
            if stack[-1] == '(':
                raise ValueError("Invalid infix expression: mismatched parentheses")
            postfix += stack.pop()

        return postfix

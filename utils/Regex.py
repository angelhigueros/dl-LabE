import re

class Regex:
    OPERATORS = ['*', '|', '+', '?', '.']

    def __init__(self, regex: str):
        self.regex = regex
        self.is_valid = self._validate()

    def _add_dots(self):
        """Agrega puntos en la expresión regular para marcar secuencias consecutivas."""
        new_regex = ""

        for i in range(len(self.regex) - 1):
            char, next_char = self.regex[i], self.regex[i + 1]
            new_regex += char

            if (
                char != '(' and
                next_char != ')' and
                next_char not in self.OPERATORS and
                char != '|'
            ):
                new_regex += '.'

        new_regex += self.regex[-1]
        return new_regex

    def _check_operators(self):
        """Verifica que los operadores estén correctamente utilizados en la expresión regular."""
        last_was_operator = False
        for char in self.regex:
            if char in self.OPERATORS:
                if last_was_operator and char not in {')', '|'}:
                    raise ValueError("No puede haber dos operadores seguidos.")
                last_was_operator = True
            else:
                last_was_operator = False

    def _check_parentheses(self):
        """Verifica que los paréntesis estén balanceados en la expresión regular."""
        open_parentheses = 0
        for char in self.regex:
            if char == '(':
                open_parentheses += 1
            elif char == ')':
                open_parentheses -= 1
                if open_parentheses < 0:
                    raise ValueError("Paréntesis desbalanceados, falta un '('.")

        if open_parentheses > 0:
            raise ValueError("Paréntesis desbalanceados, falta un ')'.")

    def _validate(self):
        """Realiza todas las verificaciones de la expresión regular."""
        try:
            self._check_operators()
            self._check_parentheses()
        except ValueError as error:
            print(error)
            return False

        return True

    def process_regex(self):
        """Procesa la expresión regular si es válida."""
        if not self.is_valid:
            return "Expresión regular inválida."

        self.regex = self._add_dots()
        return self.regex

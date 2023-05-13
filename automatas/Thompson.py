from automatas.DFA import DFA
from automatas.NFA import NFA

class Transition:
    def __init__(self, state, symbol, next_state):
        self.state = state
        self.symbol = symbol
        self.next_state = next_state

class Thompson:
    def __init__(self, postfix):
        self.postfix = postfix
        self.generated_states = 0

    # Crea un nuevo estado
    def new_state(self):
        state = self.generated_states
        self.generated_states += 1
        return state

    # Crea una transición y la añade al NFA dado
    def add_transition(self, nfa, start, symbol, end):
        transition = Transition(start, symbol, end)
        nfa.transitions.append(transition)

    # Función para manejar símbolos en la expresión
    def symbolRule(self, symbol):
        initial_state = self.new_state()
        final_state = self.new_state()
        nfa = NFA(initial_state, final_state)
        self.add_transition(nfa, initial_state, symbol, final_state)
        return nfa

    # Función para manejar la operación OR en la expresión
    def orExpression(self, nfa1, nfa2):
        initial_state = self.new_state()
        final_state = self.new_state()

        nfa = NFA(initial_state, final_state)
        self.add_transition(nfa, initial_state, 'ε', nfa1.initial_state)
        self.add_transition(nfa, initial_state, 'ε', nfa2.initial_state)
        self.add_transition(nfa, nfa1.final_state, 'ε', final_state)
        self.add_transition(nfa, nfa2.final_state, 'ε', final_state)
        
        nfa.transitions.extend(nfa1.transitions)
        nfa.transitions.extend(nfa2.transitions)

        return nfa

    # Función para manejar la concatenación en la expresión
    def concatExpression(self, nfa1, nfa2):
        nfa = NFA(nfa1.initial_state, nfa2.final_state)

        nfa.transitions.extend(nfa1.transitions)
        for transition in nfa2.transitions:
            if transition.state == nfa2.initial_state:
                transition.state = nfa1.final_state
            nfa.transitions.append(transition)

        return nfa

    # Función para manejar la operación de Kleene (estrella) en la expresión
    def kleeneExpression(self, nfa1):
        initial_state = self.new_state()
        final_state = self.new_state()

        nfa = NFA(initial_state, final_state)
        self.add_transition(nfa, initial_state, 'ε', nfa1.initial_state)
        self.add_transition(nfa, nfa1.final_state, 'ε', nfa1.initial_state)
        self.add_transition(nfa, nfa1.final_state, 'ε', final_state)
        self.add_transition(nfa, initial_state, 'ε', final_state)

        nfa.transitions.extend(nfa1.transitions)

        return nfa


    def nfaConstruction(self):
        stack = []

        for i in range(len(self.postfix)):
            character = self.postfix[i]

            if character not in ['|', '.', '*']:
                stack.append(self.symbolRule(character))
            elif character == '*':
                nfa1 = stack.pop()
                stack.append(self.kleeneExpression(nfa1))
            elif character == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self.concatExpression(nfa1, nfa2))
            elif character == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self.orExpression(nfa1, nfa2))
        return stack[-1]

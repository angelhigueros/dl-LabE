import copy
import pydot
from utils.Graph import *
from automatas.DFA import DFA
from collections import OrderedDict

class Grammar:
    def __init__(self):
        self.initialState = None
        self.productions = {}
        self.terminals = []
        self.nonTerminals = []


class Transition:
    def __init__(self, state, symbol, next_state):
        self.state = state
        self.symbol = symbol
        self.next_state = next_state


class Set:
    def __init__(self):
        self.estado = 0
        self.corazon = {}
        self.resto = {}
        self.productions = {}

class YAPar:
    def __init__(self, inputname):
        """Inicializa el objeto YAPar"""
        
        # Intenta abrir el archivo de entrada
        try:
            self.file = open(inputname, 'r')
        except FileNotFoundError as e:
            raise FileNotFoundError('El archivo no pudo ser abierto') from e

        self.filename = inputname
        self.lines = self.file.readlines()

        # Inicializa las propiedades de la gramática
        self.grammar = None

    def compiler(self):
        """Compila la gramática"""
        
        self.grammar = self.defineGrammar()

    def defineGrammar(self):  # sourcery skip: raise-specific-error
        """Define la gramática a partir de las líneas del archivo"""
        
        grammar = Grammar() 
        nonTerminals = set()
        terminals = set()

        # Busca el comienzo de las producciones de la gramática
        i = next((i for i, line in enumerate(self.lines) if line.startswith("%%")), None)
        if i is None:
            raise Exception("Las producciones de gramática no se encontraron")

        nonterm = None
        prods = []
        for line in self.lines[i+1:]:
            line = line.strip()
            if not line:
                continue
            if line.endswith(":"):
                if nonterm is not None:
                    grammar.productions[nonterm] = prods
                    nonTerminals.add(nonterm)
                nonterm = line[:-1].strip()
                prods = []
            else:
                productions = [prod.strip() for prod in line.split("|") if prod.strip()]
                prods.extend(productions)
                for prod in productions:
                    for symbol in prod.split():
                        if symbol.islower():
                            nonTerminals.add(symbol)
                        elif symbol != ";":
                            terminals.add(symbol)

        # Asegúrate de agregar la última producción
        if nonterm is not None:
            grammar.productions[nonterm] = prods
            nonTerminals.add(nonterm)

        grammar.initialState = next(iter(grammar.productions.keys()))
        grammar.nonTerminals = sorted(list(nonTerminals))
        grammar.terminals = sorted(list(terminals))

        # Elimina los caracteres ';' de las producciones
        for nonterm, prods in grammar.productions.items():
            grammar.productions[nonterm] = [prod for prod in prods if prod != ";"]

        return grammar

    def increaseGrammar(self, grammar):
        """Aumenta la gramática dada, agregando una nueva producción al comienzo"""
        
        # Realiza una copia profunda de la gramática para evitar la mutación no deseada
        tempGrammar = copy.deepcopy(grammar)

        # Crea un nuevo estado inicial y añade una producción que apunta al antiguo estado inicial
        newInitialState = f"{tempGrammar.initialState}'"
        tempGrammar.productions = {newInitialState: [tempGrammar.initialState], **tempGrammar.productions}

        return tempGrammar

    def firstSet(self, grammar):  # sourcery skip: avoid-builtin-shadow
        """Calcula el conjunto inicial de la gramática dada"""
        
        set = Set()
        
        # Realiza una copia profunda de la gramática para evitar la mutación no deseada
        tempGrammar = copy.deepcopy(grammar)

        # Obtiene la primera producción de la gramática aumentada
        increasedItem = next(iter(tempGrammar.productions.items()))

        # Añade un punto al principio de la producción
        withDot = f'.{increasedItem[1][0]}'
        increasedItem[1][0] = withDot

        # Añade la producción al conjunto
        set.corazon[increasedItem[0]] = increasedItem[1]
        set.productions[increasedItem[0]] = increasedItem[1]

        # Calcula el cierre del conjunto y construye el autómata
        firstSet = self.cerradura(set)
        firstSet.estado = self.estados
        self.estados += 1
        self.buildAutomaton(firstSet)


    def format_label(self, state, state_number):
        return f"State {state_number}\n" + '\n'.join(f"{key} -> {' | '.join(value)}\\l" for key, value in state.items())

    def buildAutomaton(self, firstSet):
        """Construye el autómata a partir del conjunto inicial"""
        
        # Inicializa el autómata y los conjuntos de corazones
        afd = DFA(firstSet.estado, [0])
        self.sets.append(firstSet)
        corazones = [firstSet.corazon]

        # Recorre cada conjunto y construye las transiciones
        for set in self.sets:
            symbols = self.getSymbols(set)
            for symbol in symbols:
                newSet = self.move(set, symbol)
                if newSet.corazon not in corazones:
                    newSet.estado = self.estados
                    self.estados += 1
                    self.sets.append(newSet)
                    corazones.append(newSet.corazon)
                nextStateIndex = corazones.index(newSet.corazon)
                nextState = self.sets[nextStateIndex]
                transition = Transition(set, symbol, nextState)
                afd.transitions.append(transition)

        # Inicializa el gráfico
        graph = pydot.Dot(graph_type='digraph')

        # Añade los nodos al gráfico
        for set in self.sets:
            label = self.format_label(set.productions, set.estado)
            node = pydot.Node(label)
            graph.add_node(node)

        # Añade las transiciones al gráfico
        for transition in afd.transitions:
            state = self.format_label(transition.state.productions, transition.state.estado)
            next_state = self.format_label(transition.next_state.productions, transition.next_state.estado)
            edge = pydot.Edge(state, next_state, label=transition.symbol)
            graph.add_edge(edge)

        # Añade una transición al estado de aceptación para el estado inicial aumentado
        for transition in afd.transitions[::-1]:
            if transition.state.estado == 1:
                state = self.format_label(transition.state.productions, transition.state.estado)
                next_state = 'accept'
                edge = pydot.Edge(state, next_state, label='$')
                graph.add_edge(edge)

        # Guarda el gráfico y actualiza el autómata
        graph.write_pdf('graphs/LR0.pdf')
        afd.final_states = ['accept']
        self.afdLR0 = afd

        return self.afdLR0

    def cerradura(self, I):
        """Calcula la cerradura de un conjunto de producciones"""
        
        J = copy.deepcopy(I)
        added = True  # Bandera para indicar si se añadieron nuevos elementos

        # Iterar mientras se sigan añadiendo nuevos elementos
        while added:
            added = False
            productions_copy = dict(J.productions)  # Crear una copia del diccionario para evitar errores de iteración
            for value in productions_copy.values():
                for prod in value:
                    parts = prod.split()
                    for part in parts:
                        if '.' in part and part[-1] != '.':
                            next_part_idx = parts.index(part) + 1
                            if next_part_idx < len(parts) and parts[next_part_idx] not in self.increasedGrammar.terminals:
                                sinPunto = part.replace('.', '')
                                if sinPunto in self.increasedGrammar.productions:
                                    for new_prod in self.increasedGrammar.productions[sinPunto]:
                                        new_item = f'.{new_prod}'
                                        if new_item not in J.productions.setdefault(sinPunto, []):
                                            J.productions.setdefault(sinPunto, []).append(new_item)
                                            J.resto.setdefault(sinPunto, []).append(new_item)
                                            added = True
        return J

    def move(self, I, X):
        """Calcula el conjunto de producciones resultante de mover el punto a la derecha del símbolo X en el conjunto I"""
        
        J = Set()
        I2 = copy.deepcopy(I)
        for key, value in I2.productions.items():
            for prod in value:
                parts = prod.split()
                for i, part in enumerate(parts):
                    if '.' in part:
                        sinPunto = part.replace('.', '')
                        if sinPunto == X:
                            parts[i] = f'{X}.'
                            if i+1 < len(parts):
                                parts[i+1] = f'.{parts[i + 1]}'
                            new_prod = ' '.join(parts)
                            J.productions.setdefault(key, []).append(new_prod)
                            J.corazon.setdefault(key, []).append(new_prod)
        return self.cerradura(J)

    def getSymbols(self, I):
        """Obtiene los símbolos que siguen a un punto en el conjunto de producciones I"""
        
        symbols = []
        for value in I.productions.values():
            for production in value:
                parts = production.split()
                for i, part in enumerate(parts):
                    if '.' in part and i+1 < len(parts):
                        next_symbol = parts[i+1].split()[0]
                        if next_symbol not in symbols:
                            symbols.append(next_symbol)
        return symbols



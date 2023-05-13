from automatas.DFA import DFA
from automatas.NFA import NFA

class Transition:
    def __init__(self, state, symbol, next_state):
        self.state = state
        self.symbol = symbol
        self.next_state = next_state


class Minimization:
    def __init__(self, dfa):
        self.dfa = dfa  # DFA original
        self.dfaFinalStates = dfa.final_states  # Estados finales del DFA original
        self.dfaStates = dfa.states  # Estados del DFA original
        self.dfaTransitions = dfa.transitions  # Transiciones del DFA original
        self.initialPartition = []  # Partición inicial
        self.partitions = []  # Particiones resultantes
        self.symbolsList = self.symbols()  # Lista de símbolos utilizados en las transiciones
        self.transitions = {}  # Diccionario de transiciones del DFA mínimo
        self.finalStates = []  # Estados finales del DFA mínimo
        self.initialState = 0  # Estado inicial del DFA mínimo

    def symbols(self):
        symbol = []  # Lista de símbolos
        for transition in self.dfaTransitions:
            if transition.symbol not in symbol:
                symbol.append(transition.symbol)
        return symbol  # Devuelve la lista de símbolos

    def buildInitialPartition(self):
        accept = []  # Estados de aceptación
        accept.extend(self.dfaFinalStates)

        nonAccept = [state for state in self.dfaStates if state not in accept]  # Estados no de aceptación
        self.initialPartition.append(accept)  # Agrega la lista de estados de aceptación a la partición inicial

        if nonAccept:
            self.initialPartition.append(nonAccept)  # Agrega la lista de estados no de aceptación a la partición inicial

        self.buildNewPartitions(self.initialPartition)  # Construye las nuevas particiones a partir de la partición inicial

    def buildNewPartitions(self, partitions):
        self.partitions = partitions.copy()  # Copia la lista de particiones
        newPartitions = self.partitions.copy()  # Copia la lista de particiones en una nueva lista

        for partition in self.partitions:
            dicPartition = {}  # Diccionario para almacenar las transiciones de cada estado en la partición

            if len(partition) > 1:
                for state in partition:
                    dicSymbol = {}  # Diccionario para almacenar las transiciones por símbolo

                    for symbol in self.symbolsList:
                        for transition in self.dfaTransitions:
                            if transition.state == state and transition.symbol == symbol:
                                dicSymbol[f"G{symbol}"] = f"G{str(self.getIndex(transition.next_state, self.partitions))}"

                    dicPartition[state] = dicSymbol  # Agrega las transiciones del estado al diccionario de la partición

                index = newPartitions.index(partition)  # Obtiene el índice de la partición actual en la lista de particiones
                newPartitions.pop(index)  # Elimina la partición actual de la lista

                for i, l in enumerate(self.getCombinations(dicPartition)):
                    newPartitions.insert(index + i, l)  # Inserta las nuevas particiones generadas en la lista

        if newPartitions == self.partitions:
            return self.partitions  # Si no hay cambios en las particiones, devuelve la lista actual

        self.buildNewPartitions(newPartitions)  # Continúa construyendo nuevas particiones recursivamente


    def getIndex(self, integer, list):
        for i, sublist in enumerate(list):
            if integer in sublist:
                return i  # Devuelve el índice de la sublista que contiene el entero buscado

    def getCombinations(self, dicPartition):
        value_sets = set()  # Conjunto para almacenar conjuntos de valores únicos
        value_dict = {}  # Diccionario para almacenar combinaciones de estados

        for key, values in dicPartition.items():
            value_set = frozenset(values.items())  # Convierte el diccionario de transiciones en un conjunto congelado
            if value_set not in value_sets:
                value_sets.add(value_set)  # Agrega el conjunto congelado a los conjuntos de valores únicos
                value_dict[value_set] = [key]  # Crea una nueva lista en el diccionario para el conjunto congelado
            else:
                value_dict[value_set].append(key)  # Agrega el estado a la lista existente en el diccionario

        return list(value_dict.values())  # Devuelve las listas de combinaciones de estados

    def minDFAConstruction(self):
        self.buildInitialPartition()  # Construye la partición inicial
        self.partitions = sorted(self.partitions, key=lambda x: x[0])  # Ordena las particiones por el primer estado de cada una
        
        for partition in self.partitions:
            for state in self.dfaFinalStates:
                if state in partition:
                    estadoNuevo = self.getIndex(state, self.partitions)
                    self.finalStates.append(estadoNuevo)  # Agrega los estados finales del DFA mínimo

        self.finalStates = list(set(self.finalStates))  # Elimina duplicados de los estados finales

        dfa = DFA(self.initialState, self.finalStates)  # Crea un nuevo DFA mínimo

        for partition in self.partitions:
            representative = partition[0]  # Representante de la partición
            index = self.getIndex(representative, self.partitions)  # Índice de la partición en la lista de particiones
            dicSymbol = {}  # Diccionario para almacenar las transiciones por símbolo

            for symbol in self.symbolsList:
                for transition in self.dfaTransitions:
                    if transition.state == representative and transition.symbol == symbol:
                        nextIndex = self.getIndex(transition.next_state, self.partitions)
                        dicSymbol[symbol] = nextIndex
                        transition = Transition(index, symbol, nextIndex)
                        dfa.transitions.append(transition)  # Agrega las transiciones al DFA mínimo

            self.transitions[index] = dicSymbol  # Agrega las transiciones al diccionario de transiciones

        return dfa  # Devuelve el DFA mínimo construido
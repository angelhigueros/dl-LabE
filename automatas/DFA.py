class DFA:
    def __init__(self, initial_state, final_states):
        self.transitions = []  # Lista de transiciones del DFA
        self.initial_state = initial_state  # Estado inicial del DFA
        self.final_states = final_states  # Estados finales del DFA
        self.states = []  # Lista de estados del DFA

    def getStates(self):
        # Obtener estados únicos del DFA
        states = set()  # Conjunto para almacenar los estados únicos

        for transition in self.transitions:
            states.add(transition.state)  # Agregar estado actual a los estados
            states.add(transition.next_state)  # Agregar estado siguiente a los estados

        self.states = sorted(states)  # Ordenar los estados en orden ascendente

        return self.states  # Devolver la lista de estados únicos

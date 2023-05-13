
class NFA:
    def __init__(self, initial_state, final_state):
        self.transitions = []  # Lista de transiciones del NFA
        self.initial_state = initial_state  # Estado inicial del NFA
        self.final_state = final_state  # Estado final del NFA
        self.states = []  # Lista de estados del NFA

    def getStates(self):
        # Obtener estados únicos del NFA
        states = set()  # Conjunto para almacenar los estados únicos

        for transition in self.transitions:
            states.add(transition.state)  # Agregar estado actual a los estados
            states.add(transition.next_state)  # Agregar estado siguiente a los estados

        self.states = sorted(states)  # Ordenar los estados en orden ascendente

        return self.states  # Devolver la lista de estados únicos



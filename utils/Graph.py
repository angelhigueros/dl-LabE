import graphviz as gv

class Graph:
    # Inicialización de la clase Graph
    def __init__(self):
        self.graph = gv.Digraph(graph_attr={'rankdir': 'LR'})
       
    # Método que se encarga de la visualización del gráfico
    def show(self, transitions, initial_state, final_states, title=None, filename='my_nfa'):
        try: 
            # Añade todas las transiciones al gráfico
            self._add_transitions(transitions)
            
            # Añade el estado inicial al gráfico
            self._add_initial_state(initial_state)
            
            # Añade todos los estados finales al gráfico
            self._add_final_states(final_states)
            
            # Añade un título al gráfico, si se proporciona
            if title:
                self._add_title(title)
            
            # Devuelve una vista del gráfico
            return self.graph.view(filename=filename)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Método privado para añadir las transiciones al gráfico
    def _add_transitions(self, transitions):
        for transition in transitions:
            self.graph.edge(str(transition.state), str(transition.next_state), label=transition.symbol)

    # Método privado para añadir el estado inicial al gráfico
    def _add_initial_state(self, initial_state):
        self.graph.node(str(initial_state), shape='circle', style='bold')
        self.graph.node('start', shape='point')
        self.graph.edge('start', str(initial_state), arrowhead='normal')

    # Método privado para añadir los estados finales al gráfico
    def _add_final_states(self, final_states):
        for final_state in final_states:
            self.graph.node(str(final_state), shape='doublecircle')

    # Método privado para añadir un título al gráfico
    def _add_title(self, title):
        self.graph.node('title', label=title, shape='none', fontsize='20', fontcolor='black', fontname='Arial')

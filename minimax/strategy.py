import node

class Strategy:
    """
    Clase para representar la estrategia de juego de
    los agentes.

    Atributos
    ---------
    root : StateNode
        Raíz del árbol de búsqueda Minimax. La raíz es dinámica, según
        se vaya avanzando en el juego se va moviendo hacia el estado
        actual del juego.
    limh : int
        Horizonte limitado
    
    Métodos
    -------
    expand()
        Expande el árbol desde la raíz actual.
    evaluate_tree()
        Evalúa los nodos en el horizonte limitado y propaga las evaluaciones
        hacia la raíz.
    next_step(move)
        Mueve la raíz del árbol hacia el siguiente paso, dado por el Agente
        o por el jugador.
    equivalent_next_step(board)
        Obtiene el hijo de la raíz del árbol para el cual es equivalente
        el estado dado en el parámetro.
    """

    def __init__(self, board, limh):
        self.root = node.StateNode(board, None)
        self.limh = limh

        self.expand()
        self.evaluate_tree()

    def expand(self):
        """
        Expande el árbol desde la raíz definida en este objeto hasta el
        horizonte limitado.

        Este método es llamado al construir el árbol por primera vez y
        cuando se alcanza el horizonte limitado.
        """
        current_level = [self.root]
        next_level = []
        for _ in range(self.limh):
            for current_node in current_level:
                current_node.gen_children()
                next_level.extend(current_node.children)
            
            if len(next_level) == 0: break
            current_level = next_level
            next_level = []
    
    def evaluate_tree(self):
        """
        Evalúa el horizonte limitado y propaga la evaluación hacia los
        nodos padre hasta la raíz.
        """
        self.root.evaluate()

    def next_step(self, move):
        """
        Establece el nodo obtenido como la raíz del árbol.
        
        El nodo pasado en el parámetro debe haber sido conseguido a
        partir de los hijos de la raíz de este objeto (self.root) para
        garantizar que se mantendrá el subárbol restante.
            Para el Agente: self.root.best_child(mode)
            Para el Jugador: <Strategy object>.equivalent_next_step(board)
        """
        self.root = move
        if not self.root.has_children():
            self.expand()
            self.evaluate_tree()

    def equivalent_next_step(self, board):
        """
        Retorna el nodo que cuyo estado es equivalente al estado del tablero
        dado en el parámetro. El nodo retornado se debe usar para next_step().
        """
        for child in self.root.children:
            if child.is_equivalent_to(board):
                return child

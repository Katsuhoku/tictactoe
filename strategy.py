import node
import numpy as np
import time

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
    """

    def __init__(self, board, limh, func):
        self.root = node.StateNode(board)
        self.limh = limh
        self.func = func

        start = time.time()
        self.expand()
        self.evaluate_tree()
        end = time.time()
        print(f'{end - start} segundos')

    def expand(self):
        """
        Expande el árbol desde la raíz definida en este objeto hasta el
        horizonte limitado.

        Este método es llamado al construir el árbol por primera vez y
        cuando se alcanza el horizonte limitado.
        """
        max_turn = True
        current_level = [self.root]
        next_level = []
        count = 0
        for _ in range(self.limh): # hasta el horizonte limitado
            for current_node in current_level: # conjunto de nodos en el mismo nivel
                if current_node.game_end == 0:
                    next_level.extend(current_node.gen_children(max_turn))
            
            if len(next_level) == 0: break
            count += len(next_level)
            current_level = np.copy(next_level)
            next_level = []
            max_turn = not max_turn
        
        print(f'{count} nodos generados')
    
    def evaluate_tree(self):
        """
        Evalúa el horizonte limitado y propaga la evaluación hacia los
        nodos padre hasta la raíz.
        """
        self.root.evaluate(func=self.func)

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
        
        print('|| Siguientes movimientos ||')
        for child in self.root.children:
            print(f'{child.board} {child.evaluation} {child.game_end}')


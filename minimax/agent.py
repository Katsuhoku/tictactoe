import strategy

class Agent:
    """
    Clase para representar el Agente inteligente utlizando minimax.

    Atributos
    ---------
    """

    def __init__(self, board, limh):
        self.strategy = strategy.Strategy(board, limh)

    def move(self, current_board):
        """
        Analiza el árbol en la estrategia y realiza su movimiento.
        """
        best = self.strategy.root.best_child()
        self.strategy.next_step(best)

        return best.equivalent_tile(current_board)

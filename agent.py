import strategy
import numpy as np

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

        transform = self.strategy.root.is_equivalent_by(current_board) # Transformación de equivalencia
        best = self.strategy.root.best_child()
        next_board = best.randt()

        if transform == 'id':
            next_board = np.copy(next_board).tolist()
        if transform == 'ta':
            next_board = np.flip(np.swapaxes(np.flip(next_board, 1), 0, 1), 1).tolist()
        if transform == 'td':
            next_board = np.swapaxes(next_board,0,1).tolist()
        if transform == 'mh':
            next_board = np.flip(next_board, 0).tolist()
        if transform == 'mv':
            next_board = np.flip(next_board, 1).tolist()
        if transform == 'r90':
            next_board = np.rot90(next_board,k=1).tolist()
        if transform == 'r180':
            next_board = np.rot90(next_board,k=2).tolist()
        if transform == 'r270':
            next_board = np.rot90(next_board,k=3).tolist()

        self.strategy.next_step(best)

        return next_board
    
    def check_usermov(self, current_board):
        """
        Ajusta la raíz del árbol en la estrategia hacia el movimiento
        del jugador.
        """
        for child in self.strategy.root.children:
            if child.is_equivalent_by(current_board) != 'none':
                self.strategy.next_step(child)
                break

import strategy
import numpy as np

class Agent:
    """
    Clase para representar el Agente inteligente utlizando minimax.

    Atributos
    ---------
    """

    def __init__(self, board, limh, func):
        self.strategy = strategy.Strategy(board, limh, func)

    def move(self, current_board):
        """
        Analiza el árbol en la estrategia y realiza su movimiento.
        """

        transform = self.strategy.root.is_equivalent_by(current_board) # Transformación de equivalencia
        best = self.strategy.root.best_child()

        print('|| Movimiento ||')
        print(f'{best.board} {best.evaluation} {best.game_end} {transform} {best.parent._sym}')

        print('|| Transformación ||')
        next_board = best.randt()
        print(f'{next_board}')

        if transform == 'id':
            print('Identidad')
            next_board = np.copy(next_board).tolist()
        if transform == 'ta':
            print('Tranposicion Ascendente')
            next_board = np.flip(np.swapaxes(np.flip(next_board, 1), 0, 1), 1).tolist()
        if transform == 'td':
            print('Transposicion Descendente')
            next_board = np.swapaxes(next_board,0,1).tolist()
        if transform == 'mh':
            print('Mirror Horizontal')
            next_board = np.flip(next_board, 0).tolist()
        if transform == 'mv':
            print('Mirror Vertical')
            next_board = np.flip(next_board, 1).tolist()
        if transform == 'r90':
            print('r90')
            next_board = np.rot90(next_board,k=1).tolist()
        if transform == 'r180':
            print('r180')
            next_board = np.rot90(next_board,k=2).tolist()
        if transform == 'r270':
            print('r270')
            next_board = np.rot90(next_board,k=3).tolist()
        
        print(f'{next_board}')

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

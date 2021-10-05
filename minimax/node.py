import numpy as np

class StateNode:
    """
    Clase para almacenar un estado del tablero, el estado del cual
    proviene (parent) y los estados posibles que se generan desde
    él (children).

    Atributos
    ---------
    board : numpy.matrix
        Tablero del Tic Tac Toe con los movimientos generados hasta
        el momento en el juego, representado de forma homóloga con un
        arreglo bidimensional.
    evaluation : int
        Evaluación del nodo. Por defecto es cero, pero debe ser
        inicializada llamando a la función evaluate().
    parent : StateNode
        Estado previo a este, a partir del cual fue generado (None
        si es la raíz).
    children : List[StateNode]
        Lista de los posibles siguientes movimientos a partir del
        estado de este nodo.
    """

    evaluation = 0
    children = []

    def __init__(self, board, parent):
        self.board = np.matrix(board)
        self.parent = parent
    
    def gen_children(self):
        """
        Genera los hijos para este nodo.
        """

    def best_child(self, mode='max'):
        """
        Retorna el nodo con la mejor evaluación para el modo solicitado.
        Los hijos de este nodo debieron haber sido previamente generados
        y evaluados antes de llamar función, de lo contrario retornará
        None.
            mode='max': Retorna el nodo hijo con la mayor evaluación
            mode='min': Retorna el nodo hijo con la menor evaluación
        """

    def evaluate(self, mode='max'):
        """
        Evalua este nodo. La evaluación se retorna y además se establece
        como atributo de este nodo.

        La evaluación será diferente según si el nodo tiene un
        conjunto de hijos definido o no:
            Si el nodo no tiene un conjunto de hijos definido, signfica
            que está en el horizonte. La evaluación correspondrá a la
            función de evaluación definida.
            Si el nodo tiene un conjunto de hijos definido, la evaluación
            se dará con base en el modo en el argumento
                mode='max': se tomará la evaluación del mayor de
                los hijos
                mode='min': se tomará la evaluación del mayor de
                los hijos
        """
    
    def is_equivalent_to(self, board):
        """
        Verifica si el estado del tablero almacenado en este nodo es
        equivalente (simétrico) al tablero dado como argumento.
        """

    def has_children(self):
        """
        Verifica si este nodo tiene nodos hijo.
        """
        if not self.children: return False
        return True
    
    def equivalent_tile(self, board):
        """
        Obtiene las coordenadas (x,y) del siguiente movimiento equivalentes
        con el tablero en el argumento.

        Esto se debe a que el tablero en el estado actual del juego puede
        no ser igual pero sí simétrico al tablero en el nodo, por tanto, para
        colocar la pieza respectiva en el tablero del juego se requieren
        las coordenadas relativas al estado equivalente.
        """
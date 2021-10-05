import numpy as np

winning_sequences = [
    [(0,0),(0,1),(0,2)],
    [(1,0),(1,1),(1,2)],
    [(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)],
    [(0,1),(1,1),(2,1)],
    [(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)],
    [(0,2),(1,1),(2,0)]
]

class StateNode:
    """
    Clase para almacenar un estado del tablero, el estado del cual
    proviene (parent) y los estados posibles que se generan desde
    él (children).

    Atributos
    ---------
    board : List[]
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
    _sym : str
        Ejes de simetría. Simplifican la generación de hijos y evita
        comparaciones.
    """

    evaluation = 0
    children = []

    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.game_end = 0

        for ws in winning_sequences:
            if board[ws[0][0]][ws[0][1]] == 1 and board[ws[1][0]][ws[1][1]] == 1 and board[ws[2][0]][ws[2][1]] == 1:
                self.game_end = 1
                break
            if board[ws[0][0]][ws[0][1]] == 2 and board[ws[1][0]][ws[1][1]] == 2 and board[ws[2][0]][ws[2][1]] == 2:
                self.game_end = 2
                break

        self._sym = ''
        count = 0
        if self.board[0][0] == self.board[0][2] and self.board[1][0] == self.board[1][2] and self.board[2][0] == self.board[2][2]:
            count += 1
            self._sym += 'mv'
        if self.board[0][0] == self.board[2][0] and self.board[0][1] == self.board[2][1] and self.board[0][2] == self.board[2][2]:
            count += 1
            self._sym += 'mh'
        if self.board[0][2] == self.board[2][0] and self.board[0][1] == self.board[1][0] and self.board[1][2] == self.board[2][1]:
            count += 1
            self._sym += 'td'
        if self.board[0][0] == self.board[2][2] and self.board[0][1] == self.board[1][2] and self.board[1][0] == self.board[2][1]:
            count += 1
            self._sym += 'ta'
        
        if count == 0: self._sym += 'none'
        if count > 2: self._sym = 'all'
    
    def gen_children(self, max_turn):
        """
        Genera los hijos para este nodo según sea el siguiente movimiento.
            max_turn=True: Construye los siguientes movimientos con max (2)
            max_turn=False: Construye los siguientes movimientos con min (1)
        """

        if self._sym == 'none':
            children = self.gen_children_none(max_turn)
        elif self._sym == 'mv':
            children = self.gen_children_mv(max_turn)
        elif self._sym == 'mh':
            children = self.gen_children_mh(max_turn)
        elif self._sym == 'td':
            children = self.gen_children_td(max_turn)
        elif self._sym == 'ta':
            children = self.gen_children_ta(max_turn)
        elif self._sym == 'mvmh':
            children = self.gen_children_mvmh(max_turn)
        elif self._sym == 'tdta':
            children = self.gen_children_tdta(max_turn)
        elif self._sym == 'all':
            children = self.gen_children_all(max_turn)

        self.children = children
        return children
    
    def gen_children_none(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def gen_children_mv(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(3):
            for j in range(2):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def gen_children_mh(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(2):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def gen_children_td(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(3):
            for j in range(i,3):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def gen_children_ta(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(3):
            for j in range(3-i):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def gen_children_mvmh(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(2):
            for j in range(1):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children

    def gen_children_tdta(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(1):
            for j in range(1,3):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def gen_children_all(self, max_turn):
        if max_turn: tile = 2
        else: tile = 1

        children = []
        for i in range(2):
            for j in range(i,2):
                if self.board[i][j] == 0:
                    self.board[i][j] = tile
                    children.append(StateNode(np.copy(self.board).tolist(), self))
                    self.board[i][j] = 0
        
        return children
    
    def add_child(self, child_node):
        self.children.append(child_node)

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
        if not self.children:
            if self.game_end == 1:
                self.evaluation = -99999
            elif self.game_end == 2:
                self.evaluation = 99999
            else:
                count_max = 0
                count_min = 0
                swapped = np.swapaxes(self.board, 0, 1)

                for i in range(3):
                    if self.board[i][0] in [0,1] and self.board[i][1] in [0,1] and self.board[i][2] in [0,1]:
                        count_min += 1
                    if self.board[i][0] in [0,2] and self.board[i][1] in [0,2] and self.board[i][2] in [0,2]:
                        count_max += 1
                    if swapped[i][0] in [0,1] and swapped[i][1] in [0,1] and swapped[i][2] in [0,1]:
                        count_min += 1
                    if swapped[i][0] in [0,2] and swapped[i][1] in [0,2] and swapped[i][2] in [0,2]:
                        count_max += 1
                
                if self.board[0][0] in [0,1] and self.board[1][1] in [0,1] and self.board[2][2] in [0,1]:
                    count_min += 1
                if self.board[0][0] in [0,2] and self.board[1][1] in [0,2] and self.board[2][2] in [0,2]:
                    count_max += 1
                if swapped[0][2] in [0,1] and swapped[1][1] in [0,1] and swapped[2][0] in [0,1]:
                    count_min += 1
                if swapped[0][2] in [0,2] and swapped[1][1] in [0,2] and swapped[2][0] in [0,2]:
                    count_max += 1

                self.evaluation = count_max - count_min
            return self.evaluation
        
        if mode == 'max':
            self.evaluation =  max([c.evaluate(mode='min') for c in self.children])
        else:
            self.evaluation =  min([c.evaluate(mode='max') for c in self.children])
        
        return self.evaluation
    
    def is_equivalent_to(self, board):
        """
        Verifica si el estado del tablero almacenado en este nodo es
        equivalente (simétrico) al tablero dado como argumento.

        Parameters
        ----------
        board : List[]
            Tablero en forma de listas de Python
        """
        transforms = [
            self.transpose_asc,
            self.transpose_desc,
            self.mirror_horizontal,
            self.mirror_vertical,
            self.rot90,
            self.rot180,
            self.rot270,
        ]

        for t in transforms:
            if np.array_equal(t(), board): return True
        
        return False

    def has_children(self):
        """
        Verifica si este nodo tiene nodos hijo.
        """
        if not self.children: return False
        return True
    
    def rot90(self):
        return np.rot90(self.board).tolist()
    
    def rot180(self):
        return np.rot90(self.board, k=2).tolist()
    
    def rot270(self):
        return np.rot90(self.board, k=3).tolist()
    
    def mirror_vertical(self):
        return np.flip(self.board, 1).tolist()
    
    def mirror_horizontal(self):
        return np.flip(self.board).tolist()
    
    def transpose_desc(self):
        return np.swapaxes(self.board, 0, 1).tolist()
    
    def transpose_asc(self):
        return np.flip(np.swapaxes(np.flip(self.board, 1), 0, 1), 1).tolist()
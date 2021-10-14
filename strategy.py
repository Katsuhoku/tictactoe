import time
import numpy as np
import node

class Strategy:
    """
    Class representing the strategy for the Minimax Agent. Stores the root of
    a tree of StateNodes representing the possible game states from the
    current state of the tic tac toe to the next horizon.
    """

    def __init__(self, board, limh):
        self.root = node.StateNode(board)
        self.limh = limh

        start = time.time()
        self.expand()
        self.evaluate_tree()
        end = time.time()

    def expand(self):
        """
        Expands the tree from the initial state given when constructed to
        the limited horizon.
        """
        max_turn = True
        current_level = [self.root]
        next_level = []
        count = 0
        for _ in range(self.limh): # 'til horizon
            for current_node in current_level:
                if current_node.game_end == 0:
                    next_level.extend(current_node.gen_children(max_turn))
            
            if len(next_level) == 0: break
            count += len(next_level)
            current_level = np.copy(next_level)
            next_level = []
            max_turn = not max_turn
    
    def evaluate_tree(self):
        """
        Evaluates the root of the strategy. The node evaluation is a recursive
        process, so it will actually evaluate from the limited horizon to the
        root with a single call.
        """
        self.root.evaluate()

    def next_step(self, move):
        """
        Updates the root of the tree in this strategy. The root must be a
        node from the children of the tree root. Also expands the new root
        if doesn't have any children
        """
        self.root = move
        if not self.root.has_children():
            self.expand()
            self.evaluate_tree()


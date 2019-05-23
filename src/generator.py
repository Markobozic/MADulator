from expression import *
import random

default_number_of_nodes: int = 20
default_variable_ratio: float = .5
maximum_value: int = 320

class Generator():
    total_leaves = 0

    def __init__(self):
        pass

    def __init__(self, seed: int):
        random.seed(seed)

    def random_function(self, nodes: int = default_number_of_nodes, variable_ratio: float = default_variable_ratio) -> Expression:
        leaves = []

        # Generate a random plan for 'var' and 'value' leaves
        for i in range(0, nodes):
            if i < nodes * variable_ratio:
                leaves.append('var')
            else:
                leaves.append('value')
        random.shuffle(leaves)

        # Generate the nodes
        function = self.randomize_node(nodes, leaves)
        return function

    def split(self, number: int) -> int:
        '''Randomly divides a number in two with a minimum size of 1.'''
        value = random.randint(1,number-1)
        return value, number - value

    def randomize_node(self, nodes: int, leaves: []) -> Expression:
        node = None

        # If this is a leaf node, grab a type from the leaves list
        if nodes == 1:
            leaf = leaves.pop(0)
            if leaf == 'var':
                node = Var()
            else:
                node = Value()
                node.set_number(random.randint(1, maximum_value))
            return node

        # If this is a branch, make it a math operator
        num = random.randint(0,9)
        if num == 0:
            node = Add()
        elif num == 1:
            node = Sub()
        elif num == 2:
            node = Mult()
        elif num == 3:
            node = Div()
        elif num == 4:
            node = Mod()
        elif num == 5:
            node = ShiftLeft()
        elif num == 6:
            node = ShiftRight()
        elif num == 7:
            node = BitOr()
        elif num == 8:
            node = BitOr()
        elif num == 9:
            node = BitOr()
        nodes -= 1
        left_nodes = 1
        right_nodes = 1
        if nodes > 2:
            left_nodes, right_nodes = self.split(nodes)
        node.left = self.randomize_node(left_nodes, leaves)
        node.right = self.randomize_node(right_nodes, leaves)
        return node

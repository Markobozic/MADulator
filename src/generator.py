from src.expression import *
import random

default_number_of_nodes: int = 32
default_number_of_variables: int = 3
maximum_value: int = 32

class Generator():
    total_leaves = 0

    def __init__(self):
        pass

    def __init__(self, seed: int):
        random.seed(seed)

    def add_variables(self, number: int) -> None:
        '''Changes some leaf nodes to be variables.'''
        while number > 0:
            length = len(leaf_nodes)
            rand = random.randint(0, length-1)
            leaf_nodes[rand]

    def random_function(self, nodes: int = default_number_of_nodes, variables: int = default_number_of_variables) -> Expression:
        leaves = []

        # Generate a random plan for 'var' and 'value' leaves
        for i in range(0, nodes + 1 // 2):
            if i < variables:
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
                node.set_number(random.randint(0, maximum_value))
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
            node = BitAnd()
        elif num == 8:
            node = BitOr()
        elif num == 9:
            node = BitXor()
        nodes -= 1
        left_nodes = 1
        right_nodes = 1
        if nodes > 2:
            left_nodes, right_nodes = self.split(nodes - 1)
        node.left = self.randomize_node(left_nodes, leaves)
        node.right = self.randomize_node(right_nodes, leaves)
        return node


if __name__ == '__main__':
    temp = Generator(1).random_function()

from expression import *
#import generator
import random

def randomize_node(node: Expression, nodes: int) -> Expression:
    if nodes <= 1:
        node = Var()
        return node
    num = random.randint(0,7)
    if num == 0:
        node = Add()
    elif num == 1:
        node = Sub()
    elif num == 2:
        node = Mult()
    elif num == 3:
        node = Div()
    elif num == 4:
        node = Pow()
    elif num == 5:
        node = Mod()
    elif num == 6:
        node = ShiftLeft()
    elif num == 7:
        node = ShiftRight()
    split = int((nodes-1)/2)
    node.left = randomize_node(node.left, split)
    node.right = randomize_node(node.right, split)
    return node

root = Add()
root = randomize_node(root, 8)
print(root)

for i in range(100):
    print(root.eval(i+1))

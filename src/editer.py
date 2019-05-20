from expression import *
from graphviz import Digraph

dot = Digraph(comment='Your Function')

class Editor():

    function = None

    def __init__(self):
        pass

    def print_operations_menu(self):
        print("\n1. Add\n2. Sub\n3. Mult\n4. Div\n5. Mod\n6. Shift Left\n")
        print("7. Shift Right\n8. Bit And\n9. Bit Or\n10. Bit Xor\n")

    def print_expressions_menu(self):
        print("\n1. Add\n2. Sub\n3. Mult\n4. Div\n5. Mod\n6. Shift Left\n")
        print("7. Shift Right\n8. Bit And\n9. Bit Or\n10. Bit Xor\n")
        print("11. Variable\n12. Value\n")

    def get_function(self) -> Expression:
        bad_op = True
        bad_func = True
        function = None

        print("Let's build your own math function to test out!")
        while bad_func:
            while bad_op:
                self.print_operations_menu()
                op = int(input("Starting operation (pick a number): "))
                if op >= 1 and op <= 10:
                    bad_op = False
                function = self.fill_op_node(op)

            if self.check_for_t(function) == True:
                bad_func = False

        return function

    def fill_op_node(self, op: int) -> Expression:
        node = None
        op = 0
        operation = None
        left = None
        right = None

        if op == 1:
            node = Add()
            operation = '+'
        elif op == 2:
            node = Sub()
            operation = '-'
        elif op == 3:
            node = Mult()
            operation = '*'
        elif op == 4:
            node = Div()
            operation = '/'
        elif op == 5:
            node = Mod()
            operation = '%'
        elif op == 6:
            node = ShiftLeft()
            operation = "<<"
        elif op == 7:
            node = ShiftRight()
            operation = ">>"
        elif op == 8:
            node = BitAnd()
            operation = '&'
        elif op == 9:
            node = BitOr()
            operation = '|'
        elif op == 10:
            node = BitXor()
            operation = '^'

        dot.clear()
        dot.node('P', operation)
        dot.node('L', 'left')
        dot.node('R', 'right')
        dot.edges(['PL', 'PR'])
        dot.view()

        node.left = self.get_expression('l', operation, left)
        node.right = self.get_expression('r', operation, right)

        dot.node('P', operation)
        dot.node('L', left)
        dot.node('R', right)
        dot.edges(['PL', 'PR'])
        dot.view()

        return node

    def get_expression(self, side: str, operation: str, next_op: str) -> Expression:
        node = None
        ex = 0
        bad_ex = True

        while bad_ex:
            self.print_expressions_menu()
            if side == 'l':
                ex = int(input("Left of ",operation, "(pick a number): "))
            elif side == 'r':
                ex = int(input("Right of ",operation, "(pick a number): "))
            if ex >= 1 and ex <= 12:
                bad_ex = False

        node = fill_expression(ex, next_op)

        return node

    def fill_expression(self, op: int, next_op: str) -> Expression:
        node = None
        left = None
        right = None

        if op == 1:
            node = Add()
            operation = '+'
        elif op == 2:
            node = Sub()
            operation = '-'
        elif op == 3:
            node = Mult()
            operation = '*'
        elif op == 4:
            node = Div()
            operation = '/'
        elif op == 5:
            node = Mod()
            operation = '%'
        elif op == 6:
            node = ShiftLeft()
            operation = "<<"
        elif op == 7:
            node = ShiftRight()
            operation = ">>"
        elif op == 8:
            node = BitAnd()
            operation = '&'
        elif op == 9:
            node = BitOr()
            operation = '|'
        elif op == 10:
            node = BitXor()
            operation = '^'
        elif op == 11:
            node = Var()
            operation = 't'
        elif op == 12:
            node = Value()
            value = string(node.get_number())
            operation = value

        next_op = operation

        dot.node('P', operation)
        dot.node('L', 'left')
        dot.node('R', 'right')
        dot.edges(['PL', 'PR'])
        dot.view()

        if op == 11 or op == 12:
            return node

        node.left = self.get_expression('l', operation, left)

        dot.node('P', operation)
        dot.node('L', left)
        dot.node('R', 'right')
        dot.edges(['PL', 'PR'])
        dot.view()

        node.right = self.get_expression('r', operation, right)

        dot.node('P', operation)
        dot.node('L', left)
        dot.node('R', right)
        dot.edges(['PL', 'PR'])
        dot.view()
        
        return node

    def check_for_t(self, function: Expression) -> bool:
        #if condition:
        #    return True

        return False

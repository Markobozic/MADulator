from expression import *

class Editor():

    stack = None
    root = None

    def __init__(self):
        pass

    def new_key(self, key: str, function: Expression) -> Expression:
        root = function
        stack = function

        if key == "up":
            return self.nav_up()
        elif key == "left":
            return self.nav_left()
        elif key == "right":
            return self.nav_right()
        elif key == '+' or key == '-' or key == '*' or key == '/' or key == '%'
            or key == '<' or key == '>' or key == '&' or key == '|' or key == '^'
            or key == 't' or key == 'v':
            return self.replace('v', key)
        elif key == "space":
            return self.play()
        elif key == "esc":
            return self.escape()

        return root

    def nav_up(self) -> Expression:
        if len(stack) == 0:
            return root
        root = stack.pop()
        return root

    def nav_left(self) -> Expression:
        if instance(root, Value) or instance(root, Var):
            return root
        root = root.left
        stack.append(root)
        return root

    def nav_right(self) -> Expression:
        if instance(root, Value) or instance(root, Var):
            return root
        root = root.right
        stack.append(root)
        return root

    def play(self) -> Expression:
        while len(stack) != 0:
            root = stack.pop()
        return root

    def escape(self) -> Expression:
        while len(stack) != 0:
            root = stack.pop()
        return root

    def replace(self, new_op_type: str, key: str) -> Expression:

        # 1. Val/Var -> Val/Var/Math
        if instance(root, Value) or instance(root, Var):
            root = self.v_to_math(key)

        # 2. Math -> Math
        if not instance(root, Value) and not instance(root, Var)
            and new_op_type != 'v':
            root = self.math_to_math(key)

        # 3. Math -> Val/Var
        if not instance(root, Value) and not instance(root, Var)
            and new_op_type == 'v':
            root = self.math_to_v(key)

        stack.pop()
        stack.append(root)

        return root

    def v_to_math(self, key: str) -> Expression:

        if key == '+':
            root = Add()
        elif key == '-':
            root = Sub()
        elif key == '*':
            root = Mult()
        elif key == '/':
            root = Div()
        elif key == '%':
            root = Mod()
        elif key == '<':
            root = ShiftLeft()
        elif key == '>':
            root = ShiftRight()
        elif key == '&':
            root = And()
        elif key == '|':
            root = Or()
        elif key == '^':
            root = Xor()
        elif key == 't':
            root = Var()
        elif key == 'v':
            root = Value()

        return root

    def math_to_math(self, key: str) -> Expression:
        left = root.left
        right = root.right
        root = v_to_math(key)
        root.left = left
        root.right = right

        return root

    def math_to_v(self, key: str) -> Expression:
        root.left = None
        root.right = None
        root = v_to_math(key)

        return root

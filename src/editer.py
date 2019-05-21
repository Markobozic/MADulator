from expression import *

class Editor():

    stack = None
    root = None

    def __init__(self):
        pass

    def new_key(self, key: int, function: Expression) -> Expression:
        root = function
        stack = function

        if key == Qt.Key_Up:
            return self.nav_up()
        elif key == Qt.Key_Left:
            return self.nav_left()
        elif key == Qt.Key_Right:
            return self.nav_right()
        elif key == Qt.Key_Plus or key == Qt.Key_Minus or key == Qt.Key_Asterisk
        or key == Qt.Key_Slash or key == Qt.Key_Percent or key == Qt.Key_Less
        or key == Qt.Key_Greater or key == Qt.Key_Ampersand or key == Qt.Key_Bar
        or key == Qt.Key_AsciiCircum:
            return self.replace('o', key)
        elif key == Qt.Key_T or key == Qt.Key_V:
            return self.replace('v', key)
        elif key == Qt.Key_Space:
            return self.play()
        elif key == Qt.Key_Excape:
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

    def replace(self, new_op_type: str, key: int) -> Expression:

        # 1. Val/Var -> Val/Var/Math
        if instance(root, Value) or instance(root, Var):
            root = self.v_to_math(key)

        # 2. Math -> Math
        if not instance(root, Value) and not instance(root, Var)
            and new_op_type == 'o':
            root = self.math_to_math(key)

        # 3. Math -> Val/Var
        if not instance(root, Value) and not instance(root, Var)
            and new_op_type == 'v':
            root = self.math_to_v(key)

        stack.pop()
        stack.append(root)

        return root

    def v_to_math(self, key: int) -> Expression:

        if key == Qt.Key_Plus:
            root = Add()
        elif key == Qt.Key_Minus:
            root = Sub()
        elif key == Qt.Key_Asterisk:
            root = Mult()
        elif key == Qt.Key_Slash:
            root = Div()
        elif key == Qt.Key_Percent:
            root = Mod()
        elif key == Qt.Key_Less:
            root = ShiftLeft()
        elif key == Qt.Key_Greater:
            root = ShiftRight()
        elif key == Qt.Key_Ampersand:
            root = And()
        elif key == Qt.Key_Bar:
            root = Or()
        elif key == Qt.Key_AsciiCircum:
            root = Xor()
        elif key == Qt.Key_T:
            root = Var()
        elif key == Qt.Key_V:
            root = Value()

        return root

    def math_to_math(self, key: int) -> Expression:
        left = root.left
        right = root.right
        root = v_to_math(key)
        root.left = left
        root.right = right

        return root

    def math_to_v(self, key: int) -> Expression:
        root.left = None
        root.right = None
        root = v_to_math(key)

        return root

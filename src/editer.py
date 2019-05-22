from expression import *
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg

class Editor():

    path = []                   # Keeps track of path from true root to current root
    root = None                 # Current root
    parent = []                 # Parent of current root

    def __init__(self):
        pass

    # Take in user command to navigate and edit function
    def new_key(self, key: QtCore.Qt.Key, function: Expression) -> Expression:
        root = function
        path.append(root)

        if key == Qt.Key_Up:
            return self.nav_up()
        elif key == Qt.Key_Left:
            return self.nav_left()
        elif key == Qt.Key_Right:
            return self.nav_right()
        elif (key == Qt.Key_Plus or key == Qt.Key_Minus or key == Qt.Key_Asterisk
            or key == Qt.Key_Slash or key == Qt.Key_Percent or key == Qt.Key_Less
            or key == Qt.Key_Greater or key == Qt.Key_Ampersand or key == Qt.Key_Bar
            or key == Qt.Key_AsciiCircum):
            return self.replace('o', key)
        elif key == Qt.Key_T or key == Qt.Key_V:
            return self.replace('v', key)
        elif key == Qt.Key_Space:
            return self.load_function()

        return root

    # Navigate back up to parent root
    def nav_up(self) -> Expression:
        if len(path) == 0:
            return root
        proot, child = parent.pop()
        if child == 'l':
            proot.set_left(root)
        else:
            proot.set_right(root)
        root = path.pop()
        return root

    # Navigate to left child
    def nav_left(self) -> Expression:
        if instance(root, Value) or instance(root, Var):
            return root
        parent.append((root, 'l'))
        root = root.get_left()
        path.append(root)
        return root

    # Navigate to right child
    def nav_right(self) -> Expression:
        if instance(root, Value) or instance(root, Var):
            return root
        parent.append((root, 'r'))
        root = root.get_right()
        path.append(root)
        return root

    # Navigate to the true root of the function
    def load_function(self) -> Expression:
        while len(path) != 0:
            self.nav_up()

        return root

    # Replace an expression with another expression
    def replace(self, new_op_type: str, key: QtCore.Qt.Key) -> Expression:

        # 1. Val/Var -> Val/Var/Math
        if instance(root, Value) or instance(root, Var):
            root = self.v_to_math(key)

        # 2. Math -> Math
        if (not instance(root, Value) and not instance(root, Var)
            and new_op_type == 'o'):
            root = self.math_to_math(key)

        # 3. Math -> Val/Var
        if (not instance(root, Value) and not instance(root, Var)
            and new_op_type == 'v'):
            root = self.math_to_v(key)

        # Set default children value for expressions that must have children
        if new_op_type == 'o':
            val = Value()
            val.set_number(1)
            if not root.get_left():
                root.set_left(val)
            if not root.get_right():
                root.set_right(val)

        # Update list to reflect updated expression node
        path.pop()
        path.append(root)

        return root

    # Change an expression with no children (Value or Var)
    # to one that may have children
    def v_to_math(self, key: QtCore.Qt.Key) -> Expression:

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

    # Change an expression that must have children to a new
    # expression that must have children (not Value or Var)
    def math_to_math(self, key: QtCore.Qt.Key) -> Expression:
        left = root.get_left()
        right = root.get_right()
        root = v_to_math(key)
        root.set_left(left)
        root.set_right(right)

        return root

    # Change an expression that must have children to a new
    # expression that does not have children (Value or Var)
    def math_to_v(self, key: QtCore.Qt.Key) -> Expression:
        root.set_left(None)
        root.set_left(None)
        root = v_to_math(key)

        return root

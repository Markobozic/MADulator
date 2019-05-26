from expression import *
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg

class Editor():

    path = []                   # Keeps track of path from true root to current root
    root = None                 # Current root
    parents = []                # List of parents of current root

    def __init__(self, function: Expression):
        self.root = function
        self.path.append(self.root)

    def get_function(self) -> Expression:
        count = 0
        for n in self.path:
            print(count, n)
            count = count + 1
        return self.path[0]

    def get_path(self) -> Expression:
        return self.root

    # Navigate to the true root of the function
    def load_function(self) -> Expression:
        while len(self.path) != 1:
            self.nav_up()

        return self.root

    # Create a value node with user input
    def create_value(self, val: int) -> None:
        self.root.set_left(None)
        self.root.set_left(None)

        self.root = Value()
        self.root.set_number(val)

        self.path.pop()
        self.path.append(self.root)

        if len(self.parents) != 0:
            parent, child_dir = self.parents[len(self.parents) - 1]
            child = self.root
            self.root = parent
            if child_dir == 'l':
                self.root.set_left(child)
            else:
                self.root.set_right(child)
            self.root = child

    # Take in user command to navigate and edit function
    def new_key(self, key: QtCore.Qt.Key) -> None:
        if key == QtCore.Qt.Key.Key_Up:
            self.nav_up()
        elif key == QtCore.Qt.Key.Key_Left:
            self.nav_left()
        elif key == QtCore.Qt.Key.Key_Right:
            self.nav_right()
        elif (key == QtCore.Qt.Key.Key_Plus or key == QtCore.Qt.Key.Key_Minus
            or key == QtCore.Qt.Key.Key_Asterisk or key == QtCore.Qt.Key.Key_Slash
            or key == QtCore.Qt.Key.Key_Percent or key == QtCore.Qt.Key.Key_Less
            or key == QtCore.Qt.Key.Key_Greater or key == QtCore.Qt.Key.Key_Ampersand
            or key == QtCore.Qt.Key.Key_Bar or key == QtCore.Qt.Key.Key_AsciiCircum):
            self.replace('o', key)
        elif key == QtCore.Qt.Key.Key_T:
            self.replace('v', key)

    # Navigate back up to parent root
    def nav_up(self) -> None:
        if len(self.parents) != 0:
            parent, child_dir = self.parents.pop()
            self.path.pop()
            self.root = parent
        else:
            self.path.pop()

    # Navigate to left child
    def nav_left(self) -> None:
        if not isinstance(self.root, Value) and not isinstance(self.root, Var):
            self.parents.append((self.root, 'l'))
            self.root = self.root.get_left()
            self.path.append(self.root)

    # Navigate to right child
    def nav_right(self) -> None:
        if not isinstance(self.root, Value) and not isinstance(self.root, Var):
            self.parents.append((self.root, 'r'))
            self.root = self.root.get_right()
            self.path.append(self.root)

    # Replace an expression with another expression
    def replace(self, new_op_type: str, key: QtCore.Qt.Key) -> None:

        # 1. Val/Var -> Val/Var/Math
        if isinstance(self.root, Value) or isinstance(self.root, Var):
            self.v_to_math(key)

        # 2. Math -> Math
        if (not isinstance(self.root, Value) and not isinstance(self.root, Var)
            and new_op_type == 'o'):
            self.math_to_math(key)

        # 3. Math -> Var
        if (not isinstance(self.root, Value) and not isinstance(self.root, Var)
            and new_op_type == 'v'):
            self.math_to_v(key)

        # Set default children value for expressions that must have children
        if new_op_type == 'o':
            val = Value()
            val.set_number(1)
            if not self.root.get_left():
                self.root.set_left(val)
            if not self.root.get_right():
                self.root.set_right(val)

        # Update list to reflect updated expression node
        self.path.pop()
        self.path.append(self.root)

        if len(self.parents) != 0:
            parent, child_dir = self.parents[len(self.parents) - 1]
            child = self.root
            self.root = parent
            if child_dir == 'l':
                self.root.set_left(child)
            else:
                self.root.set_right(child)
            self.root = child

    # Change an expression with no children (Value or Var)
    # to one that may have children
    def v_to_math(self, key: QtCore.Qt.Key) -> None:

        if key == QtCore.Qt.Key.Key_Plus:
            self.root = Add()
        elif key == QtCore.Qt.Key.Key_Minus:
            self.root = Sub()
        elif key == QtCore.Qt.Key.Key_Asterisk:
            self.root = Mult()
        elif key == QtCore.Qt.Key.Key_Slash:
            self.root = Div()
        elif key == QtCore.Qt.Key.Key_Percent:
            self.root = Mod()
        elif key == QtCore.Qt.Key.Key_Less:
            self.root = ShiftLeft()
        elif key == QtCore.Qt.Key.Key_Greater:
            self.root = ShiftRight()
        elif key == QtCore.Qt.Key.Key_Ampersand:
            self.root = BitAnd()
        elif key == QtCore.Qt.Key.Key_Bar:
            self.root = BitOr()
        elif key == QtCore.Qt.Key.Key_AsciiCircum:
            self.root = BitXor()
        elif key == QtCore.Qt.Key.Key_T:
            self.root = Var()

    # Change an expression that must have children to a new
    # expression that must have children (not Value or Var)
    def math_to_math(self, key: QtCore.Qt.Key) -> None:
        left = self.root.get_left()
        right = self.root.get_right()
        self.v_to_math(key)
        self.root.set_left(left)
        self.root.set_right(right)

    # Change an expression that must have children to a new
    # expression of type Var
    def math_to_v(self, key: QtCore.Qt.Key) -> None:
        self.root.set_left(None)
        self.root.set_left(None)
        self.root = Var()

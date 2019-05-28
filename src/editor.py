from expression import *
from pyqtgraph.Qt import QtCore

class Editor():

    path = []                   # Keeps track of path from true root to current root
    root = None                 # Current root

    def __init__(self, function: Expression):
        self.root = function
        self.path.append(self.root)

    # Updates the function
    def set_function(self, function: Expression):
        self.root = function
        self.path.clear()
        self.path.append(self.root)

    # Return the current function
    def get_function(self) -> Expression:
        return self.path[0]

    # Return the current selection
    def get_selection(self) -> Expression:
        return self.root

    # Navigate to the true root of the function
    def load_function(self) -> Expression:
        while len(self.path) != 1:
            self.nav_up()

        return self.root

    # Connect parent and child nodes
    def connect_nodes(self, new_node: Expression) -> None:
        if not len(self.path) == 1:
            parent = self.path[len(self.path) - 2]
            if parent.get_left() == self.root:
                parent.set_left(new_node)
            if parent.get_right() == self.root:
                parent.set_right(new_node)
        self.path.pop()
        self.path.append(new_node)
        self.root = new_node

    # Create a value node with user input
    def create_value(self, val: int) -> None:
        new_node = Value()
        new_node.set_number(val)

        self.connect_nodes(new_node)

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
        if len(self.path) > 1:
            self.path.pop()
            self.root = self.path[len(self.path) - 1]

    # Navigate to left child
    def nav_left(self) -> None:
        if not isinstance(self.root, Value) and not isinstance(self.root, Var):
            self.root = self.root.get_left()
            self.path.append(self.root)

    # Navigate to right child
    def nav_right(self) -> None:
        if not isinstance(self.root, Value) and not isinstance(self.root, Var):
            self.root = self.root.get_right()
            self.path.append(self.root)

    # Replace an expression with another expression
    def replace(self, new_op_type: str, key: QtCore.Qt.Key) -> None:
        new_node = None

        # 1. Val/Var -> Val/Var/Math
        if isinstance(self.root, Value) or isinstance(self.root, Var):
            new_node = self.v_to_math(key)

        # 2. Math -> Math
        if (not isinstance(self.root, Value) and not isinstance(self.root, Var)
            and new_op_type == 'o'):
            new_node = self.math_to_math(key)

        # 3. Math -> Var
        if (not isinstance(self.root, Value) and not isinstance(self.root, Var)
            and new_op_type == 'v'):
            new_node = Var()

        # Set default children value for expressions that must have children
        if new_op_type == 'o':
            if not new_node.get_left():
                new_node.set_left(Value())
            if not new_node.get_right():
                new_node.set_right(Value())

        self.connect_nodes(new_node)

    # Change an expression with no children (Value or Var)
    # to one that may have children
    def v_to_math(self, key: QtCore.Qt.Key) -> Expression:
        new_node = None

        if key == QtCore.Qt.Key.Key_Plus:
            new_node = Add()
        elif key == QtCore.Qt.Key.Key_Minus:
            new_node = Sub()
        elif key == QtCore.Qt.Key.Key_Asterisk:
            new_node = Mult()
        elif key == QtCore.Qt.Key.Key_Slash:
            new_node = Div()
        elif key == QtCore.Qt.Key.Key_Percent:
            new_node = Mod()
        elif key == QtCore.Qt.Key.Key_Less:
            new_node = ShiftLeft()
        elif key == QtCore.Qt.Key.Key_Greater:
            new_node = ShiftRight()
        elif key == QtCore.Qt.Key.Key_Ampersand:
            new_node = BitAnd()
        elif key == QtCore.Qt.Key.Key_Bar:
            new_node = BitOr()
        elif key == QtCore.Qt.Key.Key_AsciiCircum:
            new_node = BitXor()
        elif key == QtCore.Qt.Key.Key_T:
            new_node = Var()

        return new_node

    # Change an expression that must have children to a new
    # expression that must have children (not Value or Var)
    def math_to_math(self, key: QtCore.Qt.Key) -> Expression:
        new_node = self.v_to_math(key)
        new_node.set_left(self.root.get_left())
        new_node.set_right(self.root.get_right())

        return new_node

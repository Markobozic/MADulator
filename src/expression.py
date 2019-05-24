class Expression:

    left = None
    right = None

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        pass

    def set_left(self, expression: 'Expression') -> None:
        self.left = expression

    def set_right(self, expression: 'Expression') -> None:
        self.right = expression

    def get_left(self) -> 'Expression':
        return self.left

    def get_right(self) -> 'Expression':
        return self.right

    def html_tree(self, path: list) -> str:
        depth = len(path)
        if depth == 0:
            return ''
        selected = path[depth - 1]
        return '<code>' + self.html_tree_node(path, selected) + '</code>'

    def html_tree_node(self, path: list, selected: 'Expression') -> str:
        html = ''
        if self == selected:
            html = html + '<span style="color:white">'
        html = html + '('
        if self == selected:
            html = html + '</span>'
        if self.left is not None:
            if self.left in path:
                html = html + '<span style="color:gray">' + self.left.html_tree_node(path, selected) + '</span>'
            else:
                html = html + str(self.left)
        if self == selected:
            html = html + '<strong style="color:white"> ' + self.op() + ' </strong>'
        else:
            html = html + self.op()
        if self.right is not None:
            if self.right in path:
                html = html + '<span style="color:gray">' + self.right.html_tree_node(path, selected) + '</span>'
            else:
                html = html + str(self.left)
        if self == selected:
            html = html + '<span style="color:white">'
        html = html + ')'
        if self == selected:
            html = html + '</span>'
        return html

class Value(Expression):

    number = 1

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.number

    def set_number(self, num: int) -> None:
        self.number = num

    def op(self) -> str:
        return str(self.number)

    def __str__(self) -> str:
        return str(self.number)

class Add(Expression):
    
    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) + self.right.eval(t)

    def op(self) -> str:
        return '+'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' + ' + str(self.right) + ')'

class Sub(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) - self.right.eval(t)

    def op(self) -> str:
        return '-'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' - ' + str(self.right) + ')'

class Mult(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) * self.right.eval(t)

    def op(self) -> str:
        return '*'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' * ' + str(self.right) + ')'


class Div(Expression):
    '''This does floor division, but in the case it detects that the denominator
    will be zero, it reuses the denominator from the previous eval call.'''

    previous_right_result = 1

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        right_result = self.right.eval(t)
        if right_result == 0:
            return self.left.eval(t) // self.previous_right_result
        self.previous_right_result = right_result
        return self.left.eval(t) // right_result

    def op(self) -> str:
        return '/'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' / ' + str(self.right) + ')'

class Var(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return t

    def op(self) -> str:
        return 't'

    def __str__(self) -> str:
        return 't'

class ShiftLeft(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) << (self.right.eval(t) % 32)

    def op(self) -> str:
        return '&lt;&lt;'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' &lt;&lt; ' + str(self.right) + ')'

class ShiftRight(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) >> (self.right.eval(t) % 32)

    def op(self) -> str:
        return '>>'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' >> ' + str(self.right) + ')'

class Mod(Expression):

    previous_right_result = 1

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        right_result = self.right.eval(t)
        if right_result == 0:
            return self.left.eval(t) % self.previous_right_result
        self.previous_right_result = right_result
        return self.left.eval(t) % right_result

    def op(self) -> str:
        return '%'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' % ' + str(self.right) + ')'

class BitAnd(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) & self.right.eval(t)

    def op(self) -> str:
        return '&'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' & ' + str(self.right) + ')'

class BitOr(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) | self.right.eval(t)

    def op(self) -> str:
        return '|'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' | ' + str(self.right) + ')'

class BitXor(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) ^ self.right.eval(t)

    def op(self) -> str:
        return '^'

    def __str__(self) -> str:
        return '(' + str(self.left) + ' ^ ' + str(self.right) + ')'

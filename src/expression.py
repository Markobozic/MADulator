class Expression:

    left = None
    right = None

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        pass

    def set_left(self, expression: 'Expression'):
        self.left = expression

    def set_right(self, expression: 'Expression'):
        self.right = expression


class Value(Expression):

    number = 1

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.number

    def set_number(self, num: int) -> None:
        self.number = num

    def __str__(self) -> str:
        return str(self.number)

class Add(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) + self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' + ' + str(self.right) + ')'

class Sub(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) - self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' - ' + str(self.right) + ')'

class Mult(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) * self.right.eval(t)

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

    def __str__(self) -> str:
        return '(' + str(self.left) + ' / ' + str(self.right) + ')'

class Var(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return t

    def __str__(self) -> str:
        return 't'

class ShiftLeft(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) << (self.right.eval(t) % 32)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' &lt;&lt; ' + str(self.right) + ')'

class ShiftRight(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) >> (self.right.eval(t) % 32)

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

    def __str__(self) -> str:
        return '(' + str(self.left) + ' % ' + str(self.right) + ')'

class BitAnd(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) & self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' & ' + str(self.right) + ')'

class BitOr(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) | self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' | ' + str(self.right) + ')'

class BitXor(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) ^ self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' ^ ' + str(self.right) + ')'

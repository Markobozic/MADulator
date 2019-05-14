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
        return number

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

    previous = 1

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        if self.right == 0:
            return previous
        previous = self.left.eval(t)/self.right.eval(t)
        return int(previous)

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
        return self.left.eval(t) << self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' << ' + str(self.right) + ')'

class ShiftRight(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) >> self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' >> ' + str(self.right) + ')'

class Mod(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t) % self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' % ' + str(self.right) + ')'

class Pow(Expression):

    def __init__(self):
        pass

    def eval(self, t: int) -> int:
        return self.left.eval(t)**self.right.eval(t)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' ^ ' + str(self.right) + ')'

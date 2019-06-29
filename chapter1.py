from dataclasses import dataclass

@dataclass
class Number():
    value: object

    @classmethod
    def is_reducible(cls):
        return False

    def __str__(self):
        return str(self.value)


@dataclass
class Add():
    left: object
    right: object

    @classmethod
    def is_reducible(cls):
        return True

    def reduce(self, environment):
        if self.left.is_reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)

    def __str__(self):
        return f'{str(self.left)} + {str(self.right)}'


@dataclass
class Multiply():
    left: object
    right: object

    @classmethod
    def is_reducible(cls):
        return True

    def reduce(self, environment):
        if self.left.is_reducible():
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)

    def __str__(self):
        return f'{str(self.left)} * {str(self.right)}'


@dataclass
class Boolean():
    value: object

    @classmethod
    def is_reducible(self):
        return False

    def __str__(self):
        return f'{self.value}'


@dataclass
class LessThan():
    left: object
    right: object

    @classmethod
    def is_reducible(cls):
        return True

    def reduce(self, environment):
        if self.left.is_reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def __str__(self):
        return f'{str(self.left)} < {str(self.right)}'


@dataclass
class Variable():
    name: object

    @classmethod
    def is_reducible(cls):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def __str__(self):
        return f'{self.name}'


@dataclass
class DoNothing():
    @classmethod
    def is_reducible(self):
        return False

    def __str__(self):
        return 'do-nothing'


@dataclass
class Assign():
    name: object
    expression: object

    @classmethod
    def is_reducible(self):
        return True

    def reduce(self, environment):
        if self.expression.is_reducible():
            return Assign(self.name, self.expression.reduce(environment)), environment
        else:
            return DoNothing(), { **environment, self.name: self.expression }

    def __str__(self):
        return f'{self.name} = {self.expression}'


class Machine():
    def __init__(self, statment, environment):
        self.statment = statment
        self.environment = environment

    def step(self):
        self.statment, self.environment = self.statment.reduce(self.environment)

    def run(self):
        while self.statment.is_reducible():
            print(f'{self.statment}, {self.environment}')
            self.step()
        print(f'{self.statment}, {self.environment}')


if __name__ == '__main__':
    Machine(Assign("x", Add(Variable("x"), Number(1))), { "x": Number(2)}).run()

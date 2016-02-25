from State import *

class Parser:
    """
    Wrapper object of a function of type:
    State -> (Lexeme, State)
    """

    def __init__(self, f):
        # Parser with the function to execute when invoked
        setattr(self, 'run', f)

    def define(self, p):
        # Define the parser function
        setattr(self, 'run', p.run)
        return self

    def __or__(self, other):
        # parser, parser -> parser
        def _or(state):
            a = self.run(state)
            if a is not None:
                return a

            b = other.run(state)
            if b is not None:
                return b

            return None
        return Parser(_or)

    def __and__(self, other):
        # parser, parser -> parser
        def _and(state):
            a = self.run(state)
            if a is None:
                return None
            (lexemeA, a) = a

            b = other.run(a)
            if b is None:
                return None
            (lexemeB, b) = b

            return lexemeA + lexemeB, a + b
        return Parser(_and)

    def __rshift__(self, f):
        # parser, function -> parser
        # (State) -> (f(lexeme), State)
        def _rshift(state):
            a = self.run(state)
            if a is None:
                return None
            (lexeme, s) = a
            return f(lexeme), s

        return Parser(_rshift)

    def parse(self, sequence):
        # string -> (Lexeme, State)
        return self.run(State(sequence, 0))
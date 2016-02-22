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


class Lexeme:
    def __init__(self, data, start, end):
        self.token = data
        self.start = start
        self.end = end
        self.prefix_comments = []
        self.type = 0

    def __repr__(self):
        return "L({0} @ [{1}, {2}) => {3}) ".format(self.token, self.start, self.end, self.children)

    def __add__(self, other):
        token = u""
        if other.token is None:
            token = self.token
        elif self.token is None:
            token = other.token
        else:
            token = self.token + other.token
        return Lexeme(token, self.start, other.end)


class State:
    def __init__(self, sequence, end):
        self.input = sequence
        self.index = end

    def __repr__(self):
        return "S({0})".format(self.index)

    def __add__(self, other):
        return State(self.input, max(self.index, other.index))

    def __rshift__(self, increment):
        return State(self.input, self.index + increment)

    def __lshift__(self, decrement):
        return State(self.input, self.index - decrement)


def a(literal):
    def _match(state):
        if state.index < len(state.input) and state.input[state.index] == literal:
            return Lexeme(literal, state.index, state.index + 1), state >> 1
        return None
    return Parser(_match)


def match(sequence):
    options = tuple([a(l) for l in sequence])
    return every(*options)


def between(lower, upper):
    # given a lower and upper limit, return a (Lexeme, State) if the current character of the input it's between
    # the given bounds.
    # Returns the current characters as a lexeme.
    def _between(state):
        if state.index < len(state.input) and lower <= state.input[state.index] <= upper:
            return Lexeme(state.input[state.index], state.index, state.index + 1), state >> 1
        return None
    return Parser(_between)


def repeat(parser, until):
    def _repeat(state):
        result = empty(state)
        while until.run(state) is None:
            s = parser.run(state)
            if s is None:
                return None
            (lexeme, state) = s
            result = result[0] + lexeme, result[1] + state
        return result
    return Parser(_repeat)


def empty(state):
    return Lexeme(None, 0, 0), state


def skip(parser):
    def _skip(state):
        (l, s) = many(parser).run(state)
        return empty(s)
    return Parser(_skip)


def maybe(parser):
    def _maybe(state):
        a = parser.run(state)
        if a is not None:
            return a
        return empty(state)
    return Parser(_maybe)


def many(parser):
    def _many(state):
        result = empty(state)
        while True:
            a = parser.run(state)
            if a is None:
                return result
            (lexeme, state) = a
            result = result[0] + lexeme, result[1] + state
    return Parser(_many)


def at_least_one(parser):
    return parser & many(parser)


def one_of(*options):
    if len(options) == 0:
        return None
    if len(options) == 1:
        return options[0]
    return options[0] | one_of(*options[1:])


def every(*options):
    if len(options) == 0:
        return None
    if len(options) == 1:
        return options[0]
    return options[0] & every(*options[1:])


def forward_decl():
    def f(state):
        raise Exception('Forward declarations has to be defined on the parser')
    return Parser(f)
class Parser:
    """
    Wrapper object of a function of type:
    (Lexeme, State) -> (Lexeme, State)
    """
    def __init__(self, f):
        setattr(self, 'run', f)

    def define(self, p):
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
        def _rshift(state):
            (lexeme, s) = self.run(state)
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

    def __repr__(self):
        return "L({0} @ [{1}, {2}))".format(self.token, self.start, self.end)

    def __add__(self, other):
        str = u""
        if other.token is None:
            str = self.token
        elif self.token is None:
            str = other.token
        else:
            str = self.token + other.token
        return Lexeme(str, self.start, other.end)


class State:
    def __init__(self, sequence, end):
        self.input = sequence
        self.index = end

    def __repr__(self):
        return "S({0})".format(self.index)

    def __add__(self, other):
        return State(self.input, max(self.index, other.index))


def a(literal):
    def _match(state):
        if state.index < len(state.input) and state.input[state.index] == literal:
            return Lexeme(literal, state.index, state.index + 1), State(state.input, state.index + 1)
        return None

    return Parser(_match)


def between(lower, upper):
    # given a lower and upper limit, return a (Lexeme, State) if the current character of the input it's between
    # the given bounds.
    # Returns the current characters as a lexeme.
    def _between(state):
        if state.index < len(state.input) and state.input[state.index] >= lower and state.input[state.index] <= upper:
            return Lexeme(state.input[state.index], state.index, state.index + 1), State(state.input, state.index + 1)
        return None

    return Parser(_between)


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
        return None
    return Parser(_many)


def at_least_one(parser):
    return parser & many(parser)


def any(options):
    if len(options) == 0:
        return None
    if len(options) == 1:
        return options[0]
    return options[0] | any(options[1:])


def every(options):
    if len(options) == 0:
        return None
    if len(options) == 1:
        return options[0]
    return options[0] & all(options[1:])


def forward_decl():
    def f(state):
        raise Exception('Forward declarations has to be defined on the parser')
    return Parser(f)

if __name__ == "__main__":
    import string

    parser = a("a")
    assert parser.parse('a')
    assert parser.parse('b') is None

    parser = a("a") & a("b")
    assert parser.parse('ab')
    assert parser.parse('ba') is None

    parser = a('a') | a('b')
    assert parser.parse('a')
    assert parser.parse('b')
    assert parser.parse('c') is None

    parser = between('a', 'c')
    assert parser.parse('a')
    assert parser.parse('b')
    assert parser.parse('c')
    assert parser.parse('d') is None

    parser = maybe(a('a'))
    assert parser.parse('a')
    assert parser.parse('b')[0].token is None

    parser = at_least_one(a("a"))
    assert parser.parse('a')
    print parser.parse('aaaa')[0]
    assert parser.parse('aaaa')[0].token == "aaaa"
    assert parser.parse('b') is None

    parser = a("a") >> (lambda x: Lexeme(string.upper(x.token), x.start, x.end))
    assert parser.parse('a')[0].token == 'A'

    parser = skip(any([a(" "), a("\t"), a("\n")])) & a("a")
    assert parser.parse("   a")[0].token == 'a'

    # (comments >> push) & skip(whitespaces)


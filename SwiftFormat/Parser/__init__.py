from Parser import *
from Lexeme import *
from State import *


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
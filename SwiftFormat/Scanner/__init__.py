import struct


class SwiftTypes:
    IDENTIFIER = 1
    IMPLICIT_PARAMETER = 1 << 1
    LITERAL_STRING = 1 << 2
    LITERAL_INTEGER_BINARY = 1 << 3
    LITERAL_INTEGER_OCTAL = 1 << 4
    LITERAL_INTEGER_DECIMAL = 1 << 5
    LITERAL_INTEGER_HEXADECIMAL = 1 << 6
    LITERAL_FLOATING_DECIMAL = 1 << 7
    LITERAL_FLOATING_HEXADECIMAL = 1 << 8
    LITERAL_BOOLEAN = 1 << 9
    LITERAL_NIL = 1 << 10
    KEYWORD_DECLARATION = 1 << 10
    KEYWORD_STATEMENT = 1 << 11
    KEYWORD_EXPRESSION_TYPES = 1 << 12
    KEYWORD_PATTERNS = 1 << 13
    KEYWORD_RESERVED = 1 << 14
    PUNCTUATION = 1 << 15


def unichar(i):
    try:
        return unichr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')
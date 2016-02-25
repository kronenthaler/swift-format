from SwiftFormat.Parser import *
from SwiftFormat.Scanner import *

"""
literal ::= numeric-literal | string-literal | boolean-literal | nil-literal
numeric-literal ::= [-]integer-literal | [-]floating-point-literal
boolean-literal ::= true | false
nil-literal ::= nil

integer-literal ::= binary-literal
integer-literal ::= octal-literal
integer-literal ::= decimal-literal
integer-literal ::= hexadecimal-literal

binary-literal ::= 0b binary-digit {binary-literal-character}
binary-digit ::= Digit 0 or 1
binary-literal-character ::= binary-digit | _

octal-literal ::= 0o octal-digit {octal-literal-character}
octal-digit ::= Digit 0 through 7
octal-literal-character ::= octal-digit | _

decimal-literal ::= decimal-digit {decimal-literal-character}
decimal-digit ::= Digit 0 through 9
decimal-literal-character ::= decimal-digit | _

hexadecimal-literal ::= 0x hexadecimal-digit {hexadecimal-literal-character}
hexadecimal-digit ::= Digit 0 through 9, a through f, or A through F
hexadecimal-literal-character ::= hexadecimal-digit | _

floating-point-literal ::= decimal-literal [decimal-fraction] [decimal-exponent]
floating-point-literal ::= hexadecimal-literal [hexadecimal-fraction] hexadecimal-exponent
decimal-fraction ::= . decimal-literal
decimal-exponent ::= floating-point-e [sign] decimal-literal
hexadecimal-fraction ::= . hexadecimal-digit [hexadecimal-literal-characters]
hexadecimal-exponent ::= floating-point-p [sign] decimal-literal
floating-point-e ::= e | E
floating-point-p ::= p | P
sign ::= + | -

string-literal ::= static-string-literal | interpolated-string-literal
static-string-literal ::= "[quoted-text]"
quoted-text ::= quoted-text-item [quoted-text]
quoted-text-item ::= escaped-character
quoted-text-item ::= Any Unicode scalar value except ", \, U+000A, or U+000D
interpolated-string-literal ::= "[interpolated-text]"
interpolated-text ::= interpolated-text-item [interpolated-text]
interpolated-text-item ::= \(expression) | quoted-text-item
escaped-character ::= \0 | \\ | \t | \n | \r | \" | \'
escaped-character ::= \u{unicode-scalar-digits}
unicode-scalar-digits ::= Between one and eight hexadecimal digits
"""


def literal():
    return _numeric_literal() | _boolean_literal() | _nil_literal() # | _string_literal()


def _nil_literal():
    return match(u"nil") >> set_type(SwiftTypes.LITERAL_NIL)


def _boolean_literal():
    return (match(u"true") | match(u"false")) >> set_type(SwiftTypes.LITERAL_BOOLEAN)


def _numeric_literal():
    integer = maybe(a(u"-")) & _integer_literal()
    floating = maybe(a(u"-")) & _floating_point_literal()
    return integer # | floating


def _integer_literal():
    binary_digit = between(u"0", u"1")
    binary = match(u"0b") & binary_digit & many(binary_digit | a(u"_"))
    binary >>= set_type(SwiftTypes.LITERAL_INTEGER_BINARY)

    octal_digit = between(u"0", u"7")
    octal = match(u"0o") & octal_digit & many(octal_digit | a(u"_"))
    octal >>= set_type(SwiftTypes.LITERAL_INTEGER_OCTAL)

    decimal_digit = between(u"0", u"9")
    decimal = decimal_digit & many(decimal_digit | a(u"_"))
    decimal >>= set_type(SwiftTypes.LITERAL_INTEGER_DECIMAL)

    hexadecimal_digit = between(u"0", u"9") | between(u"a", u"f") | between(u"A", u"F")
    hexadecimal = match(u"0x") & hexadecimal_digit & many(hexadecimal_digit | a(u"_"))
    hexadecimal >>= set_type(SwiftTypes.LITERAL_INTEGER_HEXADECIMAL)

    return binary | octal | decimal | hexadecimal


def _floating_point_literal():
    return None


def _string_literal():
    return None

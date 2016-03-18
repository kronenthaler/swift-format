from SwiftFormat.Parser import *
from SwiftFormat.Scanner import *

# literal ::= numeric-literal | string-literal | boolean-literal | nil-literal
# numeric-literal ::= [-]integer-literal | [-]floating-point-literal
# boolean-literal ::= true | false
# nil-literal ::= nil
#
# integer-literal ::= binary-literal
# integer-literal ::= octal-literal
#
# binary-literal ::= 0b binary-digit {binary-literal-character}
# binary-digit ::= Digit 0 or 1
# binary-literal-character ::= binary-digit | _
#
# octal-literal ::= 0o octal-digit {octal-literal-character}
# octal-digit ::= Digit 0 through 7
# octal-literal-character ::= octal-digit | _
#
# floating-point-literal ::= decimal-literal [decimal-fraction] [decimal-exponent]
# decimal-literal ::= decimal-digit {decimal-literal-character}
# decimal-digit ::= Digit 0 through 9
# decimal-literal-character ::= decimal-digit | _
# decimal-fraction ::= . decimal-literal
# decimal-exponent ::= floating-point-e [sign] decimal-literal
#
# floating-point-literal ::= hexadecimal-literal [hexadecimal-fraction] hexadecimal-exponent
# hexadecimal-literal ::= 0x hexadecimal-digit {hexadecimal-literal-character}
# hexadecimal-digit ::= Digit 0 through 9, a through f, or A through F
# hexadecimal-literal-character ::= hexadecimal-digit | _
# hexadecimal-fraction ::= . hexadecimal-digit {hexadecimal-literal-character}
# hexadecimal-exponent ::= floating-point-p [sign] decimal-literal
#
# floating-point-e ::= e | E
# floating-point-p ::= p | P
# sign ::= + | -
#
# string-literal ::= static-string-literal | interpolated-string-literal
# static-string-literal ::= "[quoted-text]"
# quoted-text ::= quoted-text-item [quoted-text]
# quoted-text-item ::= escaped-character
# quoted-text-item ::= Any Unicode scalar value except ", \, U+000A, or U+000D
# interpolated-string-literal ::= "[interpolated-text]"
# interpolated-text ::= interpolated-text-item [interpolated-text]
# interpolated-text-item ::= \(expression) | quoted-text-item
# escaped-character ::= \0 | \\ | \t | \n | \r | \" | \'
# escaped-character ::= \u{unicode-scalar-digits}
# unicode-scalar-digits ::= Between one and eight hexadecimal digits


def literal():
    return _numeric_literal() | _boolean_literal() | _nil_literal() | _string_literal()


def _nil_literal():
    return match(u"nil") >> set_type(SwiftTypes.LITERAL_NIL)


def _boolean_literal():
    return (match(u"true") | match(u"false")) >> set_type(SwiftTypes.LITERAL_BOOLEAN)


def _numeric_literal():
    integer = maybe(a(u"-")) & _integer_literal()
    floating = maybe(a(u"-")) & _floating_point_literal()
    return longest(integer, floating)


def _integer_literal():
    binary_digit = between(u"0", u"1")
    binary = match(u"0b") & binary_digit & many(binary_digit | a(u"_"))
    binary >>= set_type(SwiftTypes.LITERAL_INTEGER_BINARY)

    octal_digit = between(u"0", u"7")
    octal = match(u"0o") & octal_digit & many(octal_digit | a(u"_"))
    octal >>= set_type(SwiftTypes.LITERAL_INTEGER_OCTAL)

    return binary | octal | _hexadecimal_literal() | _decimal_literal()


def _decimal_literal():
    decimal_digit = between(u"0", u"9")
    decimal = decimal_digit & many(decimal_digit | a(u"_"))
    decimal >>= set_type(SwiftTypes.LITERAL_INTEGER_DECIMAL)
    return decimal


def _hexadecimal_digit():
    return between(u"0", u"9") | between(u"a", u"f") | between(u"A", u"F")


def _hexadecimal_character():
    return _hexadecimal_digit() & many(_hexadecimal_digit() | a(u"_"))


def _hexadecimal_literal():
    hexadecimal = match(u"0x") & _hexadecimal_character()
    hexadecimal >>= set_type(SwiftTypes.LITERAL_INTEGER_HEXADECIMAL)
    return hexadecimal


def _floating_point_literal():
    float_point_e = a(u"e") | a(u"E")
    float_point_p = a(u"p") | a(u"P")
    sign = a(u"+") | a(u"-")

    decimal_fraction = a(u".") & _decimal_literal()
    decimal_exponent = float_point_e & maybe(sign) & _decimal_literal()
    decimal_floating_literal = _decimal_literal() & maybe(decimal_fraction) & maybe(decimal_exponent)
    decimal_floating_literal >>= set_type(SwiftTypes.LITERAL_FLOATING_DECIMAL)

    hexadecimal_fraction = a(u".") & _hexadecimal_character()
    hexadecimal_exponent = float_point_p & maybe(sign) & _decimal_literal()
    hexadecimal_floating_literal = _hexadecimal_literal() & maybe(hexadecimal_fraction) & hexadecimal_exponent
    hexadecimal_floating_literal >>= set_type(SwiftTypes.LITERAL_FLOATING_HEXADECIMAL)

    return longest(hexadecimal_floating_literal, decimal_floating_literal)


def _string_literal():
    # string-literal ::= static-string-literal | interpolated-string-literal
    # static-string-literal ::= "[quoted-text]"
    # quoted-text ::= quoted-text-item [quoted-text]
    # quoted-text-item ::= escaped-character
    # quoted-text-item ::= Any Unicode scalar value except ", \, U+000A, or U+000D
    # interpolated-string-literal ::= "[interpolated-text]"
    # interpolated-text ::= interpolated-text-item [interpolated-text]
    # interpolated-text-item ::= \(expression) | quoted-text-item
    # escaped-character ::= \0 | \\ | \t | \n | \r | \" | \'
    # escaped-character ::= \u{unicode-scalar-digits}
    # unicode-scalar-digits ::= Between one and eight hexadecimal digits

    return (_static_string_literal() | _interpolated_string_literal()) >> set_type(SwiftTypes.LITERAL_STRING)


def _static_string_literal():
    return a(u"\"") & many(_quoted_text_item()) & a(u"\"")


def _quoted_text_item():
    escaped_character = one_of(match(u"\\0"), match(u"\\\\"), match(u"\\t"),
                               match(u"\\n"), match(u"\\r"), match(u"\\\""), match(u"\\'")) | \
                        (match(u"\\u{") & up_to(_hexadecimal_digit(), 8) & a(u"}"))

    return escaped_character | anything(u'"', u"\\", u"\n", u"\r")


def _interpolated_string_literal():
    interpolated_text = (match(u"\\(") & expression() & a(u")")) | _quoted_text_item()
    return a(u"\"") & many(interpolated_text) & a(u"\"")


def expression():
    # TODO: remove this placeholder when the syntax handler is created
    return many(anything(u")"))
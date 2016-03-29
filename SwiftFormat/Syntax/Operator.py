from SwiftFormat.Parser import *
from SwiftFormat.Scanner import *

# operator ::= operator-head [operator-characters]
# operator ::= dot-operator-head dot-operator-characters
# operator-head ::= / | = | - | + | ! | * | % | < | > | & | | | ^ | ~ | ?
# operator-head ::= U+00A1-U+00A7
# operator-head ::= U+00A9 or U+00AB
# operator-head ::= U+00AC or U+00AE
# operator-head ::= U+00B0-U+00B1, U+00B6, U+00BB, U+00BF, U+00D7, or U+00F7
# operator-head ::= U+2016-U+2017 or U+2020-U+2027
# operator-head ::= U+2030-U+203E
# operator-head ::= U+2041-U+2053
# operator-head ::= U+2055-U+205E
# operator-head ::= U+2190-U+23FF
# operator-head ::= U+2500-U+2775
# operator-head ::= U+2794-U+2BFF
# operator-head ::= U+2E00-U+2E7F
# operator-head ::= U+3001-U+3003
# operator-head ::= U+3008-U+3030
# operator-character ::= operator-head
# operator-character ::= U+0300-U+036F
# operator-character ::= U+1DC0-U+1DFF
# operator-character ::= U+20D0-U+20FF
# operator-character ::= U+FE00-U+FE0F
# operator-character ::= U+FE20-U+FE2F
# operator-character ::= U+E0100-U+E01EF
# operator-characters ::= operator-character [operator-characters]
# dot-operator-head ::= .
# dot-operator-character ::= . | operator-character
# dot-operator-characters ::= dot-operator-character [dot-operator-characters]

# binary-operator ::= operator
# prefix-operator ::= operator
# postfix-operator ::= operator


def binary_operator():
    return operator()


def prefix_operator():
    return operator()


def postfix_operator():
    return operator()


def operator():
    op = (_operator_head() & many(_operator_character())) | (_dot_operator_head() & _dot_operator_characters())
    return op >> set_type(SwiftTypes.OPERATOR)


def _operator_head():
    return one_of(a(u"/"), a(u"="), a(u"-"), a(u"+"), a(u"!"), a(u"*"), a(u"%"), a(u"<"), a(u">"), a(u"&"), a(u"^"),
                  a(u"~"), a(u"?"), a(u"|")) | \
            a(unichar(0x00A9)) | a(unichar(0x00AB)) | \
            a(unichar(0x00AC)) | a(unichar(0x00AE)) | \
            a(unichar(0x00B6)) | a(unichar(0x00BB)) | \
            a(unichar(0x00BF)) | a(unichar(0x00D7)) | a(unichar(0x00F7)) | \
            between(unichar(0x00A1),unichar(0x00A7)) | \
            between(unichar(0x00B0),unichar(0x00B1)) | \
            between(unichar(0x2016),unichar(0x2017)) | \
            between(unichar(0x2020),unichar(0x2027)) | \
            between(unichar(0x2030),unichar(0x203E)) | \
            between(unichar(0x2041),unichar(0x2053)) | \
            between(unichar(0x2055),unichar(0x205E)) | \
            between(unichar(0x2190),unichar(0x23FF)) | \
            between(unichar(0x2500),unichar(0x2775)) | \
            between(unichar(0x2794),unichar(0x2BFF)) | \
            between(unichar(0x2E00),unichar(0x2E7F)) | \
            between(unichar(0x3001),unichar(0x3003)) | \
            between(unichar(0x3008),unichar(0x3030))


def _operator_character():
    return _operator_head() | \
            between(unichar(0x0300), unichar(0x036F)) | \
            between(unichar(0x1DC0), unichar(0x1DFF)) | \
            between(unichar(0x20D0), unichar(0x20FF)) | \
            between(unichar(0xFE00), unichar(0xFE0F)) | \
            between(unichar(0xFE20), unichar(0xFE2F)) | \
            between(unichar(0xE0100), unichar(0xE01EF))


def _dot_operator_head():
    return a(u".")


def _dot_operator_characters():
    return a(u".") | _operator_character()


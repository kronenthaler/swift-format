from SwiftFormat.SwiftNodeTypes import *


class IdentifierScanner:
    # identifier ::= identifier-head [identifier-characters]
    # identifier ::= `identifier-head [identifier-characters]`
    # identifier ::= implicit-parameter-name
    # identifier-list ::= identifier [,identifier-list]
    # identifier-head ::= a-zA-Z
    # identifier-head ::= _
    # identifier-head ::= U+00A8 | U+00AA | U+00AD | U+00AF | U+00B2-U+00B5 | or U+00B7-U+00BA
    # identifier-head ::= U+00BC-U+00BE | U+00C0-U+00D6 | U+00D8-U+00F6 | or U+00F8-U+00FF
    # identifier-head ::= U+0100-U+02FF | U+0370-U+167F | U+1681-U+180D | or U+180F-U+1DBF
    # identifier-head ::= U+1E00-U+1FFF
    # identifier-head ::= U+200B-U+200D | U+202A-U+202E | U+203F-U+2040 | U+2054 | or U+2060-U+206F
    # identifier-head ::= U+2070-U+20CF | U+2100-U+218F | U+2460-U+24FF | or U+2776-U+2793
    # identifier-head ::= U+2C00-U+2DFF or U+2E80-U+2FFF
    # identifier-head ::= U+3004-U+3007 | U+3021-U+302F | U+3031-U+303F | or U+3040-U+D7FF
    # identifier-head ::= U+F900-U+FD3D | U+FD40-U+FDCF | U+FDF0-U+FE1F | or U+FE30-U+FE44
    # identifier-head ::= U+FE47-U+FFFD
    # identifier-head ::= U+10000-U+1FFFD | U+20000-U+2FFFD | U+30000-U+3FFFD | or U+40000-U+4FFFD
    # identifier-head ::= U+50000-U+5FFFD | U+60000-U+6FFFD | U+70000-U+7FFFD | or U+80000-U+8FFFD
    # identifier-head ::= U+90000-U+9FFFD | U+A0000-U+AFFFD | U+B0000-U+BFFFD | or U+C0000-U+CFFFD
    # identifier-head ::= U+D0000-U+DFFFD or U+E0000-U+EFFFD
    # identifier-character ::= Digit 0 through 9
    # identifier-character ::= U+0300-U+036F | U+1DC0-U+1DFF | U+20D0-U+20FF | or U+FE20-U+FE2F
    # identifier-character ::= identifier-head
    # identifier-characters ::= identifier-character [identifier-characters]
    # implicit-parameter-name ::= $ decimal-digits

    def identifier(self):
        pass

    def identifier_list(self):
        pass

    def identifier_head(self):
        pass

    def identifier_character(self):
        pass

    def identifier_characters(self):
        pass

    def implicit_parameter_name(self):
        # decimal digits belongs to literals class.
        pass

import struct
from SwiftFormat.Parser import *
from SwiftFormat.Scanner import *

# identifier ::= identifier-head [identifier-characters]
# identifier ::= `identifier-head [identifier-characters]`
# identifier ::= implicit-parameter-name
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
# implicit-parameter-name ::= $ [0-9]+


def unichar(i):
    try:
        return unichr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')


def identifier():
    id_name = _identifier_head() & many(_identifier_character())
    id_name >>= set_type(SwiftTypes.IDENTIFIER)

    escaped_id = a(u"`") & id_name & a(u"`")
    escaped_id >>= set_type(SwiftTypes.IDENTIFIER)

    implicit = _implicit_parameter()
    implicit >>= set_type(SwiftTypes.IMPLICIT_PARAMETER)

    return one_of(id_name, escaped_id, implicit)


def _identifier_head():
    return one_of(a(u'_'), a(unichar(0x00A8)), a(unichar(0x00AA)), a(unichar(0x00AD)), a(unichar(0x00AF)), a(unichar(0x2054))) | \
            between(u'a', u'z') | \
            between(u'A', u'Z') | \
            between(unichar(0x00B2), unichar(0x00B5)) | \
            between(unichar(0x00B7), unichar(0x00BA)) | \
            between(unichar(0x00BC), unichar(0x00BE)) | \
            between(unichar(0x00C0), unichar(0x00D6)) | \
            between(unichar(0x00D8), unichar(0x00F6)) | \
            between(unichar(0x00F8), unichar(0x00FF)) | \
            between(unichar(0x0100), unichar(0x02FF)) | \
            between(unichar(0x0370), unichar(0x167F)) | \
            between(unichar(0x1681), unichar(0x180D)) | \
            between(unichar(0x180F), unichar(0x1DBF)) | \
            between(unichar(0x1E00), unichar(0x1FFF)) | \
            between(unichar(0x200B), unichar(0x200D)) | \
            between(unichar(0x202A), unichar(0x202E)) | \
            between(unichar(0x203F), unichar(0x2040)) | \
            between(unichar(0x2060), unichar(0x206F)) | \
            between(unichar(0x2070), unichar(0x20CF)) | \
            between(unichar(0x2100), unichar(0x218F)) | \
            between(unichar(0x2460), unichar(0x24FF)) | \
            between(unichar(0x2776), unichar(0x2793)) | \
            between(unichar(0x2C00), unichar(0x2DFF)) | \
            between(unichar(0x2E80), unichar(0x2FFF)) | \
            between(unichar(0x3004), unichar(0x3007)) | \
            between(unichar(0x3021), unichar(0x302F)) | \
            between(unichar(0x3031), unichar(0x303F)) | \
            between(unichar(0x3040), unichar(0xD7FF)) | \
            between(unichar(0xF900), unichar(0xFD3D)) | \
            between(unichar(0xFD40), unichar(0xFDCF)) | \
            between(unichar(0xFDF0), unichar(0xFE1F)) | \
            between(unichar(0xFE30), unichar(0xFE44)) | \
            between(unichar(0xFE47), unichar(0xFFFD)) | \
            between(unichar(0x10000), unichar(0x1FFFD)) | \
            between(unichar(0x20000), unichar(0x2FFFD)) | \
            between(unichar(0x30000), unichar(0x3FFFD)) | \
            between(unichar(0x40000), unichar(0x4FFFD)) | \
            between(unichar(0x50000), unichar(0x5FFFD)) | \
            between(unichar(0x60000), unichar(0x6FFFD)) | \
            between(unichar(0x70000), unichar(0x7FFFD)) | \
            between(unichar(0x80000), unichar(0x8FFFD)) | \
            between(unichar(0x90000), unichar(0x9FFFD)) | \
            between(unichar(0xA0000), unichar(0xAFFFD)) | \
            between(unichar(0xB0000), unichar(0xBFFFD)) | \
            between(unichar(0xC0000), unichar(0xCFFFD)) | \
            between(unichar(0xD0000), unichar(0xDFFFD)) | \
            between(unichar(0xE0000), unichar(0xEFFFD))


def _identifier_character():
    return between(u'0', u'9') | \
            between(unichar(0x0300), unichar(0x036F)) | \
            between(unichar(0x1DC0), unichar(0x1DFF)) | \
            between(unichar(0x20D0), unichar(0x20FF)) | \
            between(unichar(0xFE20), unichar(0xFE2F)) | \
            _identifier_head()


def _implicit_parameter():
    return a(u"$") & at_least_one(between(u'0', u'9'))

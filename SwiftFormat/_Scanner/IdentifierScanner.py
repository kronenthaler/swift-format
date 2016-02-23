# TODO: rewrite all code
import string
from SwiftFormat.SwiftNodeTypes import *
from SwiftLexeme import *


class IdentifierScanner:
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

    def identifier(self, scanner):
        char = scanner.peak_next()

        if char == u"$":
            return self._implicit_parameter_name(scanner)

        if char == u"`":
            tick_open = scanner.next_chunk()
            head = self._identifier_head(scanner)
            if head is None:
                return None

            body = self._identifier_characters(scanner)
            tick_close = scanner.next_chunk()

            if tick_close is None or tick_close.token != u'`':
                scanner.push_back(4)
                return None

            lexem = SwiftLexem.Create([tick_open, head, body, tick_close], type=SwiftLexem.IDENTIFIER)
            return scanner.replace_tokens(lexem, last_tokens=4)

        head = self._identifier_head(scanner)
        if head is None:
            return None

        body = self._identifier_characters(scanner)

        lexem = SwiftLexem.Create([head, body], type=SwiftLexem.IDENTIFIER)
        return scanner.replace_tokens(lexem, last_tokens=2)

    def _identifier_head(self, scanner):
        token = scanner.next_character()
        if self._is_head_pattern(token.token):
            return token
        scanner.push_back()
        return None

    def _identifier_characters(self, scanner):
        count = 1
        token = scanner.next_character()
        if token is None:
            return None

        start = token.start_position
        end = -1
        origin = token
        token_payload = u""
        while token is not None and self._is_character_pattern(token.token):
            token_payload += token.token
            end = token.end_position
            count += 1
            token = scanner.next_character()

        if end != -1:
            scanner.push_back()  # restore the `
            token = SwiftLexem(token_payload, start, end)

            return scanner.replace_tokens(token, count)

        scanner.push_back(count)
        return None

    def _implicit_parameter_name(self, scanner):
        lexem = scanner.next_chunk(skip=u"", delimiters=None, allowed_chars=u"$0123456789")
        if lexem is not None:
            lexem.type = SwiftLexem.IMPLICIT_PARAMETER

        return lexem

    def _is_head_pattern(self, unichar):
        char = ord(unichar)
        return char in [ord(u'_'), 0x00A8, 0x00AA, 0x00AD, 0x00AF, 0x2054] or \
               char in range(ord('a'), ord('z') + 1) or \
               char in range(ord('A'), ord('Z') + 1) or \
               char in range(0x00B2, 0x00B5 + 1) or \
               char in range(0x00B7, 0x00BA + 1) or \
               char in range(0x00BC, 0x00BE + 1) or \
               char in range(0x00C0, 0x00D6 + 1) or \
               char in range(0x00D8, 0x00F6 + 1) or \
               char in range(0x00F8, 0x00FF + 1) or \
               char in range(0x0100, 0x02FF + 1) or \
               char in range(0x0370, 0x167F + 1) or \
               char in range(0x1681, 0x180D + 1) or \
               char in range(0x180F, 0x1DBF + 1) or \
               char in range(0x1E00, 0x1FFF + 1) or \
               char in range(0x200B, 0x200D + 1) or \
               char in range(0x202A, 0x202E + 1) or \
               char in range(0x203F, 0x2040 + 1) or \
               char in range(0x2060, 0x206F + 1) or \
               char in range(0x2070, 0x20CF + 1) or \
               char in range(0x2100, 0x218F + 1) or \
               char in range(0x2460, 0x24FF + 1) or \
               char in range(0x2776, 0x2793 + 1) or \
               char in range(0x2C00, 0x2DFF + 1) or \
               char in range(0x2E80, 0x2FFF + 1) or \
               char in range(0x3004, 0x3007 + 1) or \
               char in range(0x3021, 0x302F + 1) or \
               char in range(0x3031, 0x303F + 1) or \
               char in range(0x3040, 0xD7FF + 1) or \
               char in range(0xF900, 0xFD3D + 1) or \
               char in range(0xFD40, 0xFDCF + 1) or \
               char in range(0xFDF0, 0xFE1F + 1) or \
               char in range(0xFE30, 0xFE44 + 1) or \
               char in range(0xFE47, 0xFFFD + 1) or \
               char in range(0x10000, 0x1FFFD + 1) or \
               char in range(0x20000, 0x2FFFD + 1) or \
               char in range(0x30000, 0x3FFFD + 1) or \
               char in range(0x40000, 0x4FFFD + 1) or \
               char in range(0x50000, 0x5FFFD + 1) or \
               char in range(0x60000, 0x6FFFD + 1) or \
               char in range(0x70000, 0x7FFFD + 1) or \
               char in range(0x80000, 0x8FFFD + 1) or \
               char in range(0x90000, 0x9FFFD + 1) or \
               char in range(0xA0000, 0xAFFFD + 1) or \
               char in range(0xB0000, 0xBFFFD + 1) or \
               char in range(0xC0000, 0xCFFFD + 1) or \
               char in range(0xD0000, 0xDFFFD + 1) or \
               char in range(0xE0000, 0xEFFFD + 1)

    def _is_character_pattern(self, unichar):
        char = ord(unichar)
        return char in range(ord('0'), ord('9') + 1) or \
               char in range(0x0300, 0x036F) or \
               char in range(0x1DC0, 0x1DFF) or \
               char in range(0x20D0, 0x20FF) or \
               char in range(0xFE20, 0xFE2F) or \
               self._is_head_pattern(unichar)

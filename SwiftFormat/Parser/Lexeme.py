class LexemeMetadata:
    def __init__(self, start, end, comments=None, lexeme_type=0):
        self.start = start
        self.end = end
        self.prefix_comments = comments if comments is not None else []
        self.type = lexeme_type

    def __repr__(self):
        return "@ [{0}, {1}) T: {2}".format(self.start, self.end, self.type)


class Lexeme(unicode):
    # Extended unicode string with extra metadata related to the lexeme.

    def __new__(cls, token, start, end, comments=None, lexeme_type=0):
        obj = unicode.__new__(cls, token)
        obj.meta = LexemeMetadata(start, end, comments, lexeme_type)
        return obj

    def __repr__(self):
        return "L({0} => {1})".format(self, self.meta)

    def __add__(self, other):
        token = super(Lexeme, self).__add__(other if other is not None else u"")

        return Lexeme(token,
                      self.meta.start,
                      max(self.meta.end, other.meta.end),
                      self.meta.prefix_comments + other.meta.prefix_comments,
                      self.meta.type | other.meta.type)


def set_type(lexeme_type):
    def _mark(lexeme):
        lexeme.meta.type = lexeme_type
        return lexeme

    return _mark

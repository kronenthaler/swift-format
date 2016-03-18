class Lexeme:
    def __init__(self, data, start, end, comments=None, lexeme_type=0):
        self.token = data
        self.start = start
        self.end = end
        self.prefix_comments = comments if comments is not None else []
        self.type = lexeme_type

    def __repr__(self):
        return "L({0} @ [{1}, {2}) T: {3}) ".format(self.token, self.start, self.end, self.type)

    def __add__(self, other):
        token = u""
        if other.token is None:
            token = self.token
        elif self.token is None:
            token = other.token
        else:
            token = self.token + other.token
        return Lexeme(token,
                      self.start,
                      max(self.end, other.end),
                      self.prefix_comments + other.prefix_comments,
                      self.type | other.type)

    def __len__(self):
        if self.token is None:
            return 0

        return self.token.__len__()


def set_type(lexeme_type):
    def _mark(lexeme):
        lexeme.type = lexeme_type
        return lexeme
    return _mark

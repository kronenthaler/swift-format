class Lexeme:
    def __init__(self, data, start, end, comments=[], type=0):
        self.token = data
        self.start = start
        self.end = end
        self.prefix_comments = comments
        self.type = type

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


def set_type(type):
    def _mark(lexeme):
        lexeme.type = type
        return lexeme
    return _mark

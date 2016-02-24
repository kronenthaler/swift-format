class Lexeme:
    def __init__(self, data, start, end, comments = []):
        self.token = data
        self.start = start
        self.end = end
        self.prefix_comments = comments
        self.type = 0

    def __repr__(self):
        return "L({0} @ [{1}, {2})) ".format(self.token, self.start, self.end)

    def __add__(self, other):
        token = u""
        if other.token is None:
            token = self.token
        elif self.token is None:
            token = other.token
        else:
            token = self.token + other.token
        return Lexeme(token, self.start, other.end, self.prefix_comments + other.prefix_comments)

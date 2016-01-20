

class SwiftNode:
    def __init__(self, token):
        self.token = token
        self.children = None

    def append(self, child):
        self.children.append(child)
    pass

class Comment(SwiftNode):
    pass

class SingleLineComment(Comment):
    def __repr__(self):
        return "// {0}\n".format(self.token.token)
    pass

class MultiLineComment(Comment):
    def __init__(self, token):
        Comment.__init__(self, token)
        self.children = [token]

    def __repr__(self):
        comment = "/*"

        for child in self.children:
            comment += "{0}".format(child.__repr__())

        comment += "*/"
        return comment

    def __eq__(self, other):
        return self.children == other.children
    pass
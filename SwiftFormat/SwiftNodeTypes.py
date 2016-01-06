__author__ = 'ignacio'

class SwiftNode:
    def __init__(self, token):
        self.token = token
    pass

class Comment(SwiftNode):
    pass

class SingleLineComment(Comment):
    def __str__(self):
        return "// {0}\n".format(self.token.cleaned_data);
    pass

class MultiLineComment(Comment):
    def __init__(self, token):
        Comment.__init__(self, token)
        self.children = [token]

    def append(self, data):
        self.children.append(data)

    def __str__(self):
        return "/* {0} */".format(self.children)

    def __repr__(self):
        return self.__str__()
    pass
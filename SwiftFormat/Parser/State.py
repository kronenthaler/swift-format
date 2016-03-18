class State:
    def __init__(self, sequence, end):
        self.input = sequence
        self.index = end

    def __repr__(self):
        return "S({0})".format(self.index)

    def __add__(self, other):
        return State(self.input, max(self.index, other.index))

    def __rshift__(self, increment):
        return State(self.input, self.index + increment)

    def __lshift__(self, decrement):
        return State(self.input, self.index - decrement)

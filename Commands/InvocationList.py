class InvocationList(object):

    def __init__(self):
        self.targets = []

    def add(self, func):
        self.targets.append(func)

    def remove(self, func):
        self.targets.remove(func)

    def invoke(self, *args):
        for f in self.targets:
            f(*args)

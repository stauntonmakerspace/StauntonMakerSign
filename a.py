class A():
    def __init__(self, name):
        self.name = name
    def setter(self,val):
        self.name = val

class B():
    def __init__(self):
        self.names = [A(x) for x in 'rfes']
b = B()
        
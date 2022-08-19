class Line:
    length = 0

    def __init__(self, length):
        self.length = length
        print("declared")

    def __add__(self, other):
        Line.length = self.length + other.length

    def __del__(self):
        Line.length -= self.length
        print(f"deleted... {self}")

    def __repr__(self):
        return str(self.length)

    @classmethod
    def class_add(self, length):
        return Line(length)

    @classmethod
    def class_sub(self, length):
        return Line(length)



myLine1 = Line(100)
myLine2 = Line(200)

print(Line.length)

myLine1 + myLine2

print(Line.length)

del(myLine1)

print(Line.length)

del(myLine2)

print(Line.length)
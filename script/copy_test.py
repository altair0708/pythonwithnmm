import copy


class CopyClass(object):
    def __init__(self, value):
        self.id = value


if __name__ == '__main__':
    a = CopyClass(1)
    b = a
    c = copy.copy(a)
    a.id = 2
    print(b.id)
    print(b is a)
    print(c.id)

from queue import Queue

a = Queue()

a.put('a')
a.put('b')
a.put('c')

for i in a.queue:
    print(i)


def func():
    b = True
    c = False
    return b and c


print(func())


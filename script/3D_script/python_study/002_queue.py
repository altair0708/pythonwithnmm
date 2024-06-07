from queue import Queue

a = Queue()

a.put('a')
a.put('b')
a.put('c')

for i in a.queue:
    print(i)

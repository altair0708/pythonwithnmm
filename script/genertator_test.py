import time


def genertator():
    i = 0
    while True:
        i += 1
        yield i


if __name__ == '__main__':
    gen = genertator()
    for i in range(100):
        print(next(gen))
        time.sleep(1)

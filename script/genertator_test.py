import time
import random


def genertator():
    while True:
        temp = random.uniform(-0.001, 0.001)
        yield temp


if __name__ == '__main__':
    gen = genertator()
    for i in range(100):
        print(next(gen))
        time.sleep(1)

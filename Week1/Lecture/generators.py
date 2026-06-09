def generator():
    print("generator called")
    input = yield 1
    print(input)
    print("first yield done")
    yield 3
    print("second yield")
    yield 4


result = generator()
print(result)

a = result.__next__()
print(a)
result.send(100)
# result.__next__()
# result.__next__()

# result.__next__()
# for a in result:
#    print(a)

from contextlib import contextmanager


@contextmanager
def insert_db():
    print("insert")
    yield 1
    print("close db connection")


for i in range(10):
    with insert_db() as a:
        print(a)
    print("outside")

f = open()

with open() as f:

    a = [x for x in range(1, 100)]
    a = (x for x in rapge(0, 100))

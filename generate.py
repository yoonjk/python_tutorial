
def gen():
    yield 1
    yield 2
    yield 3


g = gen()
print(type(g))

print(next(g))
print(next(g))
print(next(g))

for i in gen():
    print (i)
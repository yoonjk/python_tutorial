x = [1,2,3,4,5]
squared=list(map(lambda x: x ** 2, x))
print(squared)

numbers = [1, 2, 3, 4, 5]

def func(x):
    return x ** 2
# map to list using func
val = list(map(func, numbers))

print (val)

for x1 in val:
    print(x1)

# map to list using lambda
val = list(map(lambda x : x ** 2, numbers))
for x1 in val:
    print('lambda {}'.format(x1))
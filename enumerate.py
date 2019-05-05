val = ['a', 'b', 'c']

for index in range(len(val)):
    print (index, val[index])

#enumerate
x = list(enumerate(val))
print (x)

#enumerate(arg, index)
x = list(enumerate(val, 2))
print (x)
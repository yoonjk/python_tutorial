t = ((1,'a'), (2, 'b'))

#map
ret = dict(map(reversed, t))

print (ret)

# annonymouse
ret = dict((y, x) for x, y in t)
print (ret)
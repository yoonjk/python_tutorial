dicts=[
    {'id':1, 'name':'kim', 'age':25},
    {'id':2, 'name':'hong', 'age':44},
    {'id':3, 'name':'lee', 'age': 30},
    {'id':4, 'name':'kang', 'age': 50}
]

ret = next(( item for item in dicts if item['id'] == 2), None)
print (ret)

ret = next(( index for (index, item) in enumerate(dicts) if item['id'] == 1), None)
print (ret)

t = ((1,'a'), (2, 'b'))

#map
ret = dict(map(reversed, t))

print (ret)

# annonymouse
ret = dict((y, x) for x, y in t)
print (ret)


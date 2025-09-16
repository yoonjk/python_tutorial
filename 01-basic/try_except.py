import sys

x = ['0', 0, 2]

for entry in x:
    try:
        print('The Entry is', entry)
        r=1/int(entry)
        break
    except:
        print("oops", sys.exc_info()[0], 'occured')
        print("next entry")

print ("The reciprocol of", entry, "is", r)

try:
    f = open('test.txt', encoding='utf-8')
except Exception:
    print ('Except')
finally:
    print ('finally')
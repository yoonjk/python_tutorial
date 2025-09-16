import time
from datetime import datetime

#timestamp to str
s = str(time.time())

#timestamp
print(s)

#datetime to str
s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print('YYYY-MM-DD HH24MISS=>{}'.format(s))

s = datetime.now().strftime('%Y-%m-%d')
print('YYYY-MM-DD=>{}'.format(s))
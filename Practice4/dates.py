#1
import datetime
tday = datetime.date.today()
new_date = tday - datetime.timedelta(days=5)

print("Today:", tday)
print("5 days ago:", new_date)


#2
import datetime
tday = datetime.date.today()
yesterday = tday - datetime.timedelta(days=1)
tomorrow = tday + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", tday)
print("Tomorrow:", tomorrow)


#3
import datetime
nw = datetime.datetime.now()
without_microseconds = nw.replace(microsecond=0)

print("With microseconds:", nw)
print("Without microseconds:", without_microseconds)



#4
from datetime import datetime
d1 = datetime(2025, 1, 1, 12, 0, 0)
d2 = datetime(2025, 1, 2, 12, 0, 0)

print((d2 - d1).total_seconds())
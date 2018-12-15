import datetime

s = str(datetime.datetime.now().isoformat())
s2 = str(datetime.datetime.utcnow().isoformat())
print(s)
print(s2)
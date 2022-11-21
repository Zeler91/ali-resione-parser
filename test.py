a = '12-34'
b = a.split('-')
c = tuple(map(int, b))
print(c)
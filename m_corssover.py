# print(2 % 8)

self =    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,2]
parent =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
length = len(self)
points = 5
print(length)
x = (length // (points + 1))
print(x)

c = []
p = 0
for i in range(points):
    l = len(c)
    if length - l < x or p >= points + 1:
        c = c + parent[l:]
        break
    c = c + self[l: l+x]
    l = len(c)
    p += 1
    if length - l < x or p >= points + 1:
        c = c + self[l:]
        break
    c = c + parent[l: l+x]
    p += 1


print(self)
print(parent)
print(c)
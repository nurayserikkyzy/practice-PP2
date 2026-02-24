x = min(5, 10, 25)
y = max(5, 10, 25)

print(x)
print(y)


x = abs(-7.25)
print(x)


x = pow(4, 3)
print(x)


import math
x = math.sqrt(64)
print(x)


#1
import math
degree = 15
radian = degree * math.pi / 180
print("Output radian:", round(radian, 6))


#2
height = 5
a = 5
b = 6
area = (a + b) / 2 * height
print("Expected Output:", area)


#3
import math
n = 4
a = 25
area = (n * a**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area, 0))


#4
base = 5
height = 6
area = base * height
print("Expected Output:", float(area))
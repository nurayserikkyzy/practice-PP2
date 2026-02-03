
age = 25
height = 170
weight = 65
print(age >= 18 and height >= 160 and weight < 70)  # True

day = "Saturday"
temperature = 30
print(day == "Saturday" or day == "Sunday" or temperature > 28)  # True


is_raining = False
has_umbrella = True
print(not is_raining and has_umbrella)  # True

x = 10
y = 5
z = 20
print((x > y and y < z) or not (x == z))  # True

a = 8
b = 12
c = 5
print(a < b and b > c)       
print(a > b or c < b)        
print(not (a == c or b < c))
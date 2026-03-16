mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))



mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))


class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)

#1
def square_generator(n):
    for i in range(n + 1):
        yield i * i

# пример
for num in square_generator(5):
    print(num)

#2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter n: "))

print(",".join(str(num) for num in even_numbers(n)))

#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input("Enter n: "))

for num in divisible_by_3_and_4(n):
    print(num)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
for value in squares(3, 7):
    print(value)

#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
for num in countdown(5):
    print(num)
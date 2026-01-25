b = "Hello, World!"
print(b[:5])
#Get the characters from the start to position 5 (not included)
# 1. Изменение регистра
msg = "python is fun"
print(msg.upper())    # PYTHON IS FUN
print(msg.lower())    # python is fun

# 2. Замена слова
print(msg.replace("fun", "cool"))  # python is cool

# 3. Разделение на слова
print(msg.split())  # ['python', 'is', 'fun']

# 4. Склеивание слов
a = "I"
b = "like"
c = "Python"
sentence = a + " " + b + " " + c
print(sentence)  # I like Python

# 5. Форматированная строка
name = "Alex"
age = 15
print(f"{name} is {age} years old")  # Alex is 15 years old

# 6. Проверки и регистр
text = "hello world"
print(text.capitalize())   # Hello world
print(text.title())        # Hello World
print(text.islower())      # True
print(text.isupper())      # False

# 7. Считаем буквы и ищем слова
print(text.count("l"))        # 3
print(text.find("world"))     # 6
print(text.startswith("hello")) # True
print(text.endswith("world"))   # True

# 8. join и split
words = text.split()           # ['hello', 'world']
joined = " ".join(words)
print(joined)                  # hello world

# 9. Работа с пробелами
msg2 = "   Hi Python!   "
print(msg2.strip())   # Hi Python!
print(msg2.lstrip())  # Hi Python!   
print(msg2.rstrip())  #    Hi Python!

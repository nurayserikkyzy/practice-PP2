#1
import re
text = "ab abb abbb a ac"
matches = re.findall(r'ab*', text)
print(matches)


#2
import re
text = "ab abb abbb abbbb"
matches = re.findall(r'ab{2,3}', text)
print(matches)


#3
import re
text = "hello_world test_case Hello_World"
matches = re.findall(r'\b[a-z]+_[a-z]+\b', text)
print(matches)


#4
import re
text = "Hello World TEST AnotherOne"
matches = re.findall(r'\b[A-Z][a-z]+\b', text)
print(matches)


#5
import re
text = "a123b axxb aXYZb test"
matches = re.findall(r'a.*b', text)
print(matches)


#6
import re
text = "Hello, world. Python is cool"
result = re.sub(r'[ ,.]', ':', text)
print(result)


#7
import re
text = "hello_world_test"
matches = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)
print(matches)


#8
import re
text = "HelloWorldTest"
matches = re.split(r'(?=[A-Z])', text)
print(matches)


#9
import re
text = "HelloWorldTest"
matches = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
print(matches)


#10
import re
text = "helloWorldTest"
matches = re.sub(r'([A-Z])', r'_\1', text).lower()
print(matches)
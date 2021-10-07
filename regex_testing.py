import re

text = '''
20.445.977-0
coreyms.com
19.877.200-6
21.498.555-8
yeahhh.200
200.patatapopo20.445.977-0
#FF
#0D
#05
'''

text2 = 'Peter is a person'

urls = '''https://www.nasa.gov
http://www.mineduc.cl
https://stringy.net
https://www.clubpenguin.com
'''

with open("p3_1-correccion2.ass") as file:
	contents = file.read()
print(contents)


pattern = re.compile(r'MOV') #pattern specified
#hexadecimal = re.compile(r'#[A-F\d]{0,2}')
match = pattern.search(contents)

print(match.group(0))
print("len contents: ",len(contents))
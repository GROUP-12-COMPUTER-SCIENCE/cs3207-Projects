from zara_parser import parser

# Sample Zara code
code = '''
x = 3 + 5 * (10 - 2)
if x < 20
    y = x * 2
else
    y = x - 1
while y > 0
    y = y - 1
'''

# Parse the Zara code
result = parser.parse(code)
print(result)

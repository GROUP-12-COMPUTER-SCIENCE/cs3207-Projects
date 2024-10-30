from zara_parser_with_translation import parser

# Sample Zara code with expressions, conditionals, and loops
code = '''
x = 3 + 5 * 2
if x < 20
    y = x * 2
else
    y = x - 1
while y > 0
    y = y - 1
'''

# Parse and generate intermediate code
result = parser.parse(code)
print("\nIntermediate Code:")
print("\n".join(result) if result else "No code generated")

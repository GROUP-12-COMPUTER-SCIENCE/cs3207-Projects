import ply.lex as lex

# List of token names
tokens = (
    'TYPE', 'IDENTIFIER', 'NUMBER', 'COMMA', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN',
    'ASSIGN', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LBRACE', 'RBRACE'
)

# Regular expressions for simple tokens

t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Define a rule for identifiers and types
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'TYPE' if t.value in {'int', 'float', 'string'} else 'IDENTIFIER'
    return t

# Define a rule for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

import re

# Define regular expressions for tokens
token_specs = [
    ("DATATYPE", r"\b(integer|float|string)\b"),
    ("IF", r"\bif\b"),
    ("ELSE", r"\belse\b"),
    ("FOR", r"\bfor\b"),
    ("DO", r"\bdo\b"),
    ("WHILE", r"\bwhile\b"),
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("NUMBER", r"\b\d+(\.\d*)?\b"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("SEMICOLON", r";"),
    ("EQUALS", r"=="),
    ("GT", r">"),
    ("LT", r"<"),
    ("GE", r">="),
    ("LE", r"<="),
    ("NE", r"!="),
    ("WHITESPACE", r"\s+"),  # Ignore spaces
]

# Tokenizer function
def tokenize(code):
    tokens = []
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specs)
    get_token = re.compile(tok_regex).match
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise RuntimeError(f"Unexpected character at position {pos}")
        type_ = match.lastgroup
        value = match.group(type_)
        if type_ != "WHITESPACE":  # Skip whitespace
            tokens.append((type_, value))
        pos = match.end()
    return tokens

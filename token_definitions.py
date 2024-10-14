# token_definitions.py
TOKEN_PATTERNS = [
    ("KEYWORD", r'\b(if|else|do|while|for)\b'),  # Keywords
    ("DATATYPE", r'\b(integer|float|string|array|stack)\b'),  # Data types
    ("IDENTIFIER", r'\b[a-zA-Z_]\w*\b'),  # Variable names (identifiers)
    ("OPERATOR", r'[=+\-*/>]'),  # Operators
    ("EQUAL", r'=='),  # Equality operator
    ("NUMBER", r'\b\d+(\.\d+)?\b'),  # Integer or float literals
    ("STRING", r'"[^"]*"'),  # String literals
    ("WHITESPACE", r'\s+'),  # Whitespace (ignored)
    ("UNKNOWN", r'.')  # Catch-all for unknown tokens
]

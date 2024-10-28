import re
from .tokens import KEYWORDS, OPERATORS, DATA_TYPES

class Lexer:
    def __init__(self):
        # Regular expression patterns for different token types
        self.token_patterns = {
            "KEYWORD": r"\b(if|else|do|while|for)\b",
            "OPERATOR": r"[=/*-><]",
            "DATA_TYPE": r"\b(integer|float|string|array|stack)\b",
            "IDENTIFIER": r"\b[a-zA-Z_]\w*\b",
            "LITERAL": r"\b\d+(\.\d+)?|\".*?\"|\'.*?\'\b"
        }
        self.regex = self.compile_regex()

    def compile_regex(self):
        # Combine patterns into one regex for tokenizing
        return re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in self.token_patterns.items()))

    def tokenize(self, code):
        tokens = []
        for match in re.finditer(self.regex, code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            tokens.append((token_type, token_value))
        return tokens

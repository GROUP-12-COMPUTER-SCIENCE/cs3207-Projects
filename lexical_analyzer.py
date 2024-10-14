# lexical_analyzer.py
import re
from token_definitions import TOKEN_PATTERNS  # Import token patterns

class LexicalAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            match = None
            for token_type, pattern in TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    if token_type != "WHITESPACE":  # Ignore whitespace
                        token = (token_type, match.group(0))
                        self.tokens.append(token)
                    pos = match.end(0)
                    break
            if not match:
                raise RuntimeError(f"Unexpected character: {self.code[pos]}")
        return self.tokens

    def display_tokens(self):
        for token in self.tokens:
            print(f"{token[0]}: {token[1]}")

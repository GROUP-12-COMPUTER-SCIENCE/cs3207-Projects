import re

# Token types
KEYWORD, IDENTIFIER, NUMBER, OPERATOR, COMMENT = 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'OPERATOR', 'COMMENT'

token_exprs = [
    (r'\s+', None),  # Skip whitespace
    (KEYWORD, r'\b(if|else|while|return|func)\b'),
    (IDENTIFIER, r'[a-zA-Z][a-zA-Z0-9]*'),
    (NUMBER, r'\d+'),
    (OPERATOR, r'[+\-*/<>=;,(){}]'),
    (COMMENT, r'/\*.*?\*/'),
]

def lex(characters, token_exprs):
    ''' Tokenize the characters using the token_exprs. '''
    tokens = []
    pos = 0
    while pos < len(characters):
        match = None
        # Skip over whitespace
        if characters[pos].isspace():
            pos += 1
            continue

        for token_type, regex in token_exprs:
            if regex is not None:
                pattern = re.compile(regex)
                match = pattern.match(characters, pos)
                if match:
                    text = match.group(0)
                    if token_type != COMMENT:
                        tokens.append((token_type, text))
                    break

        if not match:
            raise Exception(f'Illegal character at position {pos}: {characters[pos]}')
        else:
            pos = match.end(0)
    
    return tokens

if __name__ == '__main__':
    source_code = '''
    x = 3 + 5 * (10 - 2);
    if x < 20 {
        y = x * 2;
    } else {
        y = x - 1;
    }
    while y > 0 {
        y = y - 1;
    }
    func foo(x, y) {
        return x + y;
    }
    foo(3, 5);
    '''
    tokens = lex(source_code, token_exprs)
    for token in tokens:
        print(token)

#!/usr/bin/env python3
''' Implementing Bottom Up Parsing (Shift Reduce or LR) '''

from lexer import lex

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

class shift_reduce_parser:
    ''' Bottom Up Parser '''
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.stack = []

    def shift(self):
        ''' Shift a token from the input to the stack. '''
        self.stack.append(self.tokens[self.pos])
        self.pos += 1

    def reduce(self):
        ''' Reduce the stack based on the grammar rules. '''
        if len(self.stack) >= 3:
            if self.stack[-1][0] == NUMBER and self.stack[-2][0] == OPERATOR and self.stack[-3][0] == NUMBER:
                self.stack = self.stack[:-3] + [(NUMBER, '42')]
            elif self.stack[-1][0] == IDENTIFIER and self.stack[-2][0] == IDENTIFIER and self.stack[-3][0] == KEYWORD:
                self.stack = self.stack[:-3] + [(NUMBER, '42')]
            else:
                raise Exception('Syntax error')
        else:
            raise Exception('Syntax error')
        
    def parse(self):
        ''' Parse the tokens. '''
        while self.pos < len(self.tokens):
            if len(self.stack) >= 3:
                if self.stack[-1][0] == NUMBER and self.stack[-2][0] == OPERATOR and self.stack[-3][0] == NUMBER:
                    self.reduce()
                elif self.stack[-1][0] == IDENTIFIER and self.stack[-2][0] == IDENTIFIER and self.stack[-3][0] == KEYWORD:
                    self.reduce()
                else:
                    self.shift()
            else:
                self.shift()
        print(self.stack)

        
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
    parser = shift_reduce_parser(tokens)
    parser.parse()
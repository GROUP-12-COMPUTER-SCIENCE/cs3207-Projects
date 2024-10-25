class GrammarRule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs  # Left-hand side of the rule (non-terminal)
        self.rhs = rhs  # Right-hand side (production)

# Example grammar for Zara
grammar = [
    GrammarRule('E', ['E', '+', 'E']),
    GrammarRule('E', ['E', '-', 'E']),
    GrammarRule('E', ['E', '*', 'E']),
    GrammarRule('E', ['E', '/', 'E']),
    GrammarRule('E', ['(', 'E', ')']),
    GrammarRule('E', ['NUMBER']),
    GrammarRule('E', ['IDENTIFIER']),
    GrammarRule('COND', ['if', '(', 'E', ')', '{', 'BLOCK', '}', 'else', '{', 'BLOCK', '}']),
    GrammarRule('LOOP', ['while', '(', 'E', ')', '{', 'BLOCK', '}']),
]


class ShiftReduceParser:
    def __init__(self, grammar):
        self.grammar = grammar  # List of grammar rules
        self.stack = []  # Stack to store tokens and non-terminals
        self.input_buffer = []  # Input tokens
        self.actions = []  # List of actions (shift/reduce)

    def parse(self, tokens):
        self.input_buffer = tokens[:]  # Copy of the input tokens
        self.stack = []
        self.actions = []

        while self.input_buffer:
            self.shift()

            # Try to reduce after every shift
            reduced = True
            while reduced:
                reduced = self.reduce()

            if not reduced and not self.input_buffer:
                print("Syntax error: Unable to reduce further.")
                break

        if len(self.stack) == 1 and self.stack[0] == 'BLOCK':
            print("Parsing successful!")
        else:
            print("Parsing failed!")

    def shift(self):
        # Move token from input buffer to stack
        token = self.input_buffer.pop(0)
        self.stack.append(token)
        self.actions.append('SHIFT')
        print(f"Shifted: {token}")

    def reduce(self):
        # Try to match the top of the stack with a production rule
        for rule in self.grammar:
            if self.stack[-len(rule.rhs):] == rule.rhs:
                # Perform reduction
                self.stack = self.stack[:-len(rule.rhs)]  # Remove the RHS tokens
                self.stack.append(rule.lhs)  # Push the LHS non-terminal
                self.actions.append(f"REDUCE {rule.lhs} -> {rule.rhs}")
                print(f"Reduced: {rule.lhs} -> {rule.rhs}")
                return True
        return False

# Example Zara tokens from a simple code snippet
tokens = [
    'if', '(', 'IDENTIFIER', ')', '{',
    'IDENTIFIER', '=', 'NUMBER', ';',
    '}', 'else', '{',
    'IDENTIFIER', '=', 'NUMBER', ';',
    '}'
]

parser = ShiftReduceParser(grammar)
parser.parse(tokens)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def advance(self):
        """Move to the next token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """Start parsing."""
        try:
            while self.current_token is not None:
                if self.current_token[0] == "KEYWORD":
                    if self.current_token[1] == "if":
                        self.parse_if_statement()
                    elif self.current_token[1] == "for":
                        self.parse_for_loop()
                    elif self.current_token[1] == "do":
                        self.parse_do_while_loop()
                    else:
                        raise SyntaxError("Unknown keyword")
                else:
                    raise SyntaxError(f"Unexpected token: {self.current_token}")
                self.advance()
        except SyntaxError as e:
            print(f"Syntax Error: {e}")

    def parse_if_statement(self):
        """Parse if-else structure."""
        self.expect("KEYWORD", "if")
        self.expect("IDENTIFIER")  # or condition handling
        self.expect("KEYWORD", "else")

    def parse_for_loop(self):
        """Parse for loop."""
        self.expect("KEYWORD", "for")
        self.expect("IDENTIFIER")  # handle loop variable

    def parse_do_while_loop(self):
        """Parse do-while loop."""
        self.expect("KEYWORD", "do")
        self.expect("KEYWORD", "while")

    def expect(self, token_type, value=None):
        """Check if the current token matches expected type and value."""
        if self.current_token[0] == token_type and (value is None or self.current_token[1] == value):
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type} '{value}', found {self.current_token}")

# Add additional parsing methods as needed for expressions and methods

from errors import SyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
        else:
            self.error(f"Expected {expected_type}, found {self.tokens[self.pos][0]}")

    def error(self, message):
        raise SyntaxError(f"Syntax error at token {self.tokens[self.pos]}: {message}")

    def parse(self):
        self.parse_block()

    # Grammar rules
    def parse_block(self):
        while self.pos < len(self.tokens):
            token_type, _ = self.tokens[self.pos]
            if token_type == "IF":
                self.parse_if()
            elif token_type == "FOR":
                self.parse_for()
            elif token_type == "DO":
                self.parse_do_while()
            elif token_type == "DATATYPE":
                self.parse_method()
            else:
                self.parse_expression()
                self.match("SEMICOLON")

    def parse_if(self):
        self.match("IF")
        self.match("LPAREN")
        self.parse_condition()
        self.match("RPAREN")
        self.match("LBRACE")
        self.parse_block()
        self.match("RBRACE")
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "ELSE":
            self.match("ELSE")
            self.match("LBRACE")
            self.parse_block()
            self.match("RBRACE")

    def parse_for(self):
        self.match("FOR")
        self.match("LPAREN")
        self.parse_expression()
        self.match("SEMICOLON")
        self.parse_condition()
        self.match("SEMICOLON")
        self.parse_expression()
        self.match("RPAREN")
        self.match("LBRACE")
        self.parse_block()
        self.match("RBRACE")

    def parse_do_while(self):
        self.match("DO")
        self.match("LBRACE")
        self.parse_block()
        self.match("RBRACE")
        self.match("WHILE")
        self.match("LPAREN")
        self.parse_condition()
        self.match("RPAREN")
        self.match("SEMICOLON")

    def parse_method(self):
        self.match("DATATYPE")
        self.match("IDENTIFIER")
        self.match("LPAREN")
        self.match("RPAREN")  # For simplicity, assume no parameters
        self.match("LBRACE")
        self.parse_block()
        self.match("RBRACE")

    def parse_condition(self):
        self.parse_expression()
        if self.tokens[self.pos][0] in ["EQUALS", "GT", "LT", "GE", "LE", "NE"]:
            self.match(self.tokens[self.pos][0])
        self.parse_expression()

    def parse_expression(self):
        self.parse_term()
        while self.tokens[self.pos][0] in ["PLUS", "MINUS"]:
            self.match(self.tokens[self.pos][0])
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.tokens[self.pos][0] in ["MULTIPLY", "DIVIDE"]:
            self.match(self.tokens[self.pos][0])
            self.parse_factor()

    def parse_factor(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == "IDENTIFIER":
            self.match("IDENTIFIER")
        elif token_type == "NUMBER":
            self.match("NUMBER")
        elif token_type == "LPAREN":
            self.match("LPAREN")
            self.parse_expression()
            self.match("RPAREN")
        else:
            self.error(f"Unexpected token: {token_type}")

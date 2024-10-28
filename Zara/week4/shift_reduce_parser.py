class ShiftReduceParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.stack = []
        self.input_tokens = []
        self.rules = {
            # Grammar rules: "symbol": ["list of symbols to reduce"]
            "expr": ["expr + term", "expr - term", "term"],
            "term": ["term * factor", "term / factor", "factor"],
            "factor": ["( expr )", "number", "identifier"],
            "if_stmt": ["if ( condition ) { statements } else { statements }"],
            "for_stmt": ["for ( init ; condition ; update ) { statements }"],
            "do_while_stmt": ["do { statements } while ( condition ) ;"]
        }
    
    def parse(self, tokens):
        self.input_tokens = tokens + ["$"]  # End of input symbol
        self.stack.append("$")
        
        while self.input_tokens:
            lookahead = self.input_tokens[0]
            self.shift(lookahead)
            if self.reduce():
                print("Reduced")
            else:
                print("Shifted")
        
        if self.stack == ["$", "program"]:
            print("Parsing Successful")
        else:
            print("Parsing Failed")
    
    def shift(self, token):
        self.stack.append(token)
        self.input_tokens.pop(0)
    
    def reduce(self):
        for rule, patterns in self.rules.items():
            for pattern in patterns:
                pattern_symbols = pattern.split()
                if self.stack[-len(pattern_symbols):] == pattern_symbols:
                    # Perform reduction
                    for _ in pattern_symbols:
                        self.stack.pop()
                    self.stack.append(rule)
                    return True
        return False

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def analyze(self, tokens):
        """
        Analyzes the tokens for semantic consistency.
        This includes:
        - Type consistency (e.g., no implicit type conversions)
        - Scope rules
        - Function/method usage
        """
        for token in tokens:
            token_type, token_value = token  # Unpack the tuple
            
            # Example: Check for variable declaration consistency
            if token_type == "VARIABLE_DECLARATION":
                var_name = token_value
                # Assume you have a way to retrieve data type here, or handle accordingly
                var_type = "integer"  # Example: Replace with actual logic if available
                
                # Check if the variable is already declared
                if self.symbol_table.lookup(var_name):
                    print(f"Error: Variable '{var_name}' already declared.")
                else:
                    self.symbol_table.add_symbol(var_name, var_type)
                    
            # Additional checks based on type consistency, scope, etc.
            # (Implement more logic as per your assignment requirements.)

        print("Semantic Analysis Complete")

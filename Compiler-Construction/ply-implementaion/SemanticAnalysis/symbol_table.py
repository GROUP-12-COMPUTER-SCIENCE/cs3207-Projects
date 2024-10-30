class SymbolTable:
    def __init__(self):
        # Stack of dictionaries to handle scope levels
        self.scopes = [{}]

    def enter_scope(self):
        """Enter a new scope."""
        self.scopes.append({})

    def exit_scope(self):
        """Exit the current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()

    def insert(self, name, var_type):
        """Insert a variable in the current scope."""
        if name in self.scopes[-1]:
            print(f"Error: Variable '{name}' already declared in current scope")
        else:
            self.scopes[-1][name] = var_type

    def lookup(self, name):
        """Look up a variable, starting from the innermost scope."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        print(f"Error: Variable '{name}' not declared")
        return None

    def display(self):
        """Display the current symbol table."""
        print("Current Symbol Table:")
        for scope in self.scopes:
            for name, var_type in scope.items():
                print(f"{name}: {var_type}")

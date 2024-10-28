# symbol_table.py

class Symbol:
    def __init__(self, name, var_type, value=None):
        self.name = name
        self.var_type = var_type
        self.value = value

    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.var_type}, value={self.value})"

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, var_type, value=None):
        if name in self.symbols:
            print(f"Warning: Symbol '{name}' already exists. Updating value.")
        self.symbols[name] = Symbol(name, var_type, value)

    def update_symbol(self, name, value):
        if name in self.symbols:
            self.symbols[name].value = value
        else:
            print(f"Error: Symbol '{name}' not found in symbol table.")

    def get_symbol(self, name):
        return self.symbols.get(name, None)

    def __repr__(self):
        return f"SymbolTable({self.symbols})"

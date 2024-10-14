# symbol_table.py
class SymbolTable:
    def __init__(self):
        # Dictionary to store variables and their attributes
        self.table = {}

    def add_symbol(self, name, symbol_type):
        """Add a symbol with its type"""
        if name not in self.table:
            self.table[name] = symbol_type
            print(f"Symbol added: {name} -> {symbol_type}")
        else:
            print(f"Symbol {name} already exists.")

    def update_symbol(self, name, symbol_type):
        """Update the type of an existing symbol"""
        if name in self.table:
            self.table[name] = symbol_type
            print(f"Symbol updated: {name} -> {symbol_type}")
        else:
            print(f"Symbol {name} does not exist.")

    def retrieve_symbol(self, name):
        """Retrieve a symbol's type"""
        return self.table.get(name, None)

    def log_symbols(self):
        """Log all symbol entries"""
        print("Current Symbol Table:")
        for name, symbol_type in self.table.items():
            print(f"{name}: {symbol_type}")

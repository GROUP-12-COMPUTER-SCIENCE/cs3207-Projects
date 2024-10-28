# parser.py

from symbol_table import SymbolTable
from data_types import INTEGER, FLOAT, STRING, ARRAY, STACK

def parse_declaration(line):
    parts = line.split()
    if len(parts) >= 3:
        var_type = parts[0]
        var_name = parts[1]
        value = " ".join(parts[3:]) if len(parts) > 3 else None
        return var_name, var_type, value
    return None

def load_symbols(filename, symbol_table):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("integer") or line.startswith("float") or line.startswith("string") or \
               line.startswith("array") or line.startswith("stack"):
                var_name, var_type, value = parse_declaration(line)
                symbol_table.add_symbol(var_name, var_type, value)

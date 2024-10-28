# main.py

from week1.symbol_table import SymbolTable
from week2.lexer import Lexer
from week3.parser import Parser

def test_symbol_table():
    print("Testing Symbol Table...")
    # Initialize symbol table
    symbol_table = SymbolTable()
    # Add sample variables
    symbol_table.add_symbol("count", "integer")
    symbol_table.add_symbol("price", "float")
    symbol_table.add_symbol("name", "string")
    # Update and retrieve entries
    symbol_table.update_symbol("count", 10)
    print("Symbol Table Entries:", symbol_table.symbols)
    print("Symbol Table Test Complete\n")

def test_lexer():
    print("Testing Lexer...")
    lexer = Lexer()

    # Load Zara code from test file
    with open("tests/test_program.zara", "r") as file:
        code = file.read()

    # Tokenize the Zara code
    tokens = lexer.tokenize(code)
    print("Tokens:", tokens)
    print("Lexer Test Complete\n")

def test_parser():
    print("Testing Parser...")
    lexer = Lexer()

    # Load Zara code from test file
    with open("tests/test_program.zara", "r") as file:
        code = file.read()

    # Tokenize the Zara code
    tokens = lexer.tokenize(code)

    # Parse the tokens
    parser = Parser(tokens)
    parser.parse()
    print("Parser Test Complete\n")

if __name__ == "__main__":
    print("Running all tests for Zara project:\n")
    test_symbol_table()
    test_lexer()
    test_parser()

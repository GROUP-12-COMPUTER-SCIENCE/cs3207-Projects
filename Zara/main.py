# main.py

from week1.symbol_table import SymbolTable
from week2.lexer import Lexer
from week3.parser import Parser
from week4.shift_reduce_parser import ShiftReduceParser

def print_separator(title):
    print("\n" + "=" * 50)
    print(f"{title}")
    print("=" * 50 + "\n")

def test_symbol_table():
    print_separator("Week 1: Symbol Table Test")
    symbol_table = SymbolTable()
    # Sample data for testing
    symbol_table.add_symbol("count", "integer")
    symbol_table.add_symbol("price", "float")
    symbol_table.add_symbol("name", "string")
    symbol_table.update_symbol("count", 10)
    print("Symbol Table Entries:", symbol_table.symbols)
    print("Symbol Table Test Complete\n")

def test_lexer():
    print_separator("Week 2: Lexical Analysis Test")
    lexer = Lexer()
    
    # Load Zara code from test file
    with open("tests/test_program.zara", "r") as file:
        code = file.read()
    
    # Tokenize the Zara code
    tokens = lexer.tokenize(code)
    print("Tokens:", tokens)
    print("Lexer Test Complete\n")

def test_top_down_parser():
    print_separator("Week 3: Syntax Analysis (Top-Down Parser) Test")
    lexer = Lexer()

    # Load Zara code from test file
    with open("tests/test_program.zara", "r") as file:
        code = file.read()

    # Tokenize the Zara code
    tokens = lexer.tokenize(code)

    # Parse the tokens using the top-down parser
    parser = Parser(tokens)
    parser.parse()
    print("Top-Down Parser Test Complete\n")

def test_bottom_up_parser():
    print_separator("Week 4: Syntax Analysis (Bottom-Up Parser) Test")
    lexer = Lexer()
    
    # Load Zara code from test file
    with open("tests/test_program.zara", "r") as file:
        code = file.read()
    
    # Tokenize the Zara code
    tokens = lexer.tokenize(code)
    
    # Parse tokens using the bottom-up parser
    parser = ShiftReduceParser(lexer)
    parser.parse(tokens)
    print("Bottom-Up Parser Test Complete\n")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Zara Language Project - Test Runner")
    print("=" * 50 + "\n")

    # Run all tests
    test_symbol_table()
    test_lexer()
    test_top_down_parser()
    test_bottom_up_parser()

    print("\n" + "=" * 50)
    print("All Tests Completed")
    print("=" * 50)

from symbolTable import SymbolTable  # Import the SymbolTable class
from subprograms import example_subprogram  # Import the subprogram
from lexical_analyzer import LexicalAnalyzer  # Import the LexicalAnalyzer class

# Sample Zara code to test the lexical analyzer
zara_code = '''
integer a = 5;
float b = 3.14;
string c = "Hello, Zara!";
string name = "Ara";
if (a > b) {
    do {
        a = a - 1;
    } while (a == b);
}
'''

def main():
    # 1. Create an instance of the SymbolTable
    symbol_table = SymbolTable()

    # Declare and add variables to the symbol table
    symbol_table.add_symbol("a", "integer")
    symbol_table.add_symbol("b", "float")
    symbol_table.add_symbol("name", "string")
    symbol_table.add_symbol("my_array", "array")
    symbol_table.add_symbol("my_stack", "stack")

    # 2. Call the example subprogram
    example_subprogram()

    # Log all symbols
    symbol_table.log_symbols()

    # 3. Run the Lexical Analyzer
    print("\nLexical Analyzer Output:")
    analyzer = LexicalAnalyzer(zara_code)
    tokens = analyzer.tokenize()
    analyzer.display_tokens()

# Run the main program
if __name__ == "__main__":
    main()

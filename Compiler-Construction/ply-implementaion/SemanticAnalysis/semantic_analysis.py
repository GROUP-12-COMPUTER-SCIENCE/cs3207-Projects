from zara_lexer import lexer
from zara_parser import parser
from symbol_table import SymbolTable

symbol_table = SymbolTable()

# Test program
test_program = '''
int main() {
    int x = 5;
    float y = x + 2.5;
    int arr[10];
    int stack[];

    // Function declaration
    int add(int a, int b) {
        return a + b;
    }

    // Function call
    int result = add(x, 3);

    // Scope error
    {
        int z = 10;
    }
    print(z); // Error: z is out of scope

    // Type mismatch
    string s = 10; // Error: assigning int to string

    // Array and stack usage
    arr[0] = x;
    stack.push(x); // Assuming stack has push operation
}
'''

# Lexing and Parsing
lexer.input(test_program)
print("\n--- Tokens ---")
for token in lexer:
    print(token)

print("\n--- Parsing and Semantic Analysis ---")
parser.parse(test_program)
symbol_table.display()

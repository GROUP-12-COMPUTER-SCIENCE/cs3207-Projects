from tokenizer import tokenize
from parser import Parser

def main():
    # Zara source code as a string
    zara_code = """
    integer a = 5;
    float b = 3.14;
    if (a > b) {
        a = a + 1;
    } else {
        b = b - 1;
    }
    for (integer i = 0; i < 10; i = i + 1) {
        do {
            a = a * 2;
        } while (a < 100);
    }
    """

    # Step 1: Tokenize the Zara code
    tokens = tokenize(zara_code)
    print("Tokens:")
    for token in tokens:
        print(token)

    # Step 2: Parse the tokens
    parser = Parser(tokens)
    try:
        parser.parse()
        print("Parsing successful!")
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    main()

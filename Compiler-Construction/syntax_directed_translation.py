#!/usr/bin/env python3
'''
Implement a syntax-directed translation rules for Zara to translate high-level constructs
(such as expressions, loops and sub-programs) into intermediate representations.
Use synthesized attributes to generate intermediate code as you parse Zara programs, ensuring it works for a variety of constructs.
'''

from lexer import lex
from semantic_analyzer import AST, VariableNode, AssignmentNode, FunctionNode, build_ast, token_exprs, SemanticAnalyzer

# Token types
KEYWORD, IDENTIFIER, NUMBER, OPERATOR, COMMENT = 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'OPERATOR', 'COMMENT'

source_code = '''
    x = 3 + 5 * (10 - 2);
    if x < 20 {
        y = x * 2;
    } else {
        y = x - 1;
    }
    while y > 0 {
        y = y - 1;
    }
    func foo(x, y) {
        return x + y;
    }
    foo(3, 5);
    '''

tokens = lex(source_code, token_exprs)

ast = build_ast(tokens)

# print(f'ast: {ast}')

analyzer = SemanticAnalyzer(ast)
analyzer.analyze()

class IntermediateCodeGenerator:
    temp_count = 0
    label_count = 0

    @staticmethod
    def new_temp():
        IntermediateCodeGenerator.temp_count += 1
        return f"t{IntermediateCodeGenerator.temp_count}"

    @staticmethod
    def new_label():
        IntermediateCodeGenerator.label_count += 1
        return f"L{IntermediateCodeGenerator.label_count}"

    @staticmethod
    def generate_code(node):
        # print(f"Processing node: {node.type}")
        if node.type == "Program":
            for child in node.children:
                IntermediateCodeGenerator.generate_code(child)

        elif node.type == "Variable":
            print(f"Declare {node.name}")
            return node.name

        elif node.type == "Assignment":
            if len(node.children) >= 2:
                var = IntermediateCodeGenerator.generate_code(node.children[0])
                expr = IntermediateCodeGenerator.generate_code(node.children[1])
                print(f"{var} = {expr}")
            else:
                print("Error: Assignment node has insufficient children.")

        elif node.type == "Number":
            return node.value

        elif node.type in {"+", "-", "*", "/"}:
            if len(node.children) >= 2:
                left = IntermediateCodeGenerator.generate_code(node.children[0])
                right = IntermediateCodeGenerator.generate_code(node.children[1])
                temp = IntermediateCodeGenerator.new_temp()
                print(f"{temp} = {left} {node.type} {right}")
                return temp
            else:
                print(f"Error: {node.type} node has insufficient children.")

        elif node.type == "If":
            if len(node.children) >= 2:
                condition = IntermediateCodeGenerator.generate_code(node.children[0])
                label_else = IntermediateCodeGenerator.new_label()
                label_end = IntermediateCodeGenerator.new_label()
                print(f"if not {condition} goto {label_else}")
                IntermediateCodeGenerator.generate_code(node.children[1])
                print(f"goto {label_end}")
                print(f"{label_else}:")
                if len(node.children) > 2:
                    IntermediateCodeGenerator.generate_code(node.children[2])
                print(f"{label_end}:")
            else:
                print("Error: If node has insufficient children.")

        elif node.type == "While":
            if len(node.children) >= 2:
                label_start = IntermediateCodeGenerator.new_label()
                label_end = IntermediateCodeGenerator.new_label()
                print(f"{label_start}:")
                condition = IntermediateCodeGenerator.generate_code(node.children[0])
                print(f"if not {condition} goto {label_end}")
                IntermediateCodeGenerator.generate_code(node.children[1])
                print(f"goto {label_start}")
                print(f"{label_end}:")
            else:
                print("Error: While node has insufficient children.")

        elif node.type == "Function":
            print(f"Function {node.value}:")
            for param in node.children[:-1]:  # Parameters
                IntermediateCodeGenerator.generate_code(param)
            if node.children:
                IntermediateCodeGenerator.generate_code(node.children[-1])  # Body
            print("endfunc")

        elif node.type == "Return":
            if node.children:
                return_value = IntermediateCodeGenerator.generate_code(node.children[0])
                print(f"return {return_value}")
            else:
                print("Error: Return node has no children.")

        elif node.type == "FunctionCall":
            args = [IntermediateCodeGenerator.generate_code(child) for child in node.children]
            print(f"call {node.value}({', '.join(args)})")

        elif node.type == "Parameter":
            print(f"Parameter {node.value}")

        elif node.type == "Identifier":
            return node.value
        
        else:
            print(f"Error: Unknown node type {node.type}")


if __name__ == "__main__":
    IntermediateCodeGenerator.generate_code(ast)
    # print the intermediate code


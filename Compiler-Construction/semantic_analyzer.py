#!/usr/bin/env python3
'''
Implement a semantic analyzer that checks for type consistency, scope rules, and function/method calls,
array and stack type consistency. Extend the lexer and parser to generate an abstract syntax tree (AST)
and then use the AST to perform the semantic analysis for the Zara programming language.
'''

from lexer import lex
from bottomUp_parser import shift_reduce_parser

# Token types
KEYWORD, IDENTIFIER, NUMBER, OPERATOR, COMMENT = 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'OPERATOR', 'COMMENT'

token_exprs = [
    (r'\s+', None),  # Skip whitespace
    (KEYWORD, r'\b(if|else|while|return|func)\b'),
    (IDENTIFIER, r'[a-zA-Z][a-zA-Z0-9]*'),
    (NUMBER, r'\d+'),
    (OPERATOR, r'[+\-*/<>=;,(){}]'),
    (COMMENT, r'/\*.*?\*/'),
]

class AST:
    ''' Abstract Syntax Tree '''
    def __init__(self, type_name, value=None, name=None):
        self.type = type_name
        self.value = value    # For constants like numbers
        self.name = name      # For identifiers like variable names
        self.children = []
        self.parent = None

    def add_child(self, child):
        ''' Add a child node to the current node '''
        self.children.append(child)
        child.parent = self

    def __repr__(self):
        return f'{self.type}({self.value if self.value else self.name}) -> {self.children}'
    
    def __str__(self):
        return self.__repr__()

# Symbol Table remains unchanged
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def add_symbol(self, name, symbol_type):
        if name in self.scopes[-1]:
            raise Exception(f"Redeclaration error: {name} already declared in this scope.")
        self.scopes[-1][name] = symbol_type

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Undeclared variable: {name}")

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()

    def analyze(self):
        ''' Perform semantic analysis on the AST. '''
        self._analyze_node(self.ast)

    def _analyze_node(self, node):
        if node.type == "Program":
            self.symbol_table.enter_scope()
            for child in node.children:
                self._analyze_node(child)
            self.symbol_table.exit_scope()
        elif isinstance(node, BodyNode):
            for stmt in node.children:
                self._analyze_node(stmt)
        elif isinstance(node, VariableNode):
            if not node.name in self.symbol_table.scopes[-1]:
                self.symbol_table.add_symbol(node.name, "int")
        elif isinstance(node, AssignmentNode):
            self.symbol_table.lookup(node.name)  # Check if variable is declared
            self._analyze_node(node.expr)
        elif node.type == "If":
            self._analyze_node(node.condition)
            self._analyze_node(node.body)
            if hasattr(node, "else_body"):
                self._analyze_node(node.else_body)
        elif node.type == "Function":
            self.symbol_table.add_symbol(node.name, "function")
            self.symbol_table.enter_scope()
            for param in node.params:
                self.symbol_table.add_symbol(param.name, "int")
            self._analyze_node(node.body)
            self.symbol_table.exit_scope()
        elif node.type == "Return":
            self._analyze_node(node.children[0])
        elif node.type == "FunctionCall":
            if self.symbol_table.lookup(node.name) != "function":
                raise Exception(f"Function {node.name} not declared.")
            for arg in node.children:
                self._analyze_node(arg)
        elif isinstance(node, BinaryOpNode):
            self._analyze_node(node.children[0])
            self._analyze_node(node.children[1])
        elif node.type == "Number":
            pass
        else:
            raise Exception(f"Unknown node type: {node.type}")


# Specific Node Types for the AST
class AssignmentNode(AST):
    def __init__(self, var_name, expr):
        super().__init__("Assignment")
        self.name = var_name
        self.expr = expr
        self.add_child(expr)

class IfNode(AST):
    def __init__(self, condition, body, else_body=None):
        super().__init__("If")
        self.condition = condition
        self.add_child(condition)
        self.body = body
        self.add_child(body)
        if else_body:
            self.else_body = else_body
            self.add_child(else_body)

class FunctionNode(AST):
    def __init__(self, name, params, body):
        super().__init__("Function", name=name)
        self.params = params
        self.body = body
        for param in params:
            self.add_child(param)
        self.add_child(body)

class VariableNode(AST):
    def __init__(self, name):
        super().__init__("Variable", name=name)

class NumberNode(AST):
    def __init__(self, value):
        super().__init__("Number", value=value)

class BinaryOpNode(AST):
    def __init__(self, op, left, right):
        super().__init__(op)
        self.add_child(left)
        self.add_child(right)

class ReturnNode(AST):
    def __init__(self, expr):
        super().__init__("Return")
        self.add_child(expr)

class FunctionCallNode(AST):
    def __init__(self, name, args):
        super().__init__("FunctionCall", name=name)
        for arg in args:
            self.add_child(arg)

class ParameterNode(AST):
    def __init__(self, name):
        super().__init__("Parameter", name=name)

class BodyNode(AST):
    def __init__(self):
        super().__init__("Body")

def build_ast(tokens):
    root = AST("Program")
    current = root
    for token in tokens:
        if token[0] == KEYWORD:
            if token[1] == "if":
                condition_node = VariableNode("x")  # Placeholder condition
                body_node = BodyNode()  # Create a BodyNode instance
                new_node = IfNode(condition_node, body_node)
                current.add_child(new_node)
                current = new_node
            elif token[1] == "func":
                body_node = BodyNode()  # Create a BodyNode for function
                new_node = FunctionNode("foo", [ParameterNode("x"), ParameterNode("y")], body_node)
                current.add_child(new_node)
                current = new_node
        elif token[0] == IDENTIFIER:
            var_node = VariableNode(token[1])
            current.add_child(var_node)
        elif token[0] == NUMBER:
            num_node = NumberNode(token[1])
            current.add_child(num_node)
        elif token[0] == OPERATOR:
            if token[1] == "{":
                continue
            elif token[1] == "}":
                if current.parent is not None:
                    current = current.parent
            elif token[1] == "=":
                assign_node = AssignmentNode("x", NumberNode(10))  # Placeholder assignment
                current.add_child(assign_node)
            elif token[1] in ["+", "-", "*", "/"]:
                op_node = BinaryOpNode(token[1], NumberNode(5), NumberNode(10))  # Example placeholder operands
                current.add_child(op_node)
            elif token[1] == ";":
                if current.parent is not None:
                    current = current.parent
        else:
            raise Exception(f"Invalid token: {token}")
    return root

if __name__ == "__main__":
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
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    print(ast)

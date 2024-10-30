import ply.yacc as yacc
from zara_lexer import tokens
from symbol_table import SymbolTable

symbol_table = SymbolTable()

# Empty rule for base case in recursive productions
def p_empty(p):
    '''empty :'''
    pass

def p_program(p):
    '''program : declaration_list'''
    p[0] = p[1]

# Declaration list rule with empty production as base case
def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | declaration
                        | empty'''
    pass

# Block rule that contains a declaration list
def p_block(p):
    '''block : LBRACE declaration_list RBRACE'''
    pass

def p_declaration(p):
    '''declaration : function_declaration
                   | variable_declaration'''
    pass

# Parameter list rule for function declarations
def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA TYPE IDENTIFIER
                      | TYPE IDENTIFIER
                      | empty'''
    pass

# Function declaration rule
def p_function_declaration(p):
    '''function_declaration : TYPE IDENTIFIER LPAREN parameter_list RPAREN block'''
    symbol_table.insert(p[2], f'function({p[1]})')
    symbol_table.enter_scope()
    # Ensure to handle variable scope within function
    # You may want to track parameters here as well
    symbol_table.exit_scope()

# Variable declaration rule
def p_variable_declaration(p):
    '''variable_declaration : TYPE IDENTIFIER ASSIGN expression'''
    symbol_table.insert(p[2], p[1])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term'''
    p[0] = 'int'

def p_term(p):
    '''term : factor
            | term MULTIPLY factor
            | term DIVIDE factor'''
    p[0] = 'int'

def p_factor(p):
    '''factor : NUMBER
              | IDENTIFIER'''
    if isinstance(p[1], int):
        p[0] = 'int'
    else:
        var_type = symbol_table.lookup(p[1])
        if var_type is None:
            print(f"Undefined variable '{p[1]}'")
        else:
            p[0] = var_type

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")
    return

# Build the parser
parser = yacc.yacc(debug=True)

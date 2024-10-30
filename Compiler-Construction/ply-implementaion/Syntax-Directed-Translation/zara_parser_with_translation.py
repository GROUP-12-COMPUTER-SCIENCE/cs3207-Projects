import ply.yacc as yacc
from zara_lexer import tokens

# Intermediate code list to store generated code
intermediate_code = []
temp_count = 0  # For temporary variable names

# Helper function to generate new temporary variable names
def new_temp():
    global temp_count
    temp_name = f"t{temp_count}"
    temp_count += 1
    return temp_name

# Grammar rules with syntax-directed translation

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_statement(p):
    '''statement : expression_statement
                 | conditional_statement
                 | loop_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : ID ASSIGN expression'''
    var = p[1]
    expr_code, result = p[3]
    code = expr_code + [f"{var} = {result}"]
    p[0] = code

# Add rule for relational expressions
def p_expression_relational(p):
    '''expression : expression LESS term
                  | expression GREATER term
                  | expression EQUAL term'''
    expr_code, expr_result = p[1]
    term_code, term_result = p[3]
    result = new_temp()
    code = expr_code + term_code + [f"{result} = {expr_result} {p[2]} {term_result}"]
    p[0] = (code, result)

# Arithmetic expressions
def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    expr_code, expr_result = p[1]
    term_code, term_result = p[3]
    result = new_temp()
    code = expr_code + term_code + [f"{result} = {expr_result} {p[2]} {term_result}"]
    p[0] = (code, result)

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    term_code, term_result = p[1]
    factor_code, factor_result = p[3]
    result = new_temp()
    code = term_code + factor_code + [f"{result} = {term_result} {p[2]} {factor_result}"]
    p[0] = (code, result)

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_number(p):
    '''factor : NUMBER'''
    p[0] = ([], str(p[1]))

def p_factor_id(p):
    '''factor : ID'''
    p[0] = ([], p[1])

# Conditional statement with if-else
def p_conditional_statement(p):
    '''conditional_statement : IF expression statement ELSE statement
                             | IF expression statement'''
    expr_code, expr_result = p[2]
    if_code = p[3]
    code = expr_code + [f"if {expr_result} goto L1"] + ["goto L2", "label L1"] + if_code
    
    if len(p) == 6:  # if-else structure
        else_code = p[5]
        code += ["goto L3", "label L2"] + else_code + ["label L3"]
    else:
        code += ["label L2"]
    
    p[0] = code

# Loop statement with while
def p_loop_statement(p):
    '''loop_statement : WHILE expression statement'''
    expr_code, expr_result = p[2]
    body_code = p[3]
    code = ["label L1"] + expr_code + [f"if {expr_result} goto L2", "goto L3", "label L2"] + body_code + ["goto L1", "label L3"]
    p[0] = code

# Error rule for syntax errors
def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

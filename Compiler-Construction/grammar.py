grammar = '''
<program>      ::= <statement> | <statement> <program>
<statement>    ::= <assignment> ";" | <if_statement> | <while_statement> | <func_definition> | <func_call> ";"
<assignment>   ::= <identifier> "=" <expression>
<expression>   ::= <term> | <expression> "+" <term> | <expression> "-" <term>
<term>         ::= <factor> | <term> "*" <factor> | <term> "/" <factor>
<factor>       ::= <number> | <identifier> | "(" <expression> ")"
<if_statement> ::= "if" <condition> "{" <program> "}" <else_clause>
<else_clause>  ::= "else" "{" <program> "}" | ε
<condition>    ::= <expression> <relational_operator> <expression>
<relational_operator> ::= "<" | ">" | "<=" | ">=" | "==" | "!="
<while_statement> ::= "while" <condition> "{" <program> "}"
<func_definition> ::= "func" <identifier> "(" <parameter_list> ")" "{" <program> "return" <expression> ";" "}"
<parameter_list>  ::= <identifier> | <identifier> "," <parameter_list> | ε
<func_call>       ::= <identifier> "(" <argument_list> ")"
<argument_list>   ::= <expression> | <expression> "," <argument_list> | ε
<number>      ::= [0-9]+
<identifier>  ::= [a-zA-Z][a-zA-Z0-9]*
'''
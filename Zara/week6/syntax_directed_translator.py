class SyntaxDirectedTranslator:
    def __init__(self):
        self.intermediate_code = []

    def translate_expression(self, expression):
        # Example translation rule for an expression
        # Here we simulate some intermediate code generation
        self.intermediate_code.append(f"eval_expr {expression}")

    def translate_loop(self, condition, body):
        # Example translation rule for a loop
        self.intermediate_code.append(f"start_loop {condition}")
        for stmt in body:
            self.intermediate_code.append(f"loop_body {stmt}")
        self.intermediate_code.append("end_loop")

    def translate_sub_program(self, name, body):
        # Example translation rule for a sub-program
        self.intermediate_code.append(f"start_func {name}")
        for stmt in body:
            self.intermediate_code.append(f"func_body {stmt}")
        self.intermediate_code.append("end_func")

    def get_intermediate_code(self):
        return "\n".join(self.intermediate_code)

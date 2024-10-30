from typing import List, Tuple, Optional
import re

class TACGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = []

    def new_temp(self) -> str:
        temp_var = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_var

    def new_label(self) -> str:
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate_tac(self, zara_code: str) -> List[Tuple[str, Optional[str]]]:
        # Split the Zara code into lines and process each line
        for line in zara_code.splitlines():
            line = line.strip()

            # Match assignment statements (e.g., `x = y + z`)
            assignment_match = re.match(r'(\w+)\s*=\s*(.+)', line)
            if assignment_match:
                var, expression = assignment_match.groups()
                self._process_assignment(var, expression)
                continue

            # Match if-statements (e.g., `if x > y`)
            if line.startswith("if"):
                condition = line[2:].strip()
                true_label = self.new_label()
                false_label = self.new_label()
                self.code.append((f"if {condition} goto {true_label}", None))
                self.code.append((f"goto {false_label}", None))
                self.code.append((f"{true_label}:", None))
                continue

            # Match method calls (e.g., `result = add(a, b)`)
            method_call_match = re.match(r'(\w+)\s*=\s*(\w+)\((.*)\)', line)
            if method_call_match:
                var, method_name, args = method_call_match.groups()
                self._process_method_call(var, method_name, args)
                continue

            # End of if-block with an optional else branch
            if line == "end_if":
                false_label = self.new_label()
                self.code.append((f"{false_label}:", None))
                continue

        return self.code

    def _process_assignment(self, var: str, expression: str):
        # Split the expression into operands and operator
        tokens = expression.split()
        if len(tokens) == 3:
            arg1, op, arg2 = tokens
            temp_result = self.new_temp()
            self.code.append((f"{temp_result} = {arg1} {op} {arg2}", None))
            self.code.append((f"{var} = {temp_result}", None))
        else:
            # Simple assignment without an operation
            self.code.append((f"{var} = {expression}", None))

    def _process_method_call(self, var: str, method_name: str, args: str):
        arg_list = args.split(",")
        for arg in arg_list:
            self.code.append((f"param {arg.strip()}", None))
        temp_result = self.new_temp()
        self.code.append((f"{temp_result} = call {method_name}, {len(arg_list)}", None))
        self.code.append((f"{var} = {temp_result}", None))

    def get_code(self) -> List[Tuple[str, Optional[str]]]:
        return self.code
    

if __name__ == '__main__':
    zara_code = """
    x = 5
    y = 10
    z = x + y
    if x > y
    max = x
    end_if
    result = add(x, y)
    """

    # Instantiate the TAC generator
    tac_generator = TACGenerator()
    tac_generator.generate_tac(zara_code)

    # Print generated TAC code
    print("Generated Intermediate Representation (TAC):")
    for line, comment in tac_generator.get_code():
        if comment:
            print(f"{line} // {comment}")
        else:
            print(line)

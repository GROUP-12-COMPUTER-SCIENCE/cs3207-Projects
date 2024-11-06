class TACInstruction:
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op       # Operation (e.g., '+', '-', 'goto', 'call')
        self.arg1 = arg1   # First argument
        self.arg2 = arg2   # Second argument
        self.result = result  # Where to store the result

    def __str__(self):
        if self.op == 'goto':
            return f"{self.op} {self.result}"
        elif self.op in {'ifgoto', 'call'}:
            return f"{self.op} {self.arg1}, {self.arg2}, {self.result}"
        elif self.arg2:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        else:
            return f"{self.result} = {self.op} {self.arg1}"

class TACGenerator:
    def __init__(self):
        self.instructions = []     # List to store TAC instructions
        self.temp_count = 0        # Counter for temporary variables
        self.label_count = 0       # Counter for labels

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def add_instruction(self, op, arg1=None, arg2=None, result=None):
        instr = TACInstruction(op, arg1, arg2, result)
        self.instructions.append(instr)

    def generate_expression(self, op, arg1, arg2):
        temp = self.new_temp()
        self.add_instruction(op, arg1, arg2, temp)
        return temp

    def generate_if(self, condition, true_label, false_label):
        self.add_instruction('ifgoto', condition, true_label, false_label)

    def generate_goto(self, label):
        self.add_instruction('goto', result=label)

    def generate_label(self, label):
        self.add_instruction('label', result=label)

    def generate_call(self, func_name, args):
        for arg in args:
            self.add_instruction('param', arg1=arg)
        result = self.new_temp()
        self.add_instruction('call', func_name, len(args), result)
        return result

    def print_instructions(self):
        for instr in self.instructions:
            print(instr)

def main():
    tac_gen = TACGenerator()

    # Example: Generate TAC for expression `a = b + c * d`
    t1 = tac_gen.generate_expression('*', 'c', 'd')  # t1 = c * d
    tac_gen.add_instruction('=', 'b', t1, 'a')       # a = b + t1

    # Example: Generate TAC for if-else
    condition = "x > y"
    true_label = tac_gen.new_label()
    false_label = tac_gen.new_label()
    tac_gen.generate_if(condition, true_label, false_label)
    tac_gen.generate_label(true_label)
    # (Add code for 'if' block here)
    tac_gen.generate_goto(false_label)  # Jump to end after 'if' block
    tac_gen.generate_label(false_label)

    # Example: Generate TAC for function call `result = myFunc(a, b)`
    tac_gen.generate_call("myFunc", ["a", "b"])

    # Print generated TAC
    tac_gen.print_instructions()

if __name__ == "__main__":
    main()

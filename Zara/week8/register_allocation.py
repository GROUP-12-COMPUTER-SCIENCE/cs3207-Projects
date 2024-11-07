class Variable:
    def __init__(self, name):
        self.name = name
        self.live_range = []
        self.register = None  # Assigned register (None if not assigned)
        self.spilled = False  # Track if variable has been spilled

class RegisterAllocator:
    def __init__(self, num_registers):
        self.num_registers = num_registers
        self.variables = {}  # Stores variable objects by name
        self.interference_graph = {}  # Stores adjacency list for interference graph
        self.register_pool = [f"R{i}" for i in range(num_registers)]  # Register names

    def analyze_live_ranges(self, program):
        """
        Perform live range analysis on a program to calculate where each variable is live.
        program: List of tuples representing instructions and variables in use.
        """
        for index, (instruction, uses) in enumerate(program):
            for var_name in uses:
                if var_name not in self.variables:
                    self.variables[var_name] = Variable(var_name)
                self.variables[var_name].live_range.append(index)

    def build_interference_graph(self):
        """
        Build the interference graph based on live ranges.
        """
        for var1 in self.variables.values():
            for var2 in self.variables.values():
                if var1 != var2 and self.overlaps(var1.live_range, var2.live_range):
                    if var1.name not in self.interference_graph:
                        self.interference_graph[var1.name] = set()
                    if var2.name not in self.interference_graph:
                        self.interference_graph[var2.name] = set()
                    self.interference_graph[var1.name].add(var2.name)
                    self.interference_graph[var2.name].add(var1.name)

    def overlaps(self, range1, range2):
        """
        Check if two live ranges overlap.
        """
        return bool(set(range1) & set(range2))

    def color_graph(self):
        """
        Assign registers to variables using graph coloring, with spill handling.
        """
        stack = []
        temp_variables = self.variables.copy()  # Keep a copy for coloring

        while temp_variables:
            # Step 1: Simplification phase, try to reduce the graph
            to_remove = []
            for var_name, var in temp_variables.items():
                degree = len(self.interference_graph.get(var_name, []))
                if degree < self.num_registers:
                    stack.append(var_name)
                    to_remove.append(var_name)

            # Remove nodes from graph
            for var_name in to_remove:
                temp_variables.pop(var_name)
                self.interference_graph.pop(var_name, None)

            # If no nodes could be removed, we need to spill a variable
            if not to_remove and temp_variables:
                # Spill heuristic: choose variable with highest degree
                spill_var = max(temp_variables, key=lambda name: len(self.interference_graph[name]))
                self.variables[spill_var].spilled = True
                print(f"Spilling variable: {spill_var}")
                temp_variables.pop(spill_var)
                self.interference_graph.pop(spill_var)

        # Step 2: Assign colors (registers) in reverse order of stack
        while stack:
            var_name = stack.pop()
            used_registers = {self.variables[neighbor].register for neighbor in self.interference_graph.get(var_name, []) if neighbor in self.variables}
            available_registers = [reg for reg in self.register_pool if reg not in used_registers]

            if available_registers:
                self.variables[var_name].register = available_registers[0]
            else:
                self.variables[var_name].spilled = True
                print(f"Spilling variable during coloring: {var_name}")


    def allocate_registers(self, program):
        """
        Main function to allocate registers for the program.
        """
        self.analyze_live_ranges(program)
        self.build_interference_graph()
        self.color_graph()
        self.print_allocation()

    def print_allocation(self):
        """
        Print final register allocation.
        """
        for var_name, var in self.variables.items():
            if var.spilled:
                print(f"{var_name} -> SPILLED")
            else:
                print(f"{var_name} -> {var.register}")

# # Example usage
# program = [
#     ("LOAD", ["a"]),
#     ("ADD", ["b", "a"]),
#     ("STORE", ["c"]),
#     ("LOAD", ["d"]),
#     ("SUB", ["c", "d"]),
#     ("STORE", ["e"])
# ]

# allocator = RegisterAllocator(num_registers=2)
# allocator.allocate_registers(program)

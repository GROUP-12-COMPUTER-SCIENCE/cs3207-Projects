import time
import tracemalloc
from register_allocation import RegisterAllocator  # Make sure this import points to the correct file/module
from tabulate import tabulate  # For improved table formatting
from termcolor import colored  # For color styling in terminal

# Sample Test Programs
test_programs = {
    "Simple Arithmetic": [
        ("LOAD", ["a"]),
        ("ADD", ["b", "a"]),
        ("STORE", ["c"]),
        ("SUB", ["c", "a"]),
        ("STORE", ["d"])
    ],
    "Loop with Condition": [
        ("LOAD", ["i"]),
        ("CMP", ["i", "10"]),
        ("JUMP_IF_LESS", ["end"]),
        ("SUB", ["i", "1"]),
        ("STORE", ["i"]),
        ("JUMP", ["loop"]),
        ("LABEL", ["end"])
    ],
    "Function Calls": [
        ("LOAD", ["a"]),
        ("LOAD", ["b"]),
        ("CALL", ["add", "a", "b"]),
        ("STORE", ["result"])
    ],
    "High Register Pressure": [
        ("LOAD", ["a"]),
        ("LOAD", ["b"]),
        ("LOAD", ["c"]),
        ("LOAD", ["d"]),
        ("LOAD", ["e"]),
        ("LOAD", ["f"]),
        ("ADD", ["a", "b"]),
        ("SUB", ["c", "d"]),
        ("MUL", ["e", "f"]),
        ("STORE", ["result1"]),
        ("STORE", ["result2"]),
        ("STORE", ["result3"])
    ]
}

class NaiveAllocator:
    def __init__(self, num_registers):
        self.num_registers = num_registers
        self.register_pool = [f"R{i}" for i in range(num_registers)]
        self.spills = 0

    def allocate(self, program):
        registers_used = 0
        allocation = {}
        for instruction, vars in program:
            for var in vars:
                if var not in allocation:
                    if registers_used < self.num_registers:
                        allocation[var] = self.register_pool[registers_used]
                        registers_used += 1
                    else:
                        allocation[var] = "SPILLED"
                        self.spills += 1
        return allocation

def evaluate_allocator(allocator, program, is_naive=False):
    # Measure execution time and memory usage
    start_time = time.time()
    tracemalloc.start()
    
    # Run the allocation method based on allocator type
    if is_naive:
        allocation = allocator.allocate(program)
        spills = allocator.spills
    else:
        allocator.allocate_registers(program)
        spills = sum(1 for var in allocator.variables.values() if var.spilled)
    
    # Measure memory and execution time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    exec_time = time.time() - start_time
    
    return spills, exec_time, peak_memory

def run_tests():
    num_registers = 2
    baseline_allocator = NaiveAllocator(num_registers)
    results = []

    # Header for output
    print(colored("Register Allocation Test Results", 'cyan', attrs=['bold']))
    print("-" * 50)

    for name, program in test_programs.items():
        # Baseline test with NaiveAllocator
        baseline_spills, baseline_time, baseline_memory = evaluate_allocator(baseline_allocator, program, is_naive=True)
        
        # Advanced allocator test with RegisterAllocator
        advanced_allocator = RegisterAllocator(num_registers)  # Create a fresh instance each time
        advanced_spills, advanced_time, advanced_memory = evaluate_allocator(advanced_allocator, program, is_naive=False)

        # Store the result for table formatting
        results.append([
            name,
            baseline_spills,
            f"{baseline_time:.4f}",
            f"{baseline_memory / 1024:.2f}",
            advanced_spills,
            f"{advanced_time:.4f}",
            f"{advanced_memory / 1024:.2f}"
        ])

    # Table headers and formatting
    headers = [
        colored("Test Program", 'yellow', attrs=['bold']),
        colored("Naive Spills", 'yellow', attrs=['bold']),
        colored("Naive Time (s)", 'yellow', attrs=['bold']),
        colored("Naive Memory (KB)", 'yellow', attrs=['bold']),
        colored("Advanced Spills", 'yellow', attrs=['bold']),
        colored("Advanced Time (s)", 'yellow', attrs=['bold']),
        colored("Advanced Memory (KB)", 'yellow', attrs=['bold'])
    ]

    # Print the results in a table format
    print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    run_tests()

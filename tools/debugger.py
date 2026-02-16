"""
Mythos Debugger - Debug Mythos programs
"""
from typing import Dict, List, Set, Optional, Any
from compiler.bytecode.compiler import OpCode, Instruction
from runtime.vm import VirtualMachine

class Breakpoint:
    """Debugger breakpoint"""
    def __init__(self, line: int, condition: str = None):
        self.line = line
        self.condition = condition
        self.enabled = True
        self.hit_count = 0

class DebuggerState:
    """Current debugger state"""
    def __init__(self):
        self.running = False
        self.paused = False
        self.current_line = 0
        self.call_stack: List[Dict] = []
        self.variables: Dict[str, Any] = {}

class Debugger:
    """Mythos debugger"""
    def __init__(self, vm: VirtualMachine):
        self.vm = vm
        self.breakpoints: Dict[int, Breakpoint] = {}
        self.state = DebuggerState()
        self.step_mode = False
        self.watch_expressions: List[str] = []
    
    def add_breakpoint(self, line: int, condition: str = None):
        """Add a breakpoint"""
        self.breakpoints[line] = Breakpoint(line, condition)
        print(f"Breakpoint added at line {line}")
    
    def remove_breakpoint(self, line: int):
        """Remove a breakpoint"""
        if line in self.breakpoints:
            del self.breakpoints[line]
            print(f"Breakpoint removed from line {line}")
    
    def toggle_breakpoint(self, line: int):
        """Toggle breakpoint enabled/disabled"""
        if line in self.breakpoints:
            bp = self.breakpoints[line]
            bp.enabled = not bp.enabled
            status = "enabled" if bp.enabled else "disabled"
            print(f"Breakpoint at line {line} {status}")
    
    def list_breakpoints(self):
        """List all breakpoints"""
        if not self.breakpoints:
            print("No breakpoints set")
            return
        
        print("Breakpoints:")
        for line, bp in sorted(self.breakpoints.items()):
            status = "enabled" if bp.enabled else "disabled"
            condition = f" (condition: {bp.condition})" if bp.condition else ""
            print(f"  Line {line}: {status}, hits: {bp.hit_count}{condition}")
    
    def add_watch(self, expression: str):
        """Add watch expression"""
        self.watch_expressions.append(expression)
        print(f"Watch added: {expression}")
    
    def remove_watch(self, expression: str):
        """Remove watch expression"""
        if expression in self.watch_expressions:
            self.watch_expressions.remove(expression)
            print(f"Watch removed: {expression}")
    
    def list_watches(self):
        """List all watch expressions"""
        if not self.watch_expressions:
            print("No watch expressions")
            return
        
        print("Watch expressions:")
        for expr in self.watch_expressions:
            try:
                # Evaluate expression in current context
                value = self._evaluate_expression(expr)
                print(f"  {expr} = {value}")
            except Exception as e:
                print(f"  {expr} = <error: {e}>")
    
    def step_over(self):
        """Step over current line"""
        self.step_mode = True
        self.state.paused = False
        print("Stepping over...")
    
    def step_into(self):
        """Step into function call"""
        self.step_mode = True
        self.state.paused = False
        print("Stepping into...")
    
    def step_out(self):
        """Step out of current function"""
        self.step_mode = True
        self.state.paused = False
        print("Stepping out...")
    
    def continue_execution(self):
        """Continue execution until next breakpoint"""
        self.step_mode = False
        self.state.paused = False
        print("Continuing...")
    
    def pause(self):
        """Pause execution"""
        self.state.paused = True
        print("Paused")
    
    def print_stack_trace(self):
        """Print current call stack"""
        if not self.state.call_stack:
            print("Call stack is empty")
            return
        
        print("Call stack:")
        for i, frame in enumerate(reversed(self.state.call_stack)):
            func_name = frame.get('function', '<main>')
            line = frame.get('line', 0)
            print(f"  #{i}: {func_name} at line {line}")
    
    def print_variables(self):
        """Print current variables"""
        print("Variables:")
        
        # Local variables
        if self.vm.current_frame:
            print("  Local:")
            for name, value in self.vm.current_frame.locals.items():
                print(f"    {name} = {value}")
        
        # Global variables
        print("  Global:")
        for name, value in self.vm.globals.items():
            if not callable(value):
                print(f"    {name} = {value}")
    
    def evaluate(self, expression: str):
        """Evaluate expression in current context"""
        try:
            result = self._evaluate_expression(expression)
            print(f"{expression} = {result}")
        except Exception as e:
            print(f"Error evaluating expression: {e}")
    
    def _evaluate_expression(self, expression: str) -> Any:
        """Evaluate expression (simplified)"""
        # In real implementation, would parse and evaluate properly
        # For now, just try to get variable value
        if self.vm.current_frame and expression in self.vm.current_frame.locals:
            return self.vm.current_frame.locals[expression]
        if expression in self.vm.globals:
            return self.vm.globals[expression]
        raise NameError(f"Variable '{expression}' not found")
    
    def run(self, instructions: List[Instruction], constants: List[Any]):
        """Run program with debugging"""
        self.state.running = True
        self.state.paused = False
        
        print("Debugger started. Type 'help' for commands.")
        
        # This would integrate with the VM to step through execution
        # For now, just run normally
        self.vm.execute(instructions, constants)
        
        self.state.running = False
        print("Program finished")

class Profiler:
    """Performance profiler for Mythos"""
    def __init__(self):
        self.function_times: Dict[str, float] = {}
        self.function_calls: Dict[str, int] = {}
        self.instruction_counts: Dict[OpCode, int] = {}
        self.enabled = False
    
    def start(self):
        """Start profiling"""
        self.enabled = True
        self.function_times.clear()
        self.function_calls.clear()
        self.instruction_counts.clear()
        print("Profiler started")
    
    def stop(self):
        """Stop profiling"""
        self.enabled = False
        print("Profiler stopped")
    
    def record_function_call(self, function_name: str, duration: float):
        """Record function call"""
        if not self.enabled:
            return
        
        if function_name not in self.function_times:
            self.function_times[function_name] = 0.0
            self.function_calls[function_name] = 0
        
        self.function_times[function_name] += duration
        self.function_calls[function_name] += 1
    
    def record_instruction(self, opcode: OpCode):
        """Record instruction execution"""
        if not self.enabled:
            return
        
        if opcode not in self.instruction_counts:
            self.instruction_counts[opcode] = 0
        
        self.instruction_counts[opcode] += 1
    
    def print_report(self):
        """Print profiling report"""
        print("\n=== Profiling Report ===\n")
        
        # Function statistics
        if self.function_times:
            print("Function Statistics:")
            print(f"{'Function':<30} {'Calls':<10} {'Total Time':<15} {'Avg Time':<15}")
            print("-" * 70)
            
            for func_name in sorted(self.function_times.keys(), key=lambda x: self.function_times[x], reverse=True):
                calls = self.function_calls[func_name]
                total_time = self.function_times[func_name]
                avg_time = total_time / calls if calls > 0 else 0
                
                print(f"{func_name:<30} {calls:<10} {total_time:<15.6f} {avg_time:<15.6f}")
        
        # Instruction statistics
        if self.instruction_counts:
            print("\nInstruction Statistics:")
            print(f"{'Instruction':<30} {'Count':<15}")
            print("-" * 45)
            
            total_instructions = sum(self.instruction_counts.values())
            for opcode in sorted(self.instruction_counts.keys(), key=lambda x: self.instruction_counts[x], reverse=True):
                count = self.instruction_counts[opcode]
                percentage = (count / total_instructions) * 100 if total_instructions > 0 else 0
                print(f"{opcode.name:<30} {count:<10} ({percentage:.2f}%)")
            
            print(f"\nTotal instructions executed: {total_instructions}")

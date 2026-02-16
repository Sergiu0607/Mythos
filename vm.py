"""
Mythos Virtual Machine - Executes bytecode
"""
from typing import List, Dict, Any, Optional
from compiler.bytecode.compiler import OpCode, Instruction
import math

class MythosFunction:
    def __init__(self, name: str, params: List[str], instructions: List[Instruction], constants: List[Any]):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.constants = constants
    
    def __repr__(self):
        return f"<function {self.name}>"

class MythosObject:
    def __init__(self, properties: Dict[str, Any] = None):
        self.properties = properties or {}
    
    def get(self, key: str):
        return self.properties.get(key)
    
    def set(self, key: str, value: Any):
        self.properties[key] = value
    
    def __repr__(self):
        return f"<object {self.properties}>"

class CallFrame:
    def __init__(self, function: MythosFunction, return_address: int):
        self.function = function
        self.return_address = return_address
        self.locals: Dict[str, Any] = {}
        self.ip = 0  # Instruction pointer

class VirtualMachine:
    def __init__(self):
        self.stack: List[Any] = []
        self.globals: Dict[str, Any] = {}
        self.call_stack: List[CallFrame] = []
        self.current_frame: Optional[CallFrame] = None
        self.ip = 0  # Instruction pointer
        
        # Initialize built-in functions
        self._init_builtins()
    
    def _init_builtins(self):
        """Initialize built-in functions and constants"""
        self.globals['print'] = self._builtin_print
        self.globals['len'] = self._builtin_len
        self.globals['range'] = self._builtin_range
        self.globals['sqrt'] = lambda x: math.sqrt(x)
        self.globals['sin'] = lambda x: math.sin(x)
        self.globals['cos'] = lambda x: math.cos(x)
        self.globals['tan'] = lambda x: math.tan(x)
        self.globals['abs'] = lambda x: abs(x)
        self.globals['min'] = lambda *args: min(args)
        self.globals['max'] = lambda *args: max(args)
        self.globals['floor'] = lambda x: math.floor(x)
        self.globals['ceil'] = lambda x: math.ceil(x)
        self.globals['round'] = lambda x: round(x)
        self.globals['pi'] = math.pi
        self.globals['e'] = math.e
    
    def _builtin_print(self, *args):
        print(*args)
        return None
    
    def _builtin_len(self, obj):
        if isinstance(obj, (list, str, dict)):
            return len(obj)
        return 0
    
    def _builtin_range(self, *args):
        return list(range(*args))
    
    def push(self, value: Any):
        self.stack.append(value)
    
    def pop(self) -> Any:
        if not self.stack:
            raise RuntimeError("Stack underflow")
        return self.stack.pop()
    
    def peek(self) -> Any:
        if not self.stack:
            raise RuntimeError("Stack is empty")
        return self.stack[-1]
    
    def get_variable(self, name: str) -> Any:
        # Check local scope first
        if self.current_frame and name in self.current_frame.locals:
            return self.current_frame.locals[name]
        
        # Then check global scope
        if name in self.globals:
            return self.globals[name]
        
        raise NameError(f"Variable '{name}' is not defined")
    
    def set_variable(self, name: str, value: Any):
        # Set in current frame if exists, otherwise global
        if self.current_frame:
            self.current_frame.locals[name] = value
        else:
            self.globals[name] = value
    
    def execute(self, instructions: List[Instruction], constants: List[Any]):
        """Execute bytecode instructions"""
        self.ip = 0
        
        while self.ip < len(instructions):
            instr = instructions[self.ip]
            opcode = instr.opcode
            arg = instr.arg
            
            # Stack operations
            if opcode == OpCode.LOAD_CONST:
                self.push(constants[arg])
            
            elif opcode == OpCode.LOAD_VAR:
                value = self.get_variable(arg)
                self.push(value)
            
            elif opcode == OpCode.STORE_VAR:
                value = self.pop()
                self.set_variable(arg, value)
                # Don't push back - assignments don't return values
            
            elif opcode == OpCode.POP:
                self.pop()
            
            elif opcode == OpCode.DUP:
                self.push(self.peek())
            
            # Arithmetic operations
            elif opcode == OpCode.ADD:
                right = self.pop()
                left = self.pop()
                self.push(left + right)
            
            elif opcode == OpCode.SUB:
                right = self.pop()
                left = self.pop()
                self.push(left - right)
            
            elif opcode == OpCode.MUL:
                right = self.pop()
                left = self.pop()
                self.push(left * right)
            
            elif opcode == OpCode.DIV:
                right = self.pop()
                left = self.pop()
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                self.push(left / right)
            
            elif opcode == OpCode.POW:
                right = self.pop()
                left = self.pop()
                self.push(left ** right)
            
            elif opcode == OpCode.MOD:
                right = self.pop()
                left = self.pop()
                self.push(left % right)
            
            elif opcode == OpCode.NEG:
                value = self.pop()
                self.push(-value)
            
            # Comparison operations
            elif opcode == OpCode.EQ:
                right = self.pop()
                left = self.pop()
                self.push(left == right)
            
            elif opcode == OpCode.NE:
                right = self.pop()
                left = self.pop()
                self.push(left != right)
            
            elif opcode == OpCode.LT:
                right = self.pop()
                left = self.pop()
                self.push(left < right)
            
            elif opcode == OpCode.GT:
                right = self.pop()
                left = self.pop()
                self.push(left > right)
            
            elif opcode == OpCode.LE:
                right = self.pop()
                left = self.pop()
                self.push(left <= right)
            
            elif opcode == OpCode.GE:
                right = self.pop()
                left = self.pop()
                self.push(left >= right)
            
            # Logical operations
            elif opcode == OpCode.AND:
                right = self.pop()
                left = self.pop()
                self.push(left and right)
            
            elif opcode == OpCode.OR:
                right = self.pop()
                left = self.pop()
                self.push(left or right)
            
            elif opcode == OpCode.NOT:
                value = self.pop()
                self.push(not value)
            
            # Control flow
            elif opcode == OpCode.JUMP:
                self.ip = arg
                continue
            
            elif opcode == OpCode.JUMP_IF_FALSE:
                condition = self.pop()
                if not condition:
                    self.ip = arg
                    continue
            
            elif opcode == OpCode.JUMP_IF_TRUE:
                condition = self.pop()
                if condition:
                    self.ip = arg
                    continue
            
            # Function operations
            elif opcode == OpCode.CALL:
                arg_count = arg
                args = [self.pop() for _ in range(arg_count)]
                args.reverse()
                
                callee = self.pop()
                
                # Handle built-in functions
                if callable(callee) and not isinstance(callee, MythosFunction):
                    result = callee(*args)
                    # Only push result if it's not None (print returns None)
                    # This prevents stack buildup
                
                # Handle Mythos functions
                elif isinstance(callee, MythosFunction):
                    # Create new call frame
                    frame = CallFrame(callee, self.ip + 1)
                    
                    # Bind parameters
                    for i, param in enumerate(callee.params):
                        if i < len(args):
                            frame.locals[param] = args[i]
                        else:
                            frame.locals[param] = None
                    
                    # Push frame and execute
                    self.call_stack.append(frame)
                    old_frame = self.current_frame
                    self.current_frame = frame
                    
                    # Execute function
                    result = self.execute(callee.instructions, callee.constants)
                    
                    # Restore frame
                    self.call_stack.pop()
                    self.current_frame = old_frame
                    
                    self.push(result if result is not None else None)
                    self.ip = frame.return_address
                    continue
            
            elif opcode == OpCode.RETURN:
                value = self.pop()
                return value
            
            elif opcode == OpCode.MAKE_FUNCTION:
                func_data = constants[arg]
                func = MythosFunction(
                    func_data['name'],
                    func_data['params'],
                    func_data['instructions'],
                    func_data['constants']
                )
                self.push(func)
            
            # Object operations
            elif opcode == OpCode.MAKE_ARRAY:
                count = arg
                elements = [self.pop() for _ in range(count)]
                elements.reverse()
                self.push(elements)
            
            elif opcode == OpCode.MAKE_OBJECT:
                count = arg
                obj = MythosObject()
                for _ in range(count):
                    value = self.pop()
                    key = self.pop()
                    obj.set(key, value)
                self.push(obj)
            
            elif opcode == OpCode.GET_MEMBER:
                member_name = constants[arg]
                obj = self.pop()
                
                if isinstance(obj, MythosObject):
                    self.push(obj.get(member_name))
                elif isinstance(obj, dict):
                    self.push(obj.get(member_name))
                else:
                    raise AttributeError(f"Object has no member '{member_name}'")
            
            elif opcode == OpCode.GET_INDEX:
                index = self.pop()
                obj = self.pop()
                
                if isinstance(obj, (list, str, dict)):
                    self.push(obj[index])
                else:
                    raise TypeError("Object is not indexable")
            
            # Import
            elif opcode == OpCode.IMPORT:
                module_name = constants[arg]
                # Import logic would go here
                pass
            
            self.ip += 1
        
        return None

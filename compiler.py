"""
Mythos Bytecode Compiler - Compiles AST to bytecode
"""
from typing import List, Dict, Any
from compiler.ast.nodes import *
from enum import Enum, auto

class OpCode(Enum):
    # Stack operations
    LOAD_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    POP = auto()
    DUP = auto()
    
    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    MOD = auto()
    NEG = auto()
    
    # Comparison
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Control flow
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    JUMP_IF_TRUE = auto()
    
    # Functions
    CALL = auto()
    RETURN = auto()
    MAKE_FUNCTION = auto()
    
    # Objects
    MAKE_ARRAY = auto()
    MAKE_OBJECT = auto()
    GET_MEMBER = auto()
    SET_MEMBER = auto()
    GET_INDEX = auto()
    SET_INDEX = auto()
    
    # Special
    PRINT = auto()
    IMPORT = auto()
    
    # Graphics
    CREATE_SCENE = auto()
    ADD_SCENE_ELEMENT = auto()
    
    # Web
    CREATE_WEB_APP = auto()
    ADD_ROUTE = auto()

class Instruction:
    def __init__(self, opcode: OpCode, arg=None):
        self.opcode = opcode
        self.arg = arg
    
    def __repr__(self):
        if self.arg is not None:
            return f"{self.opcode.name} {self.arg}"
        return self.opcode.name

class BytecodeCompiler:
    def __init__(self):
        self.instructions: List[Instruction] = []
        self.constants: List[Any] = []
        self.labels: Dict[str, int] = {}
        self.label_counter = 0
        
    def new_label(self) -> str:
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, opcode: OpCode, arg=None):
        self.instructions.append(Instruction(opcode, arg))
    
    def add_constant(self, value: Any) -> int:
        if value in self.constants:
            return self.constants.index(value)
        self.constants.append(value)
        return len(self.constants) - 1
    
    def mark_label(self, label: str):
        self.labels[label] = len(self.instructions)
    
    def compile(self, node: ASTNode):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.compile(stmt)
                # Don't auto-pop - let statements handle their own stack management
        
        elif isinstance(node, NumberNode):
            const_idx = self.add_constant(node.value)
            self.emit(OpCode.LOAD_CONST, const_idx)
        
        elif isinstance(node, StringNode):
            const_idx = self.add_constant(node.value)
            self.emit(OpCode.LOAD_CONST, const_idx)
        
        elif isinstance(node, BooleanNode):
            const_idx = self.add_constant(node.value)
            self.emit(OpCode.LOAD_CONST, const_idx)
        
        elif isinstance(node, NullNode):
            const_idx = self.add_constant(None)
            self.emit(OpCode.LOAD_CONST, const_idx)
        
        elif isinstance(node, IdentifierNode):
            self.emit(OpCode.LOAD_VAR, node.name)
        
        elif isinstance(node, BinaryOpNode):
            self.compile(node.left)
            self.compile(node.right)
            
            op_map = {
                '+': OpCode.ADD,
                '-': OpCode.SUB,
                '*': OpCode.MUL,
                '/': OpCode.DIV,
                '^': OpCode.POW,
                '%': OpCode.MOD,
                '==': OpCode.EQ,
                '!=': OpCode.NE,
                '<': OpCode.LT,
                '>': OpCode.GT,
                '<=': OpCode.LE,
                '>=': OpCode.GE,
                'and': OpCode.AND,
                'or': OpCode.OR,
            }
            
            if node.operator in op_map:
                self.emit(op_map[node.operator])
        
        elif isinstance(node, UnaryOpNode):
            self.compile(node.operand)
            
            if node.operator == '-':
                self.emit(OpCode.NEG)
            elif node.operator == 'not':
                self.emit(OpCode.NOT)
        
        elif isinstance(node, AssignmentNode):
            self.compile(node.value)
            self.emit(OpCode.STORE_VAR, node.name)
            # Don't leave value on stack
        
        elif isinstance(node, VariableDeclarationNode):
            if node.value:
                self.compile(node.value)
            else:
                const_idx = self.add_constant(None)
                self.emit(OpCode.LOAD_CONST, const_idx)
            self.emit(OpCode.STORE_VAR, node.name)
            # Don't leave value on stack
        
        elif isinstance(node, CallNode):
            # Compile callee first
            self.compile(node.callee)
            
            # Then compile arguments
            for arg in node.arguments:
                self.compile(arg)
            
            # Call with argument count
            self.emit(OpCode.CALL, len(node.arguments))
        
        elif isinstance(node, MemberAccessNode):
            self.compile(node.object)
            const_idx = self.add_constant(node.member)
            self.emit(OpCode.GET_MEMBER, const_idx)
        
        elif isinstance(node, IndexAccessNode):
            self.compile(node.object)
            self.compile(node.index)
            self.emit(OpCode.GET_INDEX)
        
        elif isinstance(node, ArrayNode):
            for element in node.elements:
                self.compile(element)
            self.emit(OpCode.MAKE_ARRAY, len(node.elements))
        
        elif isinstance(node, ObjectNode):
            for key, value in node.properties.items():
                const_idx = self.add_constant(key)
                self.emit(OpCode.LOAD_CONST, const_idx)
                self.compile(value)
            self.emit(OpCode.MAKE_OBJECT, len(node.properties))
        
        elif isinstance(node, IfNode):
            else_label = self.new_label()
            end_label = self.new_label()
            
            # Compile condition
            self.compile(node.condition)
            self.emit(OpCode.JUMP_IF_FALSE, else_label)
            
            # Then body
            for stmt in node.then_body:
                self.compile(stmt)
            self.emit(OpCode.JUMP, end_label)
            
            # Else body
            self.mark_label(else_label)
            if node.else_body:
                for stmt in node.else_body:
                    self.compile(stmt)
            
            self.mark_label(end_label)
        
        elif isinstance(node, WhileNode):
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.mark_label(start_label)
            self.compile(node.condition)
            self.emit(OpCode.JUMP_IF_FALSE, end_label)
            
            for stmt in node.body:
                self.compile(stmt)
            
            self.emit(OpCode.JUMP, start_label)
            self.mark_label(end_label)
        
        elif isinstance(node, ForNode):
            # For loops are compiled as while loops with iterators
            start_label = self.new_label()
            end_label = self.new_label()
            
            # Get iterator
            self.compile(node.iterable)
            iter_var = f"__iter_{self.label_counter}"
            self.emit(OpCode.STORE_VAR, iter_var)
            
            self.mark_label(start_label)
            # Check if iterator has next
            self.emit(OpCode.LOAD_VAR, iter_var)
            # ... iterator logic would go here
            
            for stmt in node.body:
                self.compile(stmt)
            
            self.emit(OpCode.JUMP, start_label)
            self.mark_label(end_label)
        
        elif isinstance(node, FunctionNode):
            # Create a new compiler for the function body
            func_compiler = BytecodeCompiler()
            for stmt in node.body:
                func_compiler.compile(stmt)
            func_compiler.emit(OpCode.RETURN)
            
            # Store function as constant
            func_data = {
                'name': node.name,
                'params': node.parameters,
                'instructions': func_compiler.instructions,
                'constants': func_compiler.constants
            }
            const_idx = self.add_constant(func_data)
            self.emit(OpCode.MAKE_FUNCTION, const_idx)
            self.emit(OpCode.STORE_VAR, node.name)
        
        elif isinstance(node, ReturnNode):
            if node.value:
                self.compile(node.value)
            else:
                const_idx = self.add_constant(None)
                self.emit(OpCode.LOAD_CONST, const_idx)
            self.emit(OpCode.RETURN)
        
        elif isinstance(node, ImportNode):
            const_idx = self.add_constant(node.module)
            self.emit(OpCode.IMPORT, const_idx)
        
        elif isinstance(node, SceneNode):
            const_idx = self.add_constant(node.name)
            self.emit(OpCode.CREATE_SCENE, const_idx)
            
            for element in node.elements:
                self.compile(element)
        
        elif isinstance(node, SceneElementNode):
            # Compile properties
            for key, value in element.properties.items():
                const_idx = self.add_constant(key)
                self.emit(OpCode.LOAD_CONST, const_idx)
                self.compile(value)
            
            const_idx = self.add_constant(element.element_type)
            self.emit(OpCode.ADD_SCENE_ELEMENT, const_idx)
        
        elif isinstance(node, WebAppNode):
            self.emit(OpCode.CREATE_WEB_APP)
            
            for route in node.routes:
                self.compile(route)
        
        elif isinstance(node, RouteNode):
            const_idx = self.add_constant(node.path)
            self.emit(OpCode.LOAD_CONST, const_idx)
            
            # Compile route handler as function
            route_compiler = BytecodeCompiler()
            for stmt in node.body:
                route_compiler.compile(stmt)
            
            route_data = {
                'instructions': route_compiler.instructions,
                'constants': route_compiler.constants
            }
            handler_idx = self.add_constant(route_data)
            self.emit(OpCode.ADD_ROUTE, handler_idx)
    
    def resolve_labels(self):
        """Resolve label references to actual instruction indices"""
        for i, instr in enumerate(self.instructions):
            if isinstance(instr.arg, str) and instr.arg in self.labels:
                instr.arg = self.labels[instr.arg]
    
    def get_bytecode(self):
        self.resolve_labels()
        return {
            'instructions': self.instructions,
            'constants': self.constants
        }

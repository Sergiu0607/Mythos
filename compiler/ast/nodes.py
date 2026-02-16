"""
Mythos AST Node Definitions
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

@dataclass
class NumberNode(ASTNode):
    value: float

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class BooleanNode(ASTNode):
    value: bool

@dataclass
class NullNode(ASTNode):
    pass

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class AssignmentNode(ASTNode):
    name: str
    value: ASTNode

@dataclass
class VariableDeclarationNode(ASTNode):
    name: str
    value: Optional[ASTNode]
    kind: str  # 'let', 'const', 'var'

@dataclass
class CallNode(ASTNode):
    callee: ASTNode
    arguments: List[ASTNode]

@dataclass
class MemberAccessNode(ASTNode):
    object: ASTNode
    member: str

@dataclass
class IndexAccessNode(ASTNode):
    object: ASTNode
    index: ASTNode

@dataclass
class ArrayNode(ASTNode):
    elements: List[ASTNode]

@dataclass
class ObjectNode(ASTNode):
    properties: Dict[str, ASTNode]

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]]

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class ForNode(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionNode(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]

@dataclass
class ClassNode(ASTNode):
    name: str
    parent: Optional[str]
    methods: List[FunctionNode]

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode]

@dataclass
class BreakNode(ASTNode):
    pass

@dataclass
class ContinueNode(ASTNode):
    pass

@dataclass
class ImportNode(ASTNode):
    module: str

@dataclass
class SceneNode(ASTNode):
    name: str
    elements: List['SceneElementNode']

@dataclass
class SceneElementNode(ASTNode):
    element_type: str
    properties: Dict[str, ASTNode]

@dataclass
class WebAppNode(ASTNode):
    routes: List['RouteNode']

@dataclass
class RouteNode(ASTNode):
    path: str
    body: List[ASTNode]

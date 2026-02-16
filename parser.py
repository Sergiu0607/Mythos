"""
Mythos Parser - Builds Abstract Syntax Tree from tokens
"""
from typing import List, Optional, Union
from compiler.lexer.lexer import Token, TokenType
from compiler.ast.nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        
    def current_token(self) -> Optional[Token]:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def peek_token(self, offset=1) -> Optional[Token]:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self):
        self.pos += 1
        # Skip newlines in most contexts
        while self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.pos += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if not token or token.type != token_type:
            raise SyntaxError(f"Expected {token_type.name}, got {token.type.name if token else 'EOF'}")
        self.advance()
        return token
    
    def parse(self) -> ProgramNode:
        statements = []
        while self.current_token() and self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)
    
    def parse_statement(self):
        token = self.current_token()
        
        if not token:
            return None
        
        # Variable declaration
        if token.type == TokenType.IDENTIFIER:
            return self.parse_assignment_or_expression()
        
        # Keywords
        if token.type == TokenType.KEYWORD:
            keyword = token.value
            
            if keyword == 'if':
                return self.parse_if_statement()
            elif keyword == 'while':
                return self.parse_while_statement()
            elif keyword == 'for':
                return self.parse_for_statement()
            elif keyword == 'function':
                return self.parse_function_declaration()
            elif keyword == 'class':
                return self.parse_class_declaration()
            elif keyword == 'return':
                return self.parse_return_statement()
            elif keyword == 'import':
                return self.parse_import_statement()
            elif keyword == 'scene':
                return self.parse_scene_declaration()
            elif keyword == 'web':
                return self.parse_web_declaration()
            elif keyword in ('let', 'const', 'var'):
                return self.parse_variable_declaration()
            elif keyword == 'break':
                self.advance()
                return BreakNode()
            elif keyword == 'continue':
                self.advance()
                return ContinueNode()
        
        # Expression statement
        return self.parse_expression_statement()
    
    def parse_variable_declaration(self):
        kind_token = self.current_token()
        kind = kind_token.value
        self.advance()
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        value = None
        if self.current_token() and self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        
        return VariableDeclarationNode(name, value, kind)
    
    def parse_assignment_or_expression(self):
        expr = self.parse_expression()
        
        # Check for assignment
        if self.current_token() and self.current_token().type == TokenType.ASSIGN:
            if not isinstance(expr, IdentifierNode):
                raise SyntaxError("Invalid assignment target")
            self.advance()
            value = self.parse_expression()
            return AssignmentNode(expr.name, value)
        
        return expr
    
    def parse_expression_statement(self):
        expr = self.parse_expression()
        return expr
    
    def parse_if_statement(self):
        self.expect(TokenType.KEYWORD)  # 'if'
        condition = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        then_body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            then_body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        else_body = None
        if self.current_token() and self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'else':
            self.advance()
            self.expect(TokenType.LBRACE)
            else_body = []
            while self.current_token() and self.current_token().type != TokenType.RBRACE:
                if self.current_token().type == TokenType.NEWLINE:
                    self.advance()
                    continue
                else_body.append(self.parse_statement())
            self.expect(TokenType.RBRACE)
        
        return IfNode(condition, then_body, else_body)
    
    def parse_while_statement(self):
        self.expect(TokenType.KEYWORD)  # 'while'
        condition = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return WhileNode(condition, body)
    
    def parse_for_statement(self):
        self.expect(TokenType.KEYWORD)  # 'for'
        var_token = self.expect(TokenType.IDENTIFIER)
        var_name = var_token.value
        
        self.expect(TokenType.KEYWORD)  # 'in'
        iterable = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return ForNode(var_name, iterable, body)
    
    def parse_function_declaration(self):
        self.expect(TokenType.KEYWORD)  # 'function'
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        params = []
        while self.current_token() and self.current_token().type != TokenType.RPAREN:
            param_token = self.expect(TokenType.IDENTIFIER)
            params.append(param_token.value)
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return FunctionNode(name, params, body)
    
    def parse_class_declaration(self):
        self.expect(TokenType.KEYWORD)  # 'class'
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        parent = None
        if self.current_token() and self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'extends':
            self.advance()
            parent_token = self.expect(TokenType.IDENTIFIER)
            parent = parent_token.value
        
        self.expect(TokenType.LBRACE)
        methods = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            if self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'function':
                methods.append(self.parse_function_declaration())
        self.expect(TokenType.RBRACE)
        
        return ClassNode(name, parent, methods)
    
    def parse_return_statement(self):
        self.expect(TokenType.KEYWORD)  # 'return'
        value = None
        if self.current_token() and self.current_token().type not in (TokenType.NEWLINE, TokenType.RBRACE):
            value = self.parse_expression()
        return ReturnNode(value)
    
    def parse_import_statement(self):
        self.expect(TokenType.KEYWORD)  # 'import'
        module_token = self.expect(TokenType.IDENTIFIER)
        module = module_token.value
        return ImportNode(module)
    
    def parse_scene_declaration(self):
        self.expect(TokenType.KEYWORD)  # 'scene'
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LBRACE)
        elements = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            elements.append(self.parse_scene_element())
        self.expect(TokenType.RBRACE)
        
        return SceneNode(name, elements)
    
    def parse_scene_element(self):
        element_type_token = self.expect(TokenType.IDENTIFIER)
        element_type = element_type_token.value
        
        properties = {}
        while self.current_token() and self.current_token().type == TokenType.IDENTIFIER:
            prop_name = self.current_token().value
            self.advance()
            self.expect(TokenType.COLON)
            prop_value = self.parse_expression()
            properties[prop_name] = prop_value
        
        return SceneElementNode(element_type, properties)
    
    def parse_web_declaration(self):
        self.expect(TokenType.KEYWORD)  # 'web'
        self.expect(TokenType.DOT)
        app_token = self.expect(TokenType.IDENTIFIER)
        
        self.expect(TokenType.LBRACE)
        routes = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            routes.append(self.parse_route())
        self.expect(TokenType.RBRACE)
        
        return WebAppNode(routes)
    
    def parse_route(self):
        self.expect(TokenType.KEYWORD)  # 'route'
        path_token = self.expect(TokenType.STRING)
        path = path_token.value
        
        self.expect(TokenType.LBRACE)
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return RouteNode(path, body)
    
    def parse_expression(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.current_token() and self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'or':
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOpNode('or', left, right)
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_equality()
        
        while self.current_token() and self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'and':
            self.advance()
            right = self.parse_equality()
            left = BinaryOpNode('and', left, right)
        
        return left
    
    def parse_equality(self):
        left = self.parse_comparison()
        
        while self.current_token() and self.current_token().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.current_token().value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOpNode(op, left, right)
        
        return left
    
    def parse_comparison(self):
        left = self.parse_addition()
        
        while self.current_token() and self.current_token().type in (TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.current_token().value
            self.advance()
            right = self.parse_addition()
            left = BinaryOpNode(op, left, right)
        
        return left
    
    def parse_addition(self):
        left = self.parse_multiplication()
        
        while self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplication()
            left = BinaryOpNode(op, left, right)
        
        return left
    
    def parse_multiplication(self):
        left = self.parse_power()
        
        while self.current_token() and self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current_token().value
            self.advance()
            right = self.parse_power()
            left = BinaryOpNode(op, left, right)
        
        return left
    
    def parse_power(self):
        left = self.parse_unary()
        
        if self.current_token() and self.current_token().type == TokenType.POWER:
            self.advance()
            right = self.parse_power()  # Right associative
            return BinaryOpNode('^', left, right)
        
        return left
    
    def parse_unary(self):
        if self.current_token() and self.current_token().type == TokenType.MINUS:
            self.advance()
            expr = self.parse_unary()
            return UnaryOpNode('-', expr)
        
        if self.current_token() and self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'not':
            self.advance()
            expr = self.parse_unary()
            return UnaryOpNode('not', expr)
        
        return self.parse_postfix()
    
    def parse_postfix(self):
        expr = self.parse_primary()
        
        while True:
            if self.current_token() and self.current_token().type == TokenType.LPAREN:
                # Function call
                self.advance()
                args = []
                while self.current_token() and self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current_token() and self.current_token().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
                expr = CallNode(expr, args)
            elif self.current_token() and self.current_token().type == TokenType.DOT:
                # Member access
                self.advance()
                member_token = self.expect(TokenType.IDENTIFIER)
                expr = MemberAccessNode(expr, member_token.value)
            elif self.current_token() and self.current_token().type == TokenType.LBRACKET:
                # Index access
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexAccessNode(expr, index)
            else:
                break
        
        return expr
    
    def parse_primary(self):
        token = self.current_token()
        
        if not token:
            raise SyntaxError("Unexpected end of input")
        
        # Numbers
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        # Strings
        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)
        
        # Booleans
        if token.type == TokenType.BOOLEAN:
            self.advance()
            return BooleanNode(token.value)
        
        # Null
        if token.type == TokenType.NULL:
            self.advance()
            return NullNode()
        
        # Identifiers
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return IdentifierNode(token.value)
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Array literal
        if token.type == TokenType.LBRACKET:
            return self.parse_array_literal()
        
        # Object literal
        if token.type == TokenType.LBRACE:
            return self.parse_object_literal()
        
        raise SyntaxError(f"Unexpected token: {token}")
    
    def parse_array_literal(self):
        self.expect(TokenType.LBRACKET)
        elements = []
        while self.current_token() and self.current_token().type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RBRACKET)
        return ArrayNode(elements)
    
    def parse_object_literal(self):
        self.expect(TokenType.LBRACE)
        properties = {}
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            key_token = self.expect(TokenType.IDENTIFIER)
            key = key_token.value
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            properties[key] = value
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RBRACE)
        return ObjectNode(properties)

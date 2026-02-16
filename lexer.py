"""
Mythos Lexer - Tokenizes source code into tokens
"""
import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers and Keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    MODULO = auto()
    
    # Comparison
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Assignment
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    ARROW = auto()
    
    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"

class Lexer:
    KEYWORDS = {
        'if', 'else', 'elif', 'while', 'for', 'in', 'break', 'continue',
        'function', 'return', 'class', 'extends', 'new', 'this', 'super',
        'import', 'from', 'export', 'as', 'true', 'false', 'null',
        'and', 'or', 'not', 'is', 'scene', 'route', 'web', 'ui',
        'let', 'const', 'var', 'async', 'await', 'try', 'catch', 'finally',
        'throw', 'with', 'match', 'case', 'default'
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]
        
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        value = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_string(self, quote_char: str) -> Token:
        start_line, start_col = self.line, self.column
        self.advance()  # Skip opening quote
        string_val = ''
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    string_val += '\n'
                elif escape_char == 't':
                    string_val += '\t'
                elif escape_char == 'r':
                    string_val += '\r'
                elif escape_char == '\\':
                    string_val += '\\'
                elif escape_char == quote_char:
                    string_val += quote_char
                else:
                    string_val += escape_char
                self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_val, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        if identifier in self.KEYWORDS:
            if identifier in ('true', 'false'):
                return Token(TokenType.BOOLEAN, identifier == 'true', start_line, start_col)
            elif identifier == 'null':
                return Token(TokenType.NULL, None, start_line, start_col)
            return Token(TokenType.KEYWORD, identifier, start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, identifier, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Comments
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            # Newlines
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in ('"', "'"):
                self.tokens.append(self.read_string(self.current_char()))
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and delimiters
            char = self.current_char()
            line, col = self.line, self.column
            
            if char == '+':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', line, col))
                else:
                    self.tokens.append(Token(TokenType.PLUS, '+', line, col))
            elif char == '-':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', line, col))
                elif self.current_char() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, '->', line, col))
                else:
                    self.tokens.append(Token(TokenType.MINUS, '-', line, col))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', line, col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', line, col))
            elif char == '^':
                self.advance()
                self.tokens.append(Token(TokenType.POWER, '^', line, col))
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', line, col))
            elif char == '=':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUAL, '==', line, col))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', line, col))
            elif char == '!':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, col))
            elif char == '<':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', line, col))
                else:
                    self.tokens.append(Token(TokenType.LESS_THAN, '<', line, col))
            elif char == '>':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, col))
                else:
                    self.tokens.append(Token(TokenType.GREATER_THAN, '>', line, col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', line, col))
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', line, col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', line, col))
            elif char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', line, col))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', line, col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
            else:
                raise SyntaxError(f"Unexpected character '{char}' at {line}:{col}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

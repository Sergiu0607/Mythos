"""
Tests for Mythos Lexer
"""
import unittest
from compiler.lexer.lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    def test_numbers(self):
        """Test number tokenization"""
        lexer = Lexer("42 3.14 -10")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 42)
        
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, 3.14)
    
    def test_strings(self):
        """Test string tokenization"""
        lexer = Lexer('"hello" \'world\'')
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello")
        
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].value, "world")
    
    def test_identifiers(self):
        """Test identifier tokenization"""
        lexer = Lexer("x variable_name _private")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "x")
        
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "variable_name")
    
    def test_keywords(self):
        """Test keyword tokenization"""
        lexer = Lexer("if else while for function")
        tokens = lexer.tokenize()
        
        for token in tokens[:-1]:  # Exclude EOF
            self.assertEqual(token.type, TokenType.KEYWORD)
    
    def test_operators(self):
        """Test operator tokenization"""
        lexer = Lexer("+ - * / ^ %")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.MINUS)
        self.assertEqual(tokens[2].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[3].type, TokenType.DIVIDE)
        self.assertEqual(tokens[4].type, TokenType.POWER)
        self.assertEqual(tokens[5].type, TokenType.MODULO)
    
    def test_comparison(self):
        """Test comparison operators"""
        lexer = Lexer("== != < > <= >=")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.EQUAL)
        self.assertEqual(tokens[1].type, TokenType.NOT_EQUAL)
        self.assertEqual(tokens[2].type, TokenType.LESS_THAN)
        self.assertEqual(tokens[3].type, TokenType.GREATER_THAN)
        self.assertEqual(tokens[4].type, TokenType.LESS_EQUAL)
        self.assertEqual(tokens[5].type, TokenType.GREATER_EQUAL)
    
    def test_comments(self):
        """Test comment handling"""
        lexer = Lexer("x = 10 # This is a comment\ny = 20")
        tokens = lexer.tokenize()
        
        # Comments should be skipped
        identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(identifiers), 2)
        self.assertEqual(identifiers[0].value, "x")
        self.assertEqual(identifiers[1].value, "y")
    
    def test_complex_expression(self):
        """Test complex expression"""
        lexer = Lexer("result = (x + y) * 2 ^ 3")
        tokens = lexer.tokenize()
        
        # Should have: IDENTIFIER, ASSIGN, LPAREN, IDENTIFIER, PLUS, IDENTIFIER, RPAREN, MULTIPLY, NUMBER, POWER, NUMBER, EOF
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.ASSIGN)
        self.assertEqual(tokens[2].type, TokenType.LPAREN)

if __name__ == '__main__':
    unittest.main()

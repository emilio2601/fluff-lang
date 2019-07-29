from .token import Token, TokenType, sync_tts, variable_tts, binary_ops
from .expr import *
from .stmt import *
from typing import List

tt = TokenType

class Parser:
    def __init__(self, fluff_instance, tokens: List[Token]):
        self.tokens  = tokens
        self.fluff_instance = fluff_instance
        self.current = 0
    
    def parse(self) -> List[Stmt]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
    
    def declaration(self):
        try:
            if self.match(variable_tts):
                return self.varDeclaration()
            else:
                return self.statement()
        except Exception:
            self.synchronize()

    def varDeclaration(self):
        var_type = self.previous()
        name = self.consume(tt.IDENTIFIER, "Expected variable name")
        initializer = None

        if self.match([tt.EQUAL]):
            initializer = self.expression()
        
        return VarStmt(name, var_type, initializer)
    

    def statement(self):
        if self.match([tt.LEFT_BRACE]):
            return BlockStmt(self.block())
        
        elif self.match([tt.IF]):
            return self.ifStatement()
        
        elif self.match([tt.WHILE]):
            return self.whileStatement()
        
        elif self.match([tt.FOR]):
            return self.forStatement()

        return self.expressionStatement()
    
    def expressionStatement(self):
        expr = self.expression()
        return ExpressionStmt(expr)
    
    def forStatement(self):
        expr = self.expression();
        self.consume(tt.COLON, "Expected ':' after for expression."); 
        body = self.statement();

        return ForStmt(expr, body)
    
    def whileStatement(self):
        condition = self.expression();
        self.consume(tt.COLON, "Expected ':' after while condition."); 
        body = self.statement();

        return WhileStmt(condition, body)
    
    def ifStatement(self):
        condition = self.expression();
        self.consume(tt.COLON, "Expect ':' after if condition."); 
        thenBranch = self.statement();

        elseBranch = None
        if self.match([tt.ELSE]):
            elseBranch = self.statement() 
        
        return IfStmt(condition, thenBranch, elseBranch)


    def block(self):
        statements = []
       
        while not self.check(tt.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(tt.RIGHT_BRACE, "Expected '}' after block")

        return statements

    def match(self, token_types: List[TokenType]) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def check(self, token_type: TokenType) -> bool:
        if self.isAtEnd():
            return False
        else:
            return self.peek().type == token_type
        
    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().type == tt.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.update_in_place()

        if self.match([tt.EQUAL]):
            equals = self.previous()
            value  = self.assignment()

            if type(expr) == VarExpr:
                name = expr.name
                return AssignExpr(name, value)
            else:
                self.error(equals, "Invalid assignment target")
        
        elif self.match([tt.ASSIGN]):
            equals = self.previous()
            value  = self.assignment()

            if type(expr) == VarExpr:
                name = expr.name
                return AssignExpr(name, value, assign=True)
            else:
                self.error(equals, "Invalid assignment target")
        
        return expr
    
    def update_in_place(self) -> Expr:
        expr = self.or_branch()

        if self.match([tt.MINUS_EQUAL, tt.PLUS_EQUAL, tt.SLASH_EQUAL, tt.STAR_EQUAL, tt.PERCENT_EQUAL]):
            equals = self.previous()
            value  = self.assignment()

            if type(expr) == VarExpr:
                name = expr.name
                return AssignUpdateExpr(name, value, equals)
            else:
                self.error(equals, "Invalid assignment target")

        return expr
    
    def or_branch(self):
        expr = self.and_branch()

        while self.match([tt.OR]):
            operator = self.previous()
            right    = self.and_branch()
            expr     = LogicalExpr(expr, operator, right)
        
        return expr
    
    def and_branch(self):
        expr = self.equality()

        while self.match([tt.AND]):
            operator = self.previous()
            right    = self.equality()
            expr     = LogicalExpr(expr, operator, right)
        
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([tt.NOT_EQUAL, tt.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr:
        expr = self.addition()

        while self.match([tt.GREATER, tt.GREATER_EQUAL, tt.LESS, tt.LESS_EQUAL]):
            operator = self.previous()
            right = self.addition()
            expr = BinaryExpr(expr, operator, right)

        return expr
    
    def addition(self) -> Expr:
        expr = self.multiplication()

        while self.match([tt.MINUS, tt.PLUS]):
            operator = self.previous()
            right = self.multiplication()
            expr = BinaryExpr(expr, operator, right)

        return expr
    
    def multiplication(self) -> Expr:
        expr = self.unary()

        while self.match([tt.SLASH, tt.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)

        return expr
    
    def unary(self):
        if self.match([tt.NOT, tt.MINUS]):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)
        
        return self.call()
    
    def call(self):
        expr = self.primary()

        while True:
            if self.match([tt.LEFT_PAREN]):
                expr = self.finishCall(expr)
            else:
                break

        return expr
    
    def finishCall(self, callee: Expr):
        arguments = []

        if not self.check(tt.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Cannot have more than 255 arguments")
                arguments.append(self.expression())
                if not self.match([tt.COMMA]):
                    break
        
        paren = self.consume(tt.RIGHT_PAREN, "Expected ')' after arguments")

        return FunctionExpr(callee, paren, arguments)
             
    
    def primary(self):
        if self.match([tt.FALSE]):
            return LiteralExpr(False)
        elif self.match([tt.TRUE]):
            return LiteralExpr(True)
        elif self.match([tt.NIL]):
            return LiteralExpr(None)
        elif self.match([tt.NUMBER, tt.STRING]):
            return LiteralExpr(self.previous().literal)
        elif self.match([tt.IDENTIFIER]):
            return VarExpr(self.previous())
        elif self.match([tt.LEFT_PAREN]):
            expr = self.expression()
            self.consume(tt.RIGHT_PAREN, "Expected ')' after expression")
            return GroupingExpr(expr)
        
        elif self.match(binary_ops):
            self.advance()
            raise self.error(self.tokens[self.current - 2], "Expected left-hand operand")
        
        else:
            raise self.error(self.peek(), "Expected expression")
        
    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        else:
            raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str):
        self.fluff_instance.error_t(token, message)
        return Exception()

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            t = self.peek().type

            if t in sync_tts:
                return
            
            self.advance()
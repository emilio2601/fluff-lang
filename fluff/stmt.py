from abc import ABC, abstractmethod
from .expr import Expr
from .token import Token
from typing import List

class Stmt(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def accept(self):
        pass


class ExpressionStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)
    
    def __str__(self):
        return f"{self.expr}"

class VarStmt(Stmt):
    def __init__(self, name: Token, var_type, initializer: Expr):
        self.name = name
        self.initializer = initializer

        if type(var_type) == Token:
            self.var_type = var_type.type
        else:
            self.var_type = "dynamic"
    
    def accept(self, visitor):
        return visitor.visitVarStmt(self)
    
    def __str__(self):
        return f"{self.var_type} {self.name.lexeme} = {self.initializer}"

class BlockStmt(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visitBlockStmt(self)
    
    def __str__(self):
        return f"{self.statements}"

class IfStmt(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
        self.condition  = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    
    def accept(self, visitor):
        return visitor.visitIfStmt(self)
    
    def __str__(self):
        return f"{self.expr}"

class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body      = body
    
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)

class ForStmt(Stmt):
    def __init__(self, expr: Expr, body: Stmt):
        self.expr = expr
        self.body = body
    
    def accept(self, visitor):
        return visitor.visitForStmt(self)

class VisitorStmt(ABC):
    @abstractmethod
    def visitExpressionStmt(self, expr: ExpressionStmt):
        pass
    
    @abstractmethod
    def visitVarStmt(self, expr: VarStmt):
        pass
    
    @abstractmethod
    def visitBlockStmt(self, expr: BlockStmt):
        pass
    
    @abstractmethod
    def visitIfStmt(self, expr: IfStmt):
        pass
    
    @abstractmethod
    def visitWhileStmt(self, expr: WhileStmt):
        pass
    
    @abstractmethod
    def visitForStmt(self, expr: ForStmt):
        pass
    
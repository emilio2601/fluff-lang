from .token import Token
from abc import ABC, abstractmethod
from typing import List


class Expr(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def accept(self):
        pass
    
class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left     = left
        self.operator = operator
        self.right    = right
    
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class GroupingExpr(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

class LiteralExpr(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
    
    def __str__(self):
        return f"{self.value}"

class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right    = right
    
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

class VarExpr(Expr):
    def __init__(self, name: Token):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visitVarExpr(self)
    
    def __str__(self):
        return f"{self.name}"

class AssignExpr(Expr):
    def __init__(self, name: Token, value: Expr, assign=False):
        self.name = name
        self.value = value
        self.assign = assign
    
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)
    
    def __str__(self):
        return f"{self.name} = {self.value}"

class AssignUpdateExpr(Expr):
    def __init__(self, name: Token, value: Expr, operator: Token):
        self.name = name
        self.value = value
        self.operator = operator

    def accept(self, visitor):
        return visitor.visitAssignUpdateExpr(self)
    
    def __str__(self):
        return f"{self.name} = {self.value}"

class LogicalExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left     = left
        self.operator = operator
        self.right    = right
    
    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)

class FunctionExpr(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee    = callee
        self.paren     = paren
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visitFunctionExpr(self)

    
class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: BinaryExpr):
        pass
    
    @abstractmethod
    def visitGroupingExpr(self, expr: GroupingExpr):
        pass
    
    @abstractmethod
    def visitLiteralExpr(self, expr: LiteralExpr):
        pass
    
    @abstractmethod
    def visitUnaryExpr(self, expr: UnaryExpr):
        pass

    @abstractmethod
    def visitVarExpr(self, expr: VarExpr):
        pass
    
    @abstractmethod
    def visitAssignExpr(self, expr: AssignExpr):
        pass
    
    @abstractmethod
    def visitAssignUpdateExpr(self, expr: AssignUpdateExpr):
        pass
    
    @abstractmethod
    def visitLogicalExpr(self, expr: AssignExpr):
        pass
    
    @abstractmethod
    def visitFunctionExpr(self, expr: FunctionExpr):
        pass
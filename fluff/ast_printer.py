from .expr import *
from .token import Token, TokenType as tt
from typing import List

class AstPrinter(Visitor):
    def __init__(self):
        pass
    
    def print(self, expr: Expr):
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr: BinaryExpr):
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visitGroupingExpr(self, expr: GroupingExpr):
        return self.parenthesize('group', [expr.expression])
    
    def visitLiteralExpr(self, expr: LiteralExpr):
        if expr.value == None:
            return 'nil'
        else:
            return str(expr.value)

    def visitUnaryExpr(self, expr: UnaryExpr):
        return self.parenthesize(expr.operator.lexeme, [expr.right])
    
    def parenthesize(self, name: str, exprs: List[Expr]):
        subexprs = " ".join(expr.accept(self) for expr in exprs)
        return f"({name} {subexprs})"
    
    def ___test(self):
        expr = BinaryExpr(
            UnaryExpr(
                Token(tt.MINUS, "-", None, 1), 
                LiteralExpr(123)
            ), 
            Token(tt.STAR, "*", None, 1), 
            GroupingExpr(LiteralExpr(45.67))
            )
        print(self.print(expr))

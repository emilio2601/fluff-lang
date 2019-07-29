from .expr import *
from .stmt import *
from .token import TokenType as tt
from decimal import Decimal
from typing import List
from .environment import Environment
from .runtime_error import RuntimeError
from .fluff_callable import FluffCallable, Clock, Print

class Interpreter(Visitor, VisitorStmt):
    def __init__(self, fluff_instance):
        self.fluff_instance = fluff_instance
        self.environment = Environment()
        self.environment.define("clock", Clock())
        self.environment.define("print", Print())

    def interpret(self, statements: List[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as e:
            self.fluff_instance.runtimeError(e)
    
    def execute(self, stmt: Stmt):
        stmt.accept(self)
    
    def booleanify(self, val: bool):
        return val

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitLiteralExpr(self, expr: LiteralExpr):
        return expr.value
    
    def visitGroupingExpr(self, expr: GroupingExpr):
        return self.evaluate(expr.expression)
    
    def visitUnaryExpr(self, expr: UnaryExpr):
        right = self.evaluate(expr.right)

        if expr.operator.type == tt.MINUS:
            return -right
        elif expr.operator.type == tt.NOT:
            return self.booleanify(not right)
    
    def visitBinaryExpr(self, expr: BinaryExpr):
        left  = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == tt.MINUS:
            return left - right
        elif expr.operator.type == tt.SLASH:
            return left / right
        elif expr.operator.type == tt.STAR:
            return left * right
        elif expr.operator.type == tt.PLUS:
            if type(left) == Decimal and type(right) == Decimal:
                return left + right
            elif type(left) == str and type(right) == Decimal:
                return left + right
        elif expr.operator.type == tt.GREATER_EQUAL:
            return self.booleanify(left > right)
        elif expr.operator.type == tt.GREATER:
            return self.booleanify(left >= right)
        elif expr.operator.type == tt.LESS_EQUAL:
            return self.booleanify(left <= right)
        elif expr.operator.type == tt.LESS:
            return self.booleanify(left < right)
        elif expr.operator.type == tt.NOT_EQUAL:
            return self.booleanify(left != right)
        elif expr.operator.type == tt.EQUAL_EQUAL:
            return self.booleanify(left == right)
        
    def visitExpressionStmt(self, stmt: ExpressionStmt):
        self.evaluate(stmt.expr)
    
    def visitVarStmt(self, stmt: VarStmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt, value)

    def visitVarExpr(self, expr: VarExpr):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr: AssignExpr):
        value = self.evaluate(expr.value)
        if expr.assign:
            self.environment.assign(expr.name, value)
        else:
            self.environment.update(expr.name, value)
        return value
    
    def visitAssignUpdateExpr(self, expr: AssignExpr):
        value = self.evaluate(expr.value)
        self.environment.update_in_place(expr.name, expr.operator, value)
        return value
    
    def visitBlockStmt(self, stmt: BlockStmt):
        self.executeBlock(stmt.statements, Environment(enclosing=self.environment))
    
    def executeBlock(self, statements: List[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitIfStmt(self, stmt: IfStmt):
        ev = self.evaluate(stmt.condition)
        if ev == 'true' or ev and ev != 'false':
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)

    
    def visitLogicalExpr(self, expr: LogicalExpr):
        left = self.evaluate(expr.left)

        if expr.operator.type == tt.OR:
            if left:
                return left
        else:
            if not left:
                return left
        
        return self.evaluate(expr.right)
    
    def visitWhileStmt(self, stmt: WhileStmt):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)
    
    def visitForStmt(self, stmt: ForStmt): #TODO: implement actual for's
        while self.evaluate(stmt.expr):
            self.execute(stmt.body)
    
    def visitFunctionExpr(self, expr: FunctionExpr):
        callee = self.evaluate(expr.callee)

        arguments = []

        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        
        if not isinstance(callee, FluffCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes")
        
        if len(arguments) != callee.arity():
            raise RuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}")
        
        return callee.call(self, arguments)
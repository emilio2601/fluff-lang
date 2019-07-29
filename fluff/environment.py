from .token import Token, numeric_types, TokenType
from .stmt import *
from .runtime_error import RuntimeError
from .fluff_callable import FluffCallable
from decimal import Decimal

tt = TokenType

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values    = dict()
        self.og_types  = dict()

    def define(self, name, value):
        if isinstance(value, FluffCallable):
            self.values[name]   = value
            self.og_types[name] = tt.FN
        elif name.var_type in numeric_types:
            if type(value) == Decimal:
                self.values[name.name.lexeme]   = value
                self.og_types[name.name.lexeme] = self.getTokenType(value)
            elif value is None:
                self.values[name.name.lexeme]   = None
                self.og_types[name.name.lexeme] = self.getTokenType(Decimal(0))
            else:
                raise RuntimeError(name.name, f"Type error: expected numeric, had {self.getFluffNameFromPython(value)}")
        elif name.var_type == tt.STR:
            if type(value) == str:
                self.values[name.name.lexeme]   = value
                self.og_types[name.name.lexeme] = self.getTokenType(value)
            elif value is None:
                self.values[name.name.lexeme]   = None
                self.og_types[name.name.lexeme] = self.getTokenType("")
            else:
                raise RuntimeError(name.name, f"Type error: expected str, had {self.getFluffNameFromPython(value)}")
        elif name.var_type == tt.BOOL:
            if type(value) == bool:
                self.values[name.name.lexeme]   = value
                self.og_types[name.name.lexeme] = self.getTokenType(value)
            elif value is None:
                self.values[name.name.lexeme]   = None
                self.og_types[name.name.lexeme] = self.getTokenType(False)
            else:
                raise RuntimeError(name.name, f"Type error: expected bool, had {self.getFluffNameFromPython(value)}")
                

    def getFluffNameFromPython(self, var):
        name = type(var).__name__

        if name in ["bool", "str"]:
            return name
        if name == "Decimal":
            return "double"
    
    def getFluffNameFromToken(self, token_type):
        if token_type == tt.BOOL:
            return 'bool'
        if token_type == tt.STR:
            return 'str'
        if token_type == tt.DOUBLE:
            return 'double'
    
    def getTokenType(self, var):
        name = type(var).__name__

        if name == "bool":
            return tt.BOOL
        if name == "str":
            return tt.STR
        if name == "Decimal":
            return tt.DOUBLE
    
    def assign(self, name: Token, value):
        if name.lexeme not in self.values.keys():
            self.og_types[name.lexeme] = self.getTokenType(value)
            self.values[name.lexeme] = value
        elif self.enclosing != None:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(name, f"Declaring existing variable '{name.lexeme}'")
    
    def update_in_place(self, name: Token, operator: Token, value):
        if name.lexeme not in self.values.keys() and self.enclosing and self.enclosing.exists(name.lexeme):
            if self.enclosing.recursive_og_type(name.lexeme) == self.getTokenType(value):
                self.enclosing.update_in_place(name, operator, value)
            else:
                raise RuntimeError(name, f"Assigning '{self.getFluffNameFromPython(value)}' to variable with type '{self.getFluffNameFromToken(self.enclosing.recursive_og_type(name.lexeme))}'")
        elif name.lexeme in self.values.keys():
            if self.og_types[name.lexeme] == self.getTokenType(value):
                if operator.type == tt.PLUS_EQUAL:
                    self.values[name.lexeme] += value
                elif operator.type == tt.MINUS_EQUAL:
                    self.values[name.lexeme] -= value
                elif operator.type == tt.STAR_EQUAL:
                    self.values[name.lexeme] *= value
                elif operator.type == tt.SLASH_EQUAL:
                    self.values[name.lexeme] /= value
                elif operator.type == tt.PERCENT_EQUAL:
                    self.values[name.lexeme] %= value
                else:
                    raise RuntimeError(name, f"Operator type not recognized")
            else:
                raise RuntimeError(name, f"Assigning '{self.getFluffNameFromPython(value)}' to variable with type '{self.getFluffNameFromToken(self.og_types[name.lexeme])}'")         
        else:
            raise RuntimeError(name, f"Assigning to undefined variable '{name.lexeme}'")
    
    def exists(self, var_name):
        if var_name in self.values.keys():
            return True
        elif self.enclosing:
            return self.enclosing.exists(var_name)
        else:
            return False
    
    def recursive_og_type(self, var_name):
        if var_name in self.og_types.keys():
            return self.og_types[var_name]
        elif self.enclosing:
            return self.enclosing.recursive_og_type(var_name)
        else:
            return False

    
    def update(self, name: Token, value):
        if name.lexeme not in self.values.keys() and self.enclosing and self.enclosing.exists(name.lexeme):
            if self.enclosing.recursive_og_type(name.lexeme) == self.getTokenType(value):
                self.enclosing.update(name, value)
            else:
                raise RuntimeError(name, f"Assigning '{self.getFluffNameFromPython(value)}' to variable with type '{self.getFluffNameFromToken(self.enclosing.recursive_og_type(name.lexeme))}'")
        elif name.lexeme in self.values.keys():
            if self.og_types[name.lexeme] == self.getTokenType(value):
                self.values[name.lexeme] = value
            else:
                raise RuntimeError(name, f"Assigning '{self.getFluffNameFromPython(value)}' to variable with type '{self.getFluffNameFromToken(self.og_types[name.lexeme])}'")         
        else:
            raise RuntimeError(name, f"Assigning to undefined variable '{name.lexeme}'")

    def get(self, name: Token):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        elif self.enclosing != None:
            return self.enclosing.get(name)
        else:
            raise RuntimeError(name, f"Undefined variable '{name.lexeme}'")
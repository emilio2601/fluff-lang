from enum import Enum, auto

class TokenType(Enum):
  #Single-character tokens.                      
  LEFT_PAREN       = auto() 
  RIGHT_PAREN      = auto() 
  LEFT_BRACE       = auto() 
  RIGHT_BRACE      = auto()
  LEFT_SQ_BRACKET  = auto()
  RIGHT_SQ_BRACKET = auto() 
  COMMA            = auto() 
  DOT              = auto()
  SEMICOLON        = auto()
  COLON            = auto() 
  MINUS            = auto() 
  PLUS             = auto() 
  PERCENT          = auto()
  SLASH            = auto() 
  STAR             = auto() 

  #One or two character tokens.
  MINUS_EQUAL    = auto()
  PLUS_EQUAL     = auto()
  PERCENT_EQUAL  = auto()
  SLASH_EQUAL    = auto()
  STAR_EQUAL     = auto()
  ASSIGN         = auto()                                                
  EQUAL          = auto()
  NOT_EQUAL      = auto()
  EQUAL_EQUAL    = auto()                              
  GREATER        = auto()
  GREATER_EQUAL  = auto()                        
  LESS           = auto() 
  LESS_EQUAL     = auto()                               

  #Literals.                                     
  IDENTIFIER = auto() 
  STRING     = auto() 
  NUMBER     = auto()                    

  #Keywords.                                     
  AND       = auto()
  BREAK     = auto()  
  CLASS     = auto()
  CONTINUE  = auto()  
  ELSE      = auto() 
  FALSE     = auto() 
  FN        = auto()
  FOR       = auto() 
  IF        = auto()
  NIL       = auto()
  NOT       = auto()
  OR        = auto()  
  RETURN    = auto()
  SELF      = auto() 
  SUPER     = auto() 
  TRUE      = auto() 
  WHILE     = auto()
  XOR       = auto()

  #Types
  INT    = auto() 
  INT8   = auto()
  INT16  = auto() 
  INT32  = auto() 
  INT64  = auto() 
  UINT8  = auto() 
  UINT16 = auto() 
  UINT32 = auto() 
  UINT64 = auto() 
  FLOAT  = auto() 
  DOUBLE = auto() 
  BYTE   = auto() 
  BOOL   = auto() 
  DICT   = auto()
  STR    = auto()  

  EOF  = auto() 

variable_tts  = [TokenType(i) for i in range(50, 65)]
numeric_types = [TokenType(i) for i in range(50, 61)]
sync_tts      = [TokenType(i) for i in range(32, 65)]
binary_ops    = [TokenType(i) for i in range(11, 29)]

tt_to_str = {
  "and": TokenType.AND,
  "break": TokenType.BREAK,
  "class": TokenType.CLASS,
  "continue": TokenType.CONTINUE,
  "else": TokenType.ELSE,
  "false": TokenType.FALSE,
  "fn": TokenType.FN,
  "for": TokenType.FOR,
  "if": TokenType.IF,
  "nil": TokenType.NIL,
  "not": TokenType.NOT,
  "or": TokenType.OR,
  "return": TokenType.RETURN,
  "self": TokenType.SELF,
  "super": TokenType.SUPER,
  "true": TokenType.TRUE,
  "while": TokenType.WHILE,
  "xor": TokenType.XOR,
  "int": TokenType.INT,
  "int8": TokenType.INT8,
  "int16": TokenType.INT16,
  "int32": TokenType.INT32,
  "int64": TokenType.INT64,
  "uint8": TokenType.UINT8,
  "uint16": TokenType.UINT16,
  "uint32": TokenType.UINT32,
  "uint64": TokenType.UINT64,
  "float": TokenType.FLOAT,
  "double": TokenType.DOUBLE,
  "byte": TokenType.BYTE,
  "bool": TokenType.BOOL,
  "dict": TokenType.DICT,
  "str": TokenType.STR
}


class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
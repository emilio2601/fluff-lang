from .token import Token, tt_to_str
from .token import TokenType as tt
from decimal import Decimal

class Scanner:
    def __init__(self, file_bytes: bytes, fluff_instance):
        self.file_str = file_bytes.decode('utf-8')
        self.fluff_instance = fluff_instance
        self.tokens = []
    
    def isAtEnd(self):
        return self.current >= len(self.file_str)

    def advance(self):
        self.current += 1
        return self.file_str[self.current - 1]

    def scanToken(self):
        c = self.advance()

        if c == '(':
            self.addToken(tt.LEFT_PAREN)
        elif c == ')':
            self.addToken(tt.RIGHT_PAREN)
        elif c == '{':
            self.addToken(tt.LEFT_BRACE)
        elif c == '}':
            self.addToken(tt.RIGHT_BRACE)
        elif c == '[':
            self.addToken(tt.LEFT_SQ_BRACKET)
        elif c == ']':
            self.addToken(tt.RIGHT_SQ_BRACKET)
        elif c == ',':
            self.addToken(tt.COMMA)
        elif c == '.':
            self.addToken(tt.DOT)
        elif c == '-':
            self.addToken(tt.MINUS_EQUAL if self.match('=') else tt.MINUS)
        elif c == '+':
            self.addToken(tt.PLUS_EQUAL if self.match('=') else tt.PLUS)
        elif c == '%':
            self.addToken(tt.PERCENT_EQUAL if self.match('=') else tt.PERCENT)
        elif c == ';':
            self.addToken(tt.SEMICOLON)
        elif c == '*':
            self.addToken(tt.STAR_EQUAL if self.match('=') else tt.STAR)
        elif c == '=':
            self.addToken(tt.EQUAL_EQUAL if self.match('=') else tt.EQUAL)
        elif c == '<':
            self.addToken(tt.LESS_EQUAL if self.match('=') else tt.LESS)
        elif c == '>':
            self.addToken(tt.GREATER_EQUAL if self.match('=') else tt.GREATER)
        elif c == ':':
            self.addToken(tt.ASSIGN if self.match('=') else tt.COLON)
        elif c == '!':
            self.addToken(tt.NOT_EQUAL if self.match('=') else self.fluff_instance.error(self.line, 'Unexpected character'))
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(tt.SLASH_EQUAL if self.match('=') else tt.SLASH)
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self.line += 1
        elif c in ["'", '"']:
            self.string(c)
        else:
            if c.isdigit():
                self.number()
            elif c.isidentifier():
                self.identifier()
            else:
                self.fluff_instance.error(self.line, 'Unexpected character')
    
    def identifier(self):
        while self.peek().isidentifier() or self.peek().isdigit():
            self.advance()
        
        try:
            token_type = tt_to_str[self.file_str[self.start:self.current]]
        except KeyError:
            token_type = tt.IDENTIFIER

        self.addToken(token_type)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        
        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance()
            
            while self.peek().isdigit():
                self.advance()
        
        self.addTokenObj(tt.NUMBER, Decimal(self.file_str[self.start:self.current]))
    
    def peekNext(self):
        if self.current + 1 >= len(self.file_str):
            return '\0'
        else:
            return self.file_str[self.current+1]

    def string(self, string_char):
        while self.peek() != string_char and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.isAtEnd():
            self.fluff_instance.error(self.line, 'Unterminated string')
            return
        
        self.advance()
        self.addTokenObj(tt.STRING, self.file_str[self.start+1:self.current-1].encode('utf-8').decode('unicode_escape'))
        
    def match(self, expected):
        if not self.isAtEnd() and self.file_str[self.current] == expected:
            self.current += 1
            return True
        else:
            return False

    def peek(self):
        if self.isAtEnd():
            return '\0'
        else:
            return self.file_str[self.current]

    def addToken(self, tokenType):
        self.addTokenObj(tokenType, None)
    
    def addTokenObj(self, tokenType, literal):
        text = self.file_str[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def scanTokens(self):
        self.start   = 0
        self.current = 0
        self.line    = 1

        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(tt.EOF, "", None, self.line))

        return self.tokens

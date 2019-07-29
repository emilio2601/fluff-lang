import argparse
import fluff
from fluff import TokenType as tt


class FluffInterpreter:
    def run_file(self, file_bytes: bytes):
        self.hadError = False
        self.hadRuntimeError = False
        scanner     = fluff.Scanner(file_bytes, self)
        tokens      = scanner.scanTokens()
        parser      = fluff.Parser(self, tokens)
        statements  = parser.parse()
        interpreter = fluff.Interpreter(self)

        if self.hadError:
            return
        else:
            #print([str(statement) for statement in tokens])
            interpreter.interpret(statements)
            #print(interpreter.environment.values)
    
    def error(self, line, message):
        self.report(line, "", message)
    
    def runtimeError(self, error: fluff.runtime_error.RuntimeError):
        self.hadRuntimeError = True
        print(f"[line {error.token.line}]: {error.message}")
    
    def error_t(self, token: fluff.Token, message: str):
        if token.type == tt.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f"at '{token.lexeme}'", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error {where}: {message}")
        self.hadError = True



parser = argparse.ArgumentParser(description='Interpreter for the Fluff programming language')
parser.add_argument('file', help='File to execute', type=argparse.FileType('rb'))
args = parser.parse_args()

fluff_i = FluffInterpreter()

fluff_i.run_file(args.file.read())


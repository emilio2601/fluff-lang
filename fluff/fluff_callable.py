from abc import ABC, abstractmethod
import time
from decimal import Decimal

class FluffCallable(ABC):
    @abstractmethod
    def call(self, intepreter, arguments):
        pass
    
    @abstractmethod
    def arity(self):
        pass

class Clock(FluffCallable):
    def call(self, interpreter, arguments):
        return Decimal(time.monotonic())
    
    def arity(self):
        return 0

class Print(FluffCallable):
    def call(self, interpreter, arguments):
        print(arguments[0])
    
    def arity(self):
        return 1
from functools import wraps
from typing import Callable
from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log"),
        logging.StreamHandler()         
    ]
) 


class Comission(ABC):
    @abstractmethod
    def calculate(self):
        '''в наследниках этот метод должен считать комиссию'''
        pass

     

class StandardComission(Comission):       
    def calculate(self, amount: int) -> float:
        res = amount * 0.01
        return res
    

class NoComission(Comission):

    def calculate(self,amount: int) -> int:
        return 0





class TransactionLimit:
    def __init__(self, max_limit: int):
        self.calls_data = {}
        self.max_limit = max_limit


    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            card = args[0]
            card_id = card.id

            current_calls = self.calls_data.get(card_id, 0)

            if  current_calls < self.max_limit:
                self.calls_data[card_id] = current_calls + 1
                return func(*args, **kwargs)
            
            else:
                raise PermissionError(f'Лимит бесплантных вызовов для карты {card.id} исчерап!')
        return wrapper
    

def require_auth(func:Callable):
    raise NotImplementedError



def trace_transaction(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Система банка запущена")
        res = func(*args, **kwargs)
        return res
    return wrapper




class BankError(Exception):
    """исключение для банка(дальше будут наследоваться другие от него)"""
    pass

class InsufficientFundsError(BankError):
    '''недостаточно средств'''
    def __init__(self,balance, amount):
        self.balance = balance
        self.amount = amount

        super().__init__(f'Недостаточно средств: баланс {self.balance}, нужно {self.amount}')


class InvalidPinError(BankError):
    '''неверный пин код'''
    def __init__(self):
        super().__init__(f'Неверный пин')


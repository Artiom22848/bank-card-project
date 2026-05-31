from functools import wraps
from typing import Callable
import logging
from enum import Enum

class Commission(Enum):
    STANDARD = 0
    FREE = 1

    def calculate(self, amount: int) -> int:
        match self:
            case Commission.STANDARD:
                return round(amount * 0.01)
            case Commission.FREE:
                return 0

class TransactionLimit:
    def __init__(self, max_limit: int):
        self.calls_data = {}
        self.max_limit = max_limit


    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            card = args[0]
            card_id = card.card_id

            current_calls = self.calls_data.get(card_id, 0)

            if  current_calls < self.max_limit:
                self.calls_data[card_id] = current_calls + 1
                return func(*args, **kwargs)

            else:
                raise PermissionError(f'Лимит бесплатных вызовов для карты {card.id} исчерпан!')
        return wrapper


def trace_transaction(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Система банка запущена")
        res = func(*args, **kwargs)
        return res
    return wrapper

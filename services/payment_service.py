import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from dop_work.utils import *

from models.cards import BankCard


class PaymentSystem:
    _instance = None
    _total_volume = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def transfer(self, from_card: BankCard, to_card: BankCard, amount: int, pin: str):
        if  not from_card.check_pin(pin):
            raise InvalidPinError
        try:
            from_card.withdraw(amount, pin)

            try:
                to_card.deposit(amount)
            except Exception as e:
                from_card.deposit(amount)
                raise RuntimeError(f'Ошибка зачисления: {e}: Деньги вовзращены')
            else:
                self._total_volume += amount
                print(f'Перевод успешно сделан')
        except ValueError as e:
            print(f'Перевод невозможен: {e}')
        
    
    @classmethod
    def get_stats(cls):
        print(f'Через систему прошло всего: {cls._total_volume}')

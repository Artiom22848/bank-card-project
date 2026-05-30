import os
import sys

from dop_work.utils import *
from models.cards import BankCard
from models.transaction import Transfer, TransferType

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

class PaymentSystem:
    _instance = None
    _total_volume = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def transfer(self, from_card: BankCard, pin: str, to_card: BankCard, amount: int) -> None:
        BankCard.validate_amount(amount)
        if from_card.id == to_card.id:
            raise PermissionError('Нельзя перевести деньги на тот-же счёт')

        from_card.validate_pin(pin)
        from_card.validate_for_transactions()
        to_card.validate_for_transactions()
        '''todo проверить на дневные лимиты не шарю как это делать'''

        if from_card.balance < amount:
            raise PermissionError('Недостаточно средств на балансе')

        from_card.balance -= amount
        to_card.balance += amount
        self._total_volume += amount
        from_card.transaction_history.append(Transfer(amount, to_card.id, TransferType.TO))
        to_card.transaction_history.append(Transfer(amount, from_card.id, TransferType.FROM))

    @classmethod
    def get_stats(cls):
        print(f'Через систему прошло всего: {cls._total_volume}')

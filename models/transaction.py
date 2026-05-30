from dataclasses import dataclass
import datetime
from enum import Enum
import logging

@dataclass(frozen=True)
class Deposit:
    amount: int

@dataclass(frozen=True)
class Withdraw:
    amount: int
    comission: int

class TransferType(Enum):
    TO = 0,
    FROM = 1,

@dataclass(frozen=True)
class Transfer:
    amount: int
    other_id: int
    transfer_type: TransferType

Transaction = Deposit | Withdraw | Transfer

def transaction_to_str(self: Transaction) -> str:
    match self:
        case Deposit(amount):
            return f'Депозит: {amount}'
        case Withdraw(amount, comission):
            return f'Снятие: {amount} с комиссией {comission}'
        case Transfer(amount, other_id, tt):
            match tt:
                case TransferType.TO:
                    return f'Перевод: {amount} на счёт {other_id}'
                case TransferType.FROM:
                    return f'Перевод: {amount} со счёта {other_id}'


'''
class Transaction:
    def __init__(self, trans_type: str, amount: int):
        self.trans_type = trans_type
        self.amount = amount
        logging.info(f'Записываю в историю транзакцию')
        self.trans_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        return f'Transaction(type ={self.trans_type}, amount ={self.amount}, time = {self.trans_time})'



    def __str__(self) -> str:
        return f'{self.trans_type} | Сумма: {self.amount}, Время и дата: {self.trans_time}'


    def __eq__(self, tran) -> bool:
        if not isinstance(tran,Transaction):
            raise ValueError(f'Данные введены неккоректно')
        return tran.type == self.trans_type and tran.amount == self.amount


    @property
    def sh_trans(self) -> str:
        return f'{self.trans_type} | Сумма: {self.amount}, Время и дата: {self.trans_time}'

    @property
    def is_expense(self) -> bool:
        if self.trans_type == 'Пополнение':
            return False
        return True

    @property
    def formatted_amount(self) -> str:
        if self.trans_type == 'Снятие':
            return f'-{self.amount} ₽'

        return f"+{self.amount} ₽"
'''

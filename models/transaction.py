from dataclasses import dataclass
from enum import Enum
from datetime import datetime

@dataclass(frozen=True)
class Deposit:
    amount: int
    time: datetime

@dataclass(frozen=True)
class Withdraw:
    amount: int
    comission: int
    time: datetime

class TransferType(Enum):
    TO = 0
    FROM = 1

@dataclass(frozen=True)
class Transfer:
    amount: int
    other_id: int
    transfer_type: TransferType
    time: datetime

Transaction = Deposit | Withdraw | Transfer

def transaction_to_str(transaction: Transaction) -> str:
    fmt = "%d.%m.%Y %H:%M"
    match transaction:
        case Deposit(amount, time):
            return f'Депозит: {amount} | Время: {time.strftime(fmt)}'
        case Withdraw(amount, comission, time):
            return f'Снятие: {amount} с комиссией {comission} | Время: {time.strftime(fmt)}'
        case Transfer(amount, other_id, tt, time):
            match tt:
                case TransferType.TO:
                    return f'Перевод: {amount} на счёт {other_id} | Время: {time.strftime(fmt)}'
                case TransferType.FROM:
                    return f'Перевод: {amount} со счёта {other_id} | Время: {time.strftime(fmt)}'

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

@dataclass(frozen=True)
class Deposit:
    amount: int

@dataclass(frozen=True)
class Withdraw:
    amount: int
    comission: int

class TransferType(Enum):
    TO = 0
    FROM = 1

@dataclass(frozen=True)
class Transfer:
    amount: int
    other_id: int
    transfer_type: TransferType

TransactionKind = Deposit | Withdraw | Transfer

class Transaction:
    kind: TransactionKind
    time: datetime

    def __init__(self, kind: TransactionKind) -> None:
        self.kind = kind
        self.time = datetime.now(timezone.utc)

def transaction_to_str(transaction: Transaction) -> str:
    time = transaction.time.strftime("%d.%m.%Y %H:%M")
    match transaction.kind:
        case Deposit(amount):
            return f'Депозит: {amount} | Время: {time}'
        case Withdraw(amount, comission):
            return f'Снятие: {amount} с комиссией {comission} | Время: {time}'
        case Transfer(amount, other_id, tt):
            match tt:
                case TransferType.TO:
                    return f'Перевод: {amount} на счёт {other_id} | Время: {time}'
                case TransferType.FROM:
                    return f'Перевод: {amount} со счёта {other_id} | Время: {time}'

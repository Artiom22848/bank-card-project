class BankError(Exception):
    """исключение для банка(дальше будут наследоваться другие от него)"""
    pass

class InsufficientFundsError(BankError):
    '''недостаточно средств'''
    def __init__(self,balance, amount) -> None:
        self.balance = balance
        self.amount = amount

        super().__init__(f'Недостаточно средств: баланс {self.balance}, нужно {self.amount}')

class InvalidPinError(BankError):
    '''неверный пин код'''
    def __init__(self) -> None:
        super().__init__('Неверный пин')

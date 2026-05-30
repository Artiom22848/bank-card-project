import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from dop_work.observers import *
from dop_work.utils import *
from dop_work.logi import *
from models.transaction import *
import json
from uuid import uuid4
import logging

class BankCard:
    id: int
    daily_limit: int
    is_frozen: bool
    owner_id: int
    balance: int
    pin: str
    transaction_history: list[Transaction]
    observers: list[CardObserver]
    comission: Commission

    def __init__(self, id: int, owner_id: int, balance: int, pin: str, comission: Commission) -> None:
        if not BankCard.validate_amount(balance):
            raise ValueError('Неправильный начальный баланс')

        self.id = id
        self.daily_limit = 50000
        self.is_frozen = False
        self.owner_id = owner_id
        self.balance = balance
        self.pin = pin
        self.transaction_history = []
        self.observers = [LogNotification()]
        self.comission = comission

    def __str__(self) -> str:
        return f'ID: {self.__id} {type(self).__name__} Владелец: {self.owner}, Баланс: {self.balance}'

    def __repr__(self):
        return f'BankCard(id = {self.id}, owner = {self.owner}, balance = {self.balance}, comission: {type(self.comission).__name__})'

    def __gt__(self, other) -> bool:
        if  not isinstance(other, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        other_balance = other.balance if isinstance(other, BankCard) else other
        return self.balance > other_balance

    def __lt__(self, other)-> bool:
        if  not isinstance(other, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        other_balance = other.balance if isinstance(other, BankCard) else other
        return self.balance < other_balance

    def __eq__(self, value) -> bool:
        if  not isinstance(value, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        elif isinstance(value, BankCard):
            return value.balance == self.balance
        else:
            return self.balance == value

    def __add__(self, other):
        if  not isinstance(other, BankCard):
            raise TypeError('данные введены некоректно')
        else:
            summ_balance = self.balance + other.balance
            return type(self)(self.owner, summ_balance, self.my_pin, self.comission)

    def __len__(self) -> int:
        return len(self.transaction_history)

    def get_info_bonus(self) -> str:
        return("бонусов нету")

    def display_info(self) -> str:
        return f'ID владельца: {self.owner_id}, баланс: {self.balance}'

    def validate_for_transactions(self) -> None:
        if self.is_frozen:
            raise PermissionError('Карта заморожена')

    def deposit(self, amount: int) -> None:
        BankCard.validate_amount(amount)
        self.validate_for_transactions()

        self.balance += amount

        '''эту поправить на более стандартизированную'''
        self._notify('Пополнение', amount)

        self.transaction_history.append(Deposit(amount))

        '''мб удалить раз есть обсерверы с коллбеками'''
        print(f'Счёт пополнен на {amount}')

    def withdraw(self, amount: int, pin_code: str) -> None:
        BankCard.validate_amount(amount)
        self.validate_for_transactions()
        self.validate_pin(pin_code)

        '''пофиксить а то красным горит'''
        self.card_limit_checker.check_limit(self, amount)

        if self.balance < amount:
            raise ValueError('Недостаточно средств на балансе')

        comission = self.comission.calculate(amount)
        total = amount + comission

        self.balance -= total
        self.transaction_history.append(Withdraw(amount=amount, comission=comission))

        '''эту поправить на более стандартизированную'''
        self._notify('Снятие', total)

        '''todo реально отправить деньги юзеру'''

    def get_history(self) -> str:
        if len(self.transaction_history) == 0:
            return 'История пуста'

        return '\n'.join(map(transaction_to_str, self.transaction_history))

    def add_observer(self, observer: CardObserver) -> None:
        if type(observer) in [type(o) for o in self.observers]:
            print(f'{type(observer).__name__} уже записан')
            return
        self.observers.append(observer)

    def remove_observer(self, observer: CardObserver) -> None:
        self.observers.remove(observer)

    def get_observers_count(self) -> int:
        return len(self.observers)

    def list_observers(self) -> None:
        if not self.observers:
            print('Наблюдателей нету')
            return
        for i, obs in enumerate(self.observers):
            print(f'{i+1}. {type(obs).__name__}')

    def _notify(self, event: str, amount: int) -> None:
        for observer in self.observers:
            observer.update(event, amount, self.id)

    def validate_pin(self, pin: str) -> None:
        if self.pin != pin:
            raise InvalidPinError

    @staticmethod
    def validate_amount(amount: int) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise PermissionError("Нельзя делать покупки на отрицательную сумму")
